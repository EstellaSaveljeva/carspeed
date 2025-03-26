import numpy as np

def compute_speed_shift(real_y_history, fps, last_speed=None):
    """
    Вычисляет скорость на основе истории точек в реальных координатах.

    Parameters:
        real_y_history (iterable): Список или deque с точками (x, y) в реальных координатах.
        fps (int): Частота кадров видео.
        last_speed (float, optional): Предыдущая скорость для ограничения резких скачков.

    Returns:
        float или None: Скорость в км/ч или None, если данных недостаточно.
    """
    if len(real_y_history) < 2:
        return None

    points = np.array(real_y_history, dtype=np.float32)
    distances = np.linalg.norm(np.diff(points, axis=0), axis=1)
    total_distance = np.sum(distances)
    time_delta = len(real_y_history) / fps

    if time_delta > 0 and total_distance > 0.1:
        speed_transformed = (total_distance / time_delta) * 3.6  # перевод в км/ч
        
        # Ограничение резких скачков скорости (не более 30% изменения)
        if last_speed is not None and abs(speed_transformed - last_speed) > last_speed * 0.3:
            speed_transformed = last_speed
        
        return speed_transformed
    return None
