import cv2
import numpy as np
from ultralytics import YOLO
import supervision as sv
from deep_sort_realtime.deepsort_tracker import DeepSort

# Загрузка модели YOLO11X
model = YOLO("yolo11x.pt")

# Загрузка видео
video_path = "70kmh_prieksa_jaunolaine.mov"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Ошибка: не удалось открыть видео.")
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

# 🟥 Координаты рамки и синих линий под разные видео
if "50kmh_mugur_jaunolaine" in video_path.lower():
    # Красная рамка
    x1, y1 = 5000, 2900      # Augšējais labais stūris
    x2, y2 = 4000, 2900     # Augšējais kreisais stūris
    x3, y3 = 7400, 6000     # Kreisais apakšējais stūris
    x4, y4 = 10500, 4600    # Apakšējais labais stūris
    distance_m = 200

    # 🟦 Синие линии
    blue_x1_top, blue_y1_top = 4800, 3100            # Augšējais labais stūris
    blue_x2_top, blue_y2_top = 4200, 3200            # Augšējais kreisais stūris
    blue_x1_bottom, blue_y1_bottom = 7300, 5800      # Kreisais apakšējais stūris
    blue_x2_bottom, blue_y2_bottom = 10000, 5500     # Apakšējais labais stūris

    blue_line_thickness = 3

elif "50kmh_prieksa_jaunolaine" in video_path.lower():
    # Красная рамка
    x1, y1 = 5100, 2800     # Augšējais labais stūris
    x2, y2 = 4200, 2800     # Augšējais kreisais stūris
    x3, y3 = 7500, 5900     # Kreisais apakšējais stūris
    x4, y4 = 10600, 4500     # Apakšējais labais stūris
    distance_m = 200

    # 🟦 Синие линии
    blue_x1_top, blue_y1_top = 4900, 3150           # Augšējais labais stūris
    blue_x2_top, blue_y2_top = 4300, 3250           # Augšējais kreisais stūris
    blue_x1_bottom, blue_y1_bottom = 7400, 5850     # Kreisais apakšējais stūris
    blue_x2_bottom, blue_y2_bottom = 10100, 5450    # Apakšējais labais stūris

    blue_line_thickness = 3

elif "70kmh_mugur_jaunolaine" in video_path.lower():
    # Красная рамка
    x1, y1 = 4950, 2850     # Augšējais labais stūris
    x2, y2 = 3950, 2850     # Augšējais kreisais stūris
    x3, y3 = 7300, 5900     # Kreisais apakšējais stūris
    x4, y4 = 10400, 4550     # Apakšējais labais stūris
    distance_m = 200

    # 🟦 Синие линии
    blue_x1_top, blue_y1_top = 4750, 3050           # Augšējais labais stūris
    blue_x2_top, blue_y2_top = 4150, 3150           # Augšējais kreisais stūris
    blue_x1_bottom, blue_y1_bottom = 7250, 5750     # Kreisais apakšējais stūris
    blue_x2_bottom, blue_y2_bottom = 9950, 5400     # Apakšējais labais stūris

    blue_line_thickness = 5

elif "70kmh_prieksa_jaunolaine" in video_path.lower():
    # Красная рамка
    x1, y1 = 5150, 3000   # Augšējais labais stūris
    x2, y2 = 4750, 3000   # Augšējais kreisais stūris
    x3, y3 = 8000, 6000   # Kreisais apakšējais stūris
    x4, y4 = 10700, 4600  # Apakšējais labais stūris
    distance_m = 100

    # 🟦 Синие линии
    blue_x1_top, blue_y1_top = 5200, 3025         # Augšējais labais stūris
    blue_x2_top, blue_y2_top = 4800, 3050         # Augšējais kreisais stūris
    blue_x1_bottom, blue_y1_bottom = 7950, 5950   # Kreisais apakšējais stūris
    blue_x2_bottom, blue_y2_bottom = 10650, 4550  # Apakšējais labais stūris

    blue_line_thickness = 5

elif "50kmh_ropazi" in video_path.lower():
    # Красная рамка
    x1, y1 = 6400, 2900     # Augšējais labais stūris
    x2, y2 = 5700, 2900     # Augšējais kreisais stūris
    x3, y3 = 500, 5800      # Kreisais apakšējais stūris
    x4, y4 = 6900, 5800     # Apakšējais labais stūris
    distance_m = 150

    # 🟦 Синие линии (наклонные)
    blue_x1_top, blue_y1_top = 6200, 3000           # Augšējais labais stūris
    blue_x2_top, blue_y2_top = 5000, 3100           # Augšējais kreisais stūris
    blue_x1_bottom, blue_y1_bottom = 5400, 5600     # Kreisais apakšējais stūris
    blue_x2_bottom, blue_y2_bottom = 3000, 5700     # Apakšējais labais stūris

    blue_line_thickness = 3

elif "70kmh_ropazi" in video_path.lower():
    # Красная рамка
    x1, y1 = 6500, 2950     # Augšējais labais stūris
    x2, y2 = 5800, 2950     # Augšējais kreisais stūris
    x3, y3 = 550, 5850      # Kreisais apakšējais stūris
    x4, y4 = 6950, 5850     # Apakšējais labais stūris
    distance_m = 150

    # 🟦 Синие линии
    blue_x1_top, blue_y1_top = 6300, 3100           # Augšējais labais stūris
    blue_x2_top, blue_y2_top = 5100, 3200           # Augšējais kreisais stūris
    blue_x1_bottom, blue_y1_bottom = 5500, 5650     # Kreisais apakšējais stūris
    blue_x2_bottom, blue_y2_bottom = 3100, 5750     # Apakšējais labais stūris

    blue_line_thickness = 3

elif "80kmh_ropazi" in video_path.lower():
    # Красная рамка
    x1, y1 = 6600, 3000     # Augšējais labais stūris
    x2, y2 = 5900, 3000     # Augšējais kreisais stūris
    x3, y3 = 600, 5900      # Kreisais apakšējais stūris
    x4, y4 = 7000, 5900     # Apakšējais labais stūris
    distance_m = 150

    # 🟦 Синие линии
    blue_x1_top, blue_y1_top = 6400, 3150           # Augšējais labais stūris
    blue_x2_top, blue_y2_top = 5200, 3250           # Augšējais kreisais stūris
    blue_x1_bottom, blue_y1_bottom = 5600, 5700     # Kreisais apakšējais stūris
    blue_x2_bottom, blue_y2_bottom = 3200, 5800     # Apakšējais labais stūris

    blue_line_thickness = 3

else:
    print("Ошибка: неизвестный тип видео.")
    cap.release()
    exit()



# Приведение координат к масштабу
x1, x2, x3, x4 = int(x1 * scale), int(x2 * scale), int(x3 * scale), int(x4 * scale)
y1, y2, y3, y4 = int(y1 * scale), int(y2 * scale), int(y3 * scale), int(y4 * scale)

blue_x1_top, blue_x2_top = int(blue_x1_top * scale), int(blue_x2_top * scale)
blue_y1_top, blue_y2_top = int(blue_y1_top * scale), int(blue_y2_top * scale)
blue_x1_bottom, blue_x2_bottom = int(blue_x1_bottom * scale), int(blue_x2_bottom * scale)
blue_y1_bottom, blue_y2_bottom = int(blue_y1_bottom * scale), int(blue_y2_bottom * scale)


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
label_annotator = sv.LabelAnnotator()

# Deep SORT трекер
tracker = DeepSort(max_age=30)

# Словарь для засечки времени
vehicle_timestamps = {}

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
        l, t, r, b = map(int, track.to_ltrb())
        cx = (l + r) // 2
        cy = (t + b) // 2

        if track_id not in vehicle_timestamps:
            vehicle_timestamps[track_id] = {"start": None, "end": None, "last_position": cy}

        last_cy = vehicle_timestamps[track_id]["last_position"]

        if vehicle_timestamps[track_id]["start"] is None and is_above_line(cx, cy, blue_x1_top, blue_y1_top, blue_x2_top, blue_y2_top):
            vehicle_timestamps[track_id]["start"] = frame_time

        if vehicle_timestamps[track_id]["end"] is None and not is_above_line(cx, cy, blue_x1_bottom, blue_y1_bottom, blue_x2_bottom, blue_y2_bottom):
            vehicle_timestamps[track_id]["end"] = frame_time

        vehicle_timestamps[track_id]["last_position"] = cy
        # 🟩 Добавляем в список для отрисовки
        tracked_boxes.append([l, t, r, b])
        confidences.append(1.0)
        class_ids.append(2)
        labels.append(f"ID {track_id}")


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

for vehicle_id, times in vehicle_timestamps.items():
    if times["start"] is not None and times["end"] is not None:
        travel_time = times["end"] - times["start"]
        speed_kmh = (distance_m / travel_time) * 3.6
        print(f"🚗 Машина {vehicle_id} -> Скорость: {speed_kmh:.2f} км/ч")

cap.release()
out.release()
cv2.destroyAllWindows()

print(f"✅ Обработанное видео сохранено как {output_path}")
