import cv2
import numpy as np
from ultralytics import YOLO

# Загрузка модели YOLO11X
model = YOLO("yolo11x.pt")

# Загрузка видео
video_path = "70km_h_prieksa.mp4"  # Имя видеофайла
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
fps = int(cap.get(cv2.CAP_PROP_FPS))  # Частота кадров

# Размер окна для масштабирования
screen_width, screen_height = 1280, 720
scale = min(screen_width / frame_width, screen_height / frame_height)
new_width = int(frame_width * scale)
new_height = int(frame_height * scale)

# Настройка видеозаписи
output_path = "output.mp4"
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Кодек для MP4
out = cv2.VideoWriter(output_path, fourcc, fps, (new_width, new_height))

# Координаты четырех углов области интереса (задай вручную)
x1, y1 = 1715, 1000  # Правый верхний угол
x2, y2 = 1610, 1025  # Левый верхний угол
x3, y3 = 2850, 2140  # Левый нижний угол
x4, y4 = 3660, 1540  # Правый нижний угол

# Приведение координат к масштабу кадра
x1, x2, x3, x4 = int(x1 * scale), int(x2 * scale), int(x3 * scale), int(x4 * scale)
y1, y2, y3, y4 = int(y1 * scale), int(y2 * scale), int(y3 * scale), int(y4 * scale)

# Создаем маску для выделенной зоны
mask = np.zeros_like(frame[:, :, 0], dtype=np.uint8)
pts = np.array([[x1, y1], [x2, y2], [x3, y3], [x4, y4]], np.int32)
cv2.fillPoly(mask, [pts], 255)  # Заливаем область белым

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

    for result in results:
        for box in result.boxes:
            x, y, w, h = map(int, box.xywh[0])  # Координаты бокса
            conf = box.conf[0].item()  # Уверенность модели
            cls = int(box.cls[0].item())  # Класс объекта

            if conf > 0.5:  # Фильтр по уверенности
                # Рисуем рамку вокруг обнаруженного объекта
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, f"Car {conf:.2f}", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Рисуем красную рамку вокруг зоны интереса
    cv2.polylines(frame, [pts], isClosed=True, color=(0, 0, 255), thickness=3)

    # Записываем обработанный кадр в файл
    out.write(frame)

# Освобождение ресурсов
cap.release()
out.release()
cv2.destroyAllWindows()