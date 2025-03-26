import cv2
import numpy as np
from ultralytics import YOLO
import supervision as sv
from deep_sort_realtime.deepsort_tracker import DeepSort
from collections import defaultdict, deque
from coordinates import get_coordinates

# Импорт функций для расчёта скорости
from speed_by_shift import compute_speed_shift
from speed_by_lines import update_vehicle_timestamp, compute_speed_line

def is_above_line(cx, cy, x1, y1, x2, y2):
    """
    Проверяет, находится ли точка (cx, cy) выше линии, заданной двумя точками (x1, y1) и (x2, y2).
    """
    if x1 == x2:
        return cx <= x1
    m = (y2 - y1) / (x2 - x1)
    b = y1 - m * x1
    y_on_line = m * cx + b
    return cy <= y_on_line

def main():
    # Загрузка модели YOLO
    model = YOLO("yolo11x.pt")

    # Загрузка видео
    video_path = "50kmh_prieksa_jaunolaine.mov"
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Ошибка: не удалось открыть видео.")
        return

    # Получение координат из coordinates.py
    try:
        (x1, y1, x2, y2, x3, y3, x4, y4, distance_m,
         blue_x1_top, blue_y1_top, blue_x2_top, blue_y2_top,
         blue_x1_bottom, blue_y1_bottom, blue_x2_bottom, blue_y2_bottom,
         blue_line_thickness) = get_coordinates(video_path)
    except ValueError as e:
        print(e)
        cap.release()
        return

    # Чтение первого кадра
    ret, frame = cap.read()
    if not ret:
        print("Ошибка: не удалось считать кадр.")
        cap.release()
        return

    # Получение параметров видео
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    # Масштабирование для отображения
    screen_width, screen_height = 1280, 720
    scale = min(screen_width / frame_width, screen_height / frame_height)
    new_width = int(frame_width * scale)
    new_height = int(frame_height * scale)

    # Настройка записи видео
    output_path = "output.mp4"
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

    # Приведение координат к масштабу
    x1, x2, x3, x4 = int(x1 * scale), int(x2 * scale), int(x3 * scale), int(x4 * scale)
    y1, y2, y3, y4 = int(y1 * scale), int(y2 * scale), int(y3 * scale), int(y4 * scale)
    blue_x1_top, blue_x2_top = int(blue_x1_top * scale), int(blue_x2_top * scale)
    blue_y1_top, blue_y2_top = int(blue_y1_top * scale), int(blue_y2_top * scale)
    blue_x1_bottom, blue_x2_bottom = int(blue_x1_bottom * scale), int(blue_x2_bottom * scale)
    blue_y1_bottom, blue_y2_bottom = int(blue_y1_bottom * scale), int(blue_y2_bottom * scale)

    # Настройка матрицы перспективного преобразования
    src = np.array([
        [blue_x1_top, blue_y1_top],
        [blue_x2_top, blue_y2_top],
        [blue_x1_bottom, blue_y1_bottom],
        [blue_x2_bottom, blue_y2_bottom]
    ], dtype=np.float32)

    dst = np.array([
        [0, 0],
        [6, 0],
        [0, distance_m],
        [6, distance_m]
    ], dtype=np.float32)

    matrix = cv2.getPerspectiveTransform(src, dst)

    # Определение области интереса (красная рамка)
    pts = np.array([[x1, y1], [x2, y2], [x3, y3], [x4, y4]], np.int32)

    # Отображение первого кадра с рамкой и линиями
    frame_with_zone = frame.copy()
    cv2.polylines(frame_with_zone, [pts], isClosed=True, color=(0, 0, 255), thickness=3)
    cv2.line(frame_with_zone, (blue_x1_top, blue_y1_top), (blue_x2_top, blue_y2_top), (255, 0, 0), blue_line_thickness)
    cv2.line(frame_with_zone, (blue_x1_bottom, blue_y1_bottom), (blue_x2_bottom, blue_y2_bottom), (255, 0, 0), blue_line_thickness)
    resized_frame = cv2.resize(frame_with_zone, (new_width, new_height))
    cv2.imshow("Область интереса (первый кадр)", resized_frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Инициализация аннотаторов
    box_annotator = sv.BoxAnnotator(color=sv.Color.GREEN, thickness=2)
    label_annotator = sv.LabelAnnotator(text_color=sv.Color.BLACK)

    # История для метода сдвига (храним историю реальных координат)
    real_y_history = defaultdict(lambda: deque(maxlen=int(fps)))

    # Инициализация трекера Deep SORT
    tracker = DeepSort(max_age=30)

    # Словарь для временных меток (метод линий)
    vehicle_timestamps = {}

    # Хранение скоростей по методу сдвига
    vehicle_speeds_shift = defaultdict(list)

    frame_count = 0
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    # Определение верхней и нижней линий для расчёта скорости (кортежи: (x1, y1, x2, y2))
    top_line = (blue_x1_top, blue_y1_top, blue_x2_top, blue_y2_top)
    bottom_line = (blue_x1_bottom, blue_y1_bottom, blue_x2_bottom, blue_y2_bottom)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_time = frame_count / fps
        frame_count += 1

        results = model(frame)
        boxes_for_tracking = []

        # Формирование списка детекций для трекера
        for result in results:
            for box in result.boxes:
                x_min, y_min, x_max, y_max = map(int, box.xyxy[0])
                conf = box.conf[0].item()
                cls = int(box.cls[0].item())

                # Отсеиваем всё, кроме автомобилей (класс 2)
                if cls != 2:
                    continue

                if not cv2.pointPolygonTest(pts, ((x_min + x_max) // 2, (y_min + y_max) // 2), False) >= 0:
                    continue

                boxes_for_tracking.append(([x_min, y_min, x_max - x_min, y_max - y_min], conf, 'car'))

        tracks = tracker.update_tracks(boxes_for_tracking, frame=frame)
        
        tracked_boxes = []
        confidences = []
        class_ids = []
        labels = []

        for track in tracks:
            if not track.is_confirmed():
                continue

            track_id = track.track_id
            l, t, r, b = map(int, track.to_ltrb())
            cx = (l + r) // 2
            cy = b

                    # Преобразование координат в реальное пространство
            real_point = cv2.perspectiveTransform(
                np.array([[[cx, cy]]], dtype=np.float32),
                matrix
            )[0][0]

            real_y_history[track_id].append(real_point)

            # Обновление временных меток для метода линий
            if track_id not in vehicle_timestamps:
                vehicle_timestamps[track_id] = {"start": None, "end": None, "last_position": cy, "done": False}
            if not vehicle_timestamps[track_id].get("done"):
                update_vehicle_timestamp(vehicle_timestamps[track_id], cx, cy, frame_time, top_line, bottom_line, is_above_line)

            # Вычисление скорости по методу сдвига только между синими линиями
            speed_transformed = None
            if is_above_line(cx, cy, blue_x1_bottom, blue_y1_bottom, blue_x2_bottom, blue_y2_bottom) and \
            not is_above_line(cx, cy, blue_x1_top, blue_y1_top, blue_x2_top, blue_y2_top):
                last_speed = vehicle_speeds_shift[track_id][-1] if vehicle_speeds_shift[track_id] else None
                speed_transformed = compute_speed_shift(real_y_history[track_id], fps, last_speed)

            # Формирование подписи с обеими скоростями
            label_parts = []
            if speed_transformed is not None:
                label_parts.append(f"T: {speed_transformed:.1f} km/h")
            speed_line = compute_speed_line(vehicle_timestamps[track_id], distance_m)
            if speed_line is not None:
                label_parts.append(f"L: {speed_line:.1f} km/h")
            if not label_parts:
                label_parts.append("Tracking...")

            labels.append(" | ".join(label_parts))
            tracked_boxes.append([l, t, r, b])
            confidences.append(1.0)
            class_ids.append(2)

        if tracked_boxes:
            detections_sv = sv.Detections(
                xyxy=np.array(tracked_boxes),
                confidence=np.array(confidences),
                class_id=np.array(class_ids)
            )
            frame = box_annotator.annotate(scene=frame, detections=detections_sv)
            frame = label_annotator.annotate(scene=frame, detections=detections_sv, labels=labels)

        cv2.line(frame, (blue_x1_top, blue_y1_top), (blue_x2_top, blue_y2_top), (255, 0, 0), blue_line_thickness)
        cv2.line(frame, (blue_x1_bottom, blue_y1_bottom), (blue_x2_bottom, blue_y2_bottom), (255, 0, 0), blue_line_thickness)
        cv2.polylines(frame, [pts], isClosed=True, color=(0, 0, 255), thickness=2)

        out.write(frame)

    # Вывод итоговых скоростей (метод линий)
    print("\n📊 Итоговые скорости (линия):")
    for vehicle_id, times in vehicle_timestamps.items():
        speed_kmh = compute_speed_line(times, distance_m)
        if speed_kmh is not None:
            print(f"🚗 Машина {vehicle_id}: L: {speed_kmh:.2f} км/ч")

    # Вывод итоговых скоростей (метод сдвига)
    print("\n📊 Итоговые скорости (сдвиг):")
    for vehicle_id, speeds in vehicle_speeds_shift.items():
        if speeds:
            avg_speed_shift = sum(speeds) / len(speeds)
            print(f"🚗 Машина {vehicle_id}: T: {avg_speed_shift:.2f} км/ч")

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print(f"✅ Обработанное видео сохранено как {output_path}")

if __name__ == "__main__":
    main()
