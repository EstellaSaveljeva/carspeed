import cv2
import numpy as np
from ultralytics import YOLO
import supervision as sv  # Используем Supervision

# Загрузка модели YOLO11X
model = YOLO("yolo11x.pt")

# Загрузка видео
video_path = "50kmh_prieksa_jaunolaine.mov"
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

# Координаты четырех углов области интереса (задай вручную)
x1, y1 = 5200, 3000  # Правый верхний угол
x2, y2 = 4100, 3000  # Левый верхний угол
x3, y3 = 7500, 6000  # Левый нижний угол
x4, y4 = 10700, 4600  # Правый нижний угол

# Приведение координат к масштабу кадра
x1, x2, x3, x4 = int(x1 * scale), int(x2 * scale), int(x3 * scale), int(x4 * scale)
y1, y2, y3, y4 = int(y1 * scale), int(y2 * scale), int(y3 * scale), int(y4 * scale)

# Создаем маску для выделенной зоны
mask = np.zeros_like(frame[:, :, 0], dtype=np.uint8)
pts = np.array([[x1, y1], [x2, y2], [x3, y3], [x4, y4]], np.int32)
cv2.fillPoly(mask, [pts], 255)  # Заливаем область белым

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

# Обработка каждого кадра видео
cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break  # Конец видео

    # Применяем маску, чтобы оставить только область интереса
    masked_frame = cv2.bitwise_and(frame, frame, mask=mask)

    # Запускаем YOLO на кадре
    results = model(masked_frame)

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

            # 🔹 Игнорируем слишком большие боксы (ошибочные детекции)
            box_width = x_max - x_min
            box_height = y_max - y_min
            if box_width > frame_width * 0.7 or box_height > frame_height * 0.7:
                continue

            # 🔹 Корректируем границы боксов
            x_min = max(x_min, 0)
            y_min = max(y_min, 0)
            x_max = min(x_max, frame_width)
            y_max = min(y_max, frame_height)

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

# Освобождение ресурсов
cap.release()
out.release()
cv2.destroyAllWindows()

print(f"✅ Обработанное видео сохранено как {output_path}")
