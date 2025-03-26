import cv2
import numpy as np
from ultralytics import YOLO
import supervision as sv
from deep_sort_realtime.deepsort_tracker import DeepSort

# Загрузка модели YOLO11X
model = YOLO("yolo11x.pt")

from coordinates import get_coordinates

# Загрузка видео
video_path = "70kmh_ropazi.mov"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Ошибка: не удалось открыть видео.")
    exit()

# Получение координат из coordinates.py
try:
    (x1, y1, x2, y2, x3, y3, x4, y4, distance_m,
     blue_x1_top, blue_y1_top, blue_x2_top, blue_y2_top,
     blue_x1_bottom, blue_y1_bottom, blue_x2_bottom, blue_y2_bottom,
     blue_line_thickness) = get_coordinates(video_path)
except ValueError as e:
    print(e)
    cap.release()
    exit()

# Читаем первый кадр
ret, frame = cap.read()
if not ret:
    print("Ошибка: не удалось считать кадр.")
    cap.release()
    exit()

# Получение параметров исходного видео
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

# Размер окна для масштабирования (чтобы первый кадр влезал в экран)
screen_width, screen_height = 1280, 720
scale = min(screen_width / frame_width, screen_height / frame_height)
new_width = int(frame_width * scale)
new_height = int(frame_height * scale)

# Настройка видеозаписи
output_path = "output.mp4"
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

# # 🟥 Координаты рамки и синих линий под разные видео
# if "50kmh_mugur_jaunolaine" in video_path.lower():
#     # Красная рамка
#     x1, y1 = 5000, 2900      # Augšējais labais stūris
#     x2, y2 = 4000, 2900     # Augšējais kreisais stūris
#     x3, y3 = 7400, 6000     # Kreisais apakšējais stūris
#     x4, y4 = 10500, 4600    # Apakšējais labais stūris
#     distance_m = 200

#     # 🟦 Синие линии
#     blue_x1_top, blue_y1_top = 5000, 3050           # Augšējais kreisais stūris
#     blue_x2_top, blue_y2_top = 5300, 3050           # Augšējais labais stūris
#     blue_x1_bottom, blue_y1_bottom = 7400, 5000     # Kreisais apakšējais stūris
#     blue_x2_bottom, blue_y2_bottom = 10900, 5250    # Apakšējais labais stūris

#     blue_line_thickness = 3

# elif "50kmh_prieksa_jaunolaine" in video_path.lower():
#     # Красная рамка
#     x1, y1 = 5200, 3000     # Augšējais labais stūris
#     x2, y2 = 4900, 3000     # Augšējais kreisais stūris
#     x3, y3 = 7950, 5500     # Kreisais apakšējais stūris
#     x4, y4 = 11000, 4800    # Apakšējais labais stūris
#     distance_m = 60

#     # 🟦 Синие линии
#     blue_x1_top, blue_y1_top = 4950, 3100           # Augšējais kreisais stūris
#     blue_x2_top, blue_y2_top = 5550, 3075           # Augšējais labais stūris
#     blue_x1_bottom, blue_y1_bottom = 7400, 5500     # Kreisais apakšējais stūris
#     blue_x2_bottom, blue_y2_bottom = 11000, 4750    # Apakšējais labais stūris

#     blue_line_thickness = 3

# elif "70kmh_mugur_jaunolaine" in video_path.lower():
#     # Красная рамка
#     x1, y1 = 4950, 2850     # Augšējais labais stūris
#     x2, y2 = 3950, 2850     # Augšējais kreisais stūris
#     x3, y3 = 7300, 5900     # Kreisais apakšējais stūris
#     x4, y4 = 10400, 4550     # Apakšējais labais stūris
#     distance_m = 200

#     # 🟦 Синие линии
#     blue_x1_top, blue_y1_top = 5000, 3050           # Augšējais kreisais stūris
#     blue_x2_top, blue_y2_top = 5300, 3050           # Augšējais labais stūris
#     blue_x1_bottom, blue_y1_bottom = 7400, 5000     # Kreisais apakšējais stūris
#     blue_x2_bottom, blue_y2_bottom = 10900, 5250    # Apakšējais labais stūris

#     blue_line_thickness = 3

# elif "70kmh_prieksa_jaunolaine" in video_path.lower():
#     # Красная рамка
#     x1, y1 = 5150, 3000   # Augšējais labais stūris
#     x2, y2 = 4750, 3000   # Augšējais kreisais stūris
#     x3, y3 = 8000, 6000   # Kreisais apakšējais stūris
#     x4, y4 = 10700, 4600  # Apakšējais labais stūris
#     distance_m = 60

#     # 🟦 Синие линии
#     blue_x1_top, blue_y1_top = 5200, 3025         # Augšējais kreisais stūris
#     blue_x2_top, blue_y2_top = 4800, 3050         # Augšējais labais stūris
#     blue_x1_bottom, blue_y1_bottom = 7950, 5950   # Kreisais apakšējais stūris
#     blue_x2_bottom, blue_y2_bottom = 10650, 4550  # Apakšējais labais stūris

#     blue_line_thickness = 3

# elif "50kmh_ropazi" in video_path.lower():
#     # Красная рамка
#     x1, y1 = 6400, 2900     # Augšējais labais stūris
#     x2, y2 = 5700, 2900     # Augšējais kreisais stūris
#     x3, y3 = 500, 5800      # Kreisais apakšējais stūris
#     x4, y4 = 6900, 5800     # Apakšējais labais stūris
#     distance_m = 150

#     # 🟦 Синие линии (наклонные)
#     blue_x1_top, blue_y1_top = 5000, 3050           # Augšējais kreisais stūris
#     blue_x2_top, blue_y2_top = 5300, 3050           # Augšējais labais stūris
#     blue_x1_bottom, blue_y1_bottom = 7400, 5000     # Kreisais apakšējais stūris
#     blue_x2_bottom, blue_y2_bottom = 10900, 5250    # Apakšējais labais stūris

#     blue_line_thickness = 3

# elif "70kmh_ropazi" in video_path.lower():
#     # Красная рамка
#     x1, y1 = 6400, 3200     # Augšējais labais stūris
#     x2, y2 = 5700, 3200     # Augšējais Kreisais stūris
#     x3, y3 = 500, 5700     # Apakšējais Kreisais stūris
#     x4, y4 = 6600, 6200    # labais apakšējais stūris
#     distance_m =45

#     # 🟦 Синие линии
#     blue_x1_top, blue_y1_top = 5350, 3275           # Augšējais kreisais stūris
#     blue_x2_top, blue_y2_top = 6400, 3275           # Augšējais labais stūris
#     blue_x1_bottom, blue_y1_bottom = 1050, 5500     # Kreisais apakšējais stūris
#     blue_x2_bottom, blue_y2_bottom = 6450, 5900    # Apakšējais labais stūris

#     blue_line_thickness = 3

# elif "80kmh_ropazi" in video_path.lower():
#     # Красная рамка
#     x1, y1 = 6600, 3000     # Augšējais labais stūris
#     x2, y2 = 5900, 3000     # Augšējais kreisais stūris
#     x3, y3 = 600, 5900      # Kreisais apakšējais stūris
#     x4, y4 = 7000, 5900     # Apakšējais labais stūris
#     distance_m = 150

#     # 🟦 Синие линии
#     blue_x1_top, blue_y1_top = 5000, 3050           # Augšējais kreisais stūris
#     blue_x2_top, blue_y2_top = 5300, 3050           # Augšējais labais stūris
#     blue_x1_bottom, blue_y1_bottom = 7400, 5000     # Kreisais apakšējais stūris
#     blue_x2_bottom, blue_y2_bottom = 10900, 5250    # Apakšējais labais stūris

#     blue_line_thickness = 3

# else:
#     print("Ошибка: неизвестный тип видео.")
#     cap.release()
#     exit()



# Приведение координат к масштабу
x1, x2, x3, x4 = int(x1 * scale), int(x2 * scale), int(x3 * scale), int(x4 * scale)
y1, y2, y3, y4 = int(y1 * scale), int(y2 * scale), int(y3 * scale), int(y4 * scale)

blue_x1_top, blue_x2_top = int(blue_x1_top * scale), int(blue_x2_top * scale)
blue_y1_top, blue_y2_top = int(blue_y1_top * scale), int(blue_y2_top * scale)
blue_x1_bottom, blue_x2_bottom = int(blue_x1_bottom * scale), int(blue_x2_bottom * scale)
blue_y1_bottom, blue_y2_bottom = int(blue_y1_bottom * scale), int(blue_y2_bottom * scale)

src = np.array([
    [blue_x1_top, blue_y1_top],
    [blue_x2_top, blue_y2_top],
    [blue_x1_bottom, blue_y1_bottom],
    [blue_x2_bottom, blue_y2_bottom]
    #[blue_x1_bottom, blue_y1_bottom]
], dtype=np.float32)

dst = np.array([
    [0, 0],
    [6, 0],  # ширина полосы — 4 м
    [0, distance_m],     # 60 м по вертикали между синими линиями
    [6, distance_m]
], dtype=np.float32)

matrix = cv2.getPerspectiveTransform(src, dst)


# Красная рамка (область интереса)
pts = np.array([[x1, y1], [x2, y2], [x3, y3], [x4, y4]], np.int32)

# 🔴 Показываем первый кадр с рамкой и синими линиями
frame_with_zone = frame.copy()
# Рисуем красную рамку
cv2.polylines(frame_with_zone, [pts], isClosed=True, color=(0, 0, 255), thickness=3)
# Рисуем синие линии
# 🟦 Рисуем синие линии (наклонные)
# 🔵 Теперь добавляем синие линии в `frame_with_zone`
cv2.line(frame_with_zone, (blue_x1_top, blue_y1_top), (blue_x2_top, blue_y2_top), (255, 0, 0), blue_line_thickness)
cv2.line(frame_with_zone, (blue_x1_bottom, blue_y1_bottom), (blue_x2_bottom, blue_y2_bottom), (255, 0, 0), blue_line_thickness)

# Масштабируем для экрана и показываем
resized_frame = cv2.resize(frame_with_zone, (new_width, new_height))
cv2.imshow("Область интереса (первый кадр)", resized_frame)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 📌 Функция для проверки, выше ли точка (cx, cy) наклонной линии
def is_above_line(cx, cy, x1, y1, x2, y2):
    if x1 == x2:
        return cx <= x1
    m = (y2 - y1) / (x2 - x1)
    b = y1 - m * x1
    y_on_line = m * cx + b
    return cy <= y_on_line

# 🟢 Аннотаторы
box_annotator = sv.BoxAnnotator(color=sv.Color.GREEN, thickness=2)

label_annotator = sv.LabelAnnotator(
    text_color=sv.Color.BLACK,       # цвет текста
)

from collections import defaultdict, deque

# История Y-координат в метрах после трансформации — храним последнюю 1 секунду
real_y_history = defaultdict(lambda: deque(maxlen=int(fps)))


# Deep SORT трекер
tracker = DeepSort(max_age=30)

# Словарь для засечки времени
vehicle_timestamps = {}

# Хранение всех скоростей по сдвигу
vehicle_speeds_shift = defaultdict(list)  


# Обработка кадров
frame_count = 0
cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_time = frame_count / fps
    frame_count += 1

    results = model(frame)
    detections = []
    boxes_for_tracking = []

    for result in results:
        for box in result.boxes:
            x_min, y_min, x_max, y_max = map(int, box.xyxy[0])
            conf = box.conf[0].item()
            cls = int(box.cls[0].item())

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

        # координаты центра
        l, t, r, b = map(int, track.to_ltrb())
        cx = (l + r) // 2
        cy = b  # нижняя граница (bottom)


        # перспектива
        real_point = cv2.perspectiveTransform(
            np.array([[[cx, cy]]], dtype=np.float32),
           matrix
        )[0][0]


        real_y_history[track_id].append(real_point)  # это уже (x, y)


        # если машина уже прошла обе линии — больше ничего не делаем
        if vehicle_timestamps.get(track_id, {}).get("done"):
            continue


        speed_transformed = None

        # Только если объект между линиями
        if is_above_line(cx, cy, blue_x1_bottom, blue_y1_bottom, blue_x2_bottom, blue_y2_bottom) and \
           not is_above_line(cx, cy, blue_x1_top, blue_y1_top, blue_x2_top, blue_y2_top):
            
            if len(real_y_history[track_id]) >= 2:
                # Переводим всю историю Y-координат в массив точек (x, y)
                points = np.array(real_y_history[track_id], dtype=np.float32)

                # Считаем длину пути вдоль всей траектории
                distances = np.linalg.norm(np.diff(points, axis=0), axis=1)
                total_distance = np.sum(distances)
                time_delta = len(real_y_history[track_id]) / fps

                if time_delta > 0 and total_distance > 0.1:
                    speed_transformed = (total_distance / time_delta) * 3.6



        # Сохранение скорости по сдвигу
        if speed_transformed is not None:
            # Ограничение скачков скорости (максимум +30% от предыдущей)
            if len(vehicle_speeds_shift[track_id]) > 0:
                last_speed = vehicle_speeds_shift[track_id][-1]
                if abs(speed_transformed - last_speed) > last_speed * 0.3:  # Не более 30% скачка
                    speed_transformed = last_speed

            vehicle_speeds_shift[track_id].append(speed_transformed)


        # Метод с линиями (остался без изменений)
        if track_id not in vehicle_timestamps:
            vehicle_timestamps[track_id] = {
            "start": None,
            "end": None,
            "last_position": cy,
            "done": False
        }


        last_cy = vehicle_timestamps[track_id]["last_position"]

        # ➕ Перед расчётом скорости, определяем направление:
        direction = cy - last_cy  # + вниз, - вверх

        # ⛔ Если машина движется вверх (от нижней к верхней линии), игнорируем расчёты
        if direction < -2:  # с порогом для стабильности
            continue



        if vehicle_timestamps[track_id]["start"] is None and is_above_line(cx, cy, blue_x1_top, blue_y1_top, blue_x2_top, blue_y2_top):
            vehicle_timestamps[track_id]["start"] = frame_time

        if vehicle_timestamps[track_id]["end"] is None and not is_above_line(cx, cy, blue_x1_bottom, blue_y1_bottom, blue_x2_bottom, blue_y2_bottom):
            vehicle_timestamps[track_id]["end"] = frame_time
            vehicle_timestamps[track_id]["done"] = True  # больше не обновляем историю


        vehicle_timestamps[track_id]["last_position"] = cy


       # 🟩 Добавляем в список для отрисовки
        tracked_boxes.append([l, t, r, b])
        confidences.append(1.0)
        class_ids.append(2)

        # 🏷 Создаём подпись с обеими скоростями
        label_parts = []

        if speed_transformed is not None:
            label_parts.append(f"T: {speed_transformed:.1f} km/h")

        if vehicle_timestamps[track_id]["start"] is not None and vehicle_timestamps[track_id]["end"] is not None:
            travel_time = vehicle_timestamps[track_id]["end"] - vehicle_timestamps[track_id]["start"]
            if travel_time > 0:
                speed_line = (distance_m / travel_time) * 3.6
                label_parts.append(f"L: {speed_line:.1f} km/h")

        if not label_parts:
            label_parts.append("Tracking...")

        labels.append(" | ".join(label_parts))



    if tracked_boxes:
        detections_sv = sv.Detections(
            xyxy=np.array(tracked_boxes),
            confidence=np.array(confidences),
            class_id=np.array(class_ids)
        )

        # 🟩 Отрисовка боксов и подписей
        frame = box_annotator.annotate(scene=frame, detections=detections_sv)
        frame = label_annotator.annotate(scene=frame, detections=detections_sv, labels=labels)


    cv2.line(frame, (blue_x1_top, blue_y1_top), (blue_x2_top, blue_y2_top), (255, 0, 0), blue_line_thickness)
    cv2.line(frame, (blue_x1_bottom, blue_y1_bottom), (blue_x2_bottom, blue_y2_bottom), (255, 0, 0), blue_line_thickness)
    # 🟥 Красная рамка
    cv2.polylines(frame, [pts], isClosed=True, color=(0, 0, 255), thickness=2)

    out.write(frame)

# Вывод результатов обоих методов
print("\n📊 Итоговые скорости:")

for vehicle_id, times in vehicle_timestamps.items():
    if times["start"] is not None and times["end"] is not None:
        travel_time = times["end"] - times["start"]
        speed_kmh = (distance_m / travel_time) * 3.6
        print(f"🚗 Машина {vehicle_id}: L: {speed_kmh:.2f} км/ч")

for vehicle_id, speeds in vehicle_speeds_shift.items():
    if speeds:
        avg_speed_shift = sum(speeds) / len(speeds)
        print(f"🚗 Машина {vehicle_id}: T: {avg_speed_shift:.2f} км/ч")

cap.release()
out.release()
cv2.destroyAllWindows()


cap.release()
out.release()
cv2.destroyAllWindows()

print(f"✅ Обработанное видео сохранено как {output_path}")
