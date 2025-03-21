import cv2
import numpy as np
from ultralytics import YOLO
import supervision as sv  # Используем Supervision

# Загрузка модели YOLO11X
model = YOLO("yolo11x.pt")

# Загрузка видео
video_path = "50kmh_ropazi.mov"
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
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Кодек для MP4
out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

# 🟥 Выбор координат красной рамки в зависимости от названия видео
if "jaunolaine" in video_path.lower():
    x1, y1 = 5200, 3000  # Augšējais labais stūris 
    x2, y2 = 4100, 3000  # Augšējais kreisais stūris
    x3, y3 = 7500, 6000  # Apakšējais kreisais stūris
    x4, y4 = 10700, 4600 # Apakšējais labais stūris
    distance_m = 200  # Расстояние между границами (метры)
elif "ropazi" in video_path.lower():
    x1, y1 = 6400, 2900  # Augšējais labais stūris
    x2, y2 = 5700, 2900  # Augšējais kreisais stūris
    x3, y3 = 500, 5800   # Apakšējais kreisais stūris
    x4, y4 = 6900, 5800  # Apakšējais labais stūris
    distance_m = 150  # Расстояние между границами (метры)
else:
    print("Ошибка: название видео не содержит 'jaunolaine' или 'ropazi'. Укажите правильный файл.")
    cap.release()
    exit()

# Приведение координат к масштабу кадра
x1, x2, x3, x4 = int(x1 * scale), int(x2 * scale), int(x3 * scale), int(x4 * scale)
y1, y2, y3, y4 = int(y1 * scale), int(y2 * scale), int(y3 * scale), int(y4 * scale)

# Создаем красную рамку (без маски)
pts = np.array([[x1, y1], [x2, y2], [x3, y3], [x4, y4]], np.int32)

# 🔴 **Вывод первого кадра с красной рамкой**
frame_with_zone = frame.copy()
cv2.polylines(frame_with_zone, [pts], isClosed=True, color=(0, 0, 255), thickness=3)
resized_frame = cv2.resize(frame_with_zone, (new_width, new_height))  # Масштабирование для окна
cv2.imshow("Область интереса (первый кадр)", resized_frame)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 🟢 Supervision: Настройка аннотаторов
box_annotator = sv.BoxAnnotator(color=sv.Color.GREEN, thickness=2)  # Рамка
label_annotator = sv.LabelAnnotator()  # Подписи

# Словарь для отслеживания машин (ID -> время пересечения границ)
vehicle_timestamps = {}

# Обработка каждого кадра видео
frame_count = 0
cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break  # Конец видео

    frame_time = frame_count / fps  # Текущее время кадра (секунды)
    frame_count += 1

    # Запускаем YOLO на полном кадре (🚗 теперь видит машину везде!)
    results = model(frame)

    detections = []  # Список всех найденных машин
    confidences = []  # Список вероятностей
    class_ids = []  # Список классов
    labels = []  # Текстовые подписи

    for result in results:
        for box in result.boxes:
            x_min, y_min, x_max, y_max = map(int, box.xyxy[0])
            conf = box.conf[0].item()
            cls = int(box.cls[0].item())

            # 🔹 Фильтруем только машины (класс "car")
            if cls != 2:
                continue

            # 🔹 Корректируем границы боксов
            x_min = max(x_min, 0)
            y_min = max(y_min, 0)
            x_max = min(x_max, frame_width)
            y_max = min(y_max, frame_height)

            # 🔹 Определяем ID машины (на основе координат)
            vehicle_id = (x_min, x_max)  # Уникальный идентификатор

            # 🔹 Отслеживание пересечения верхней и нижней границы
            if vehicle_id not in vehicle_timestamps:
                if y_min <= y1:  # Верхняя граница
                    vehicle_timestamps[vehicle_id] = {"start": frame_time, "end": None}
            else:
                if y_max >= y3 and vehicle_timestamps[vehicle_id]["end"] is None:  # Нижняя граница
                    vehicle_timestamps[vehicle_id]["end"] = frame_time

            # 🔹 Добавляем в список для Supervision
            detections.append([x_min, y_min, x_max, y_max])
            confidences.append(conf)
            class_ids.append(cls)

            # 🔹 Создаем текстовую метку
            labels.append(f"Car {conf:.2f}")

    if detections:
        detections_np = np.array(detections)
        confidences_np = np.array(confidences)
        class_ids_np = np.array(class_ids)

        # Создаем объект Detections
        detections_sv = sv.Detections(xyxy=detections_np, confidence=confidences_np, class_id=class_ids_np)

        # Отрисовываем боксы
        frame = box_annotator.annotate(scene=frame, detections=detections_sv)

        # Добавляем подписи над рамками
        frame = label_annotator.annotate(scene=frame, detections=detections_sv, labels=labels)

    # Рисуем красную рамку вокруг зоны интереса
    cv2.polylines(frame, [pts], isClosed=True, color=(0, 0, 255), thickness=2)

    # Записываем обработанный кадр в файл
    out.write(frame)

# Вычисляем скорость
for vehicle_id, times in vehicle_timestamps.items():
    if times["start"] is not None and times["end"] is not None:
        travel_time = times["end"] - times["start"]  # Время в секундах
        speed_kmh = (distance_m / travel_time) * 3.6  # Перевод в км/ч
        print(f"🚗 Машина {vehicle_id} -> Скорость: {speed_kmh:.2f} км/ч")

# Освобождение ресурсов
cap.release()
out.release()
cv2.destroyAllWindows()

print(f"✅ Обработанное видео сохранено как {output_path}")
