def update_vehicle_timestamp(vehicle_timestamp, cx, cy, frame_time, top_line, bottom_line, is_above_line):
    """
    Обновляет временные метки для транспортного средства, основываясь на его положении относительно верхней и нижней линий.

    Parameters:
        vehicle_timestamp (dict): Словарь с ключами "start", "end", "last_position" и "done".
        cx, cy (int): Координаты центра транспортного средства.
        frame_time (float): Время текущего кадра.
        top_line (tuple): Координаты (x1, y1, x2, y2) верхней линии.
        bottom_line (tuple): Координаты (x1, y1, x2, y2) нижней линии.
        is_above_line (function): Функция для проверки, находится ли точка выше линии.
    """
    if vehicle_timestamp["start"] is None and is_above_line(cx, cy, *top_line):
        vehicle_timestamp["start"] = frame_time

    if vehicle_timestamp["end"] is None and not is_above_line(cx, cy, *bottom_line):
        vehicle_timestamp["end"] = frame_time
        vehicle_timestamp["done"] = True

    vehicle_timestamp["last_position"] = cy

def compute_speed_line(vehicle_timestamp, distance_m):
    """
    Вычисляет скорость транспортного средства на основе разницы времени между прохождением верхней и нижней линий.

    Parameters:
        vehicle_timestamp (dict): Словарь с временными метками "start" и "end".
        distance_m (float): Фактическое расстояние между линиями в метрах.

    Returns:
        float или None: Скорость в км/ч или None, если данных недостаточно.
    """
    if vehicle_timestamp["start"] is not None and vehicle_timestamp["end"] is not None:
        travel_time = vehicle_timestamp["end"] - vehicle_timestamp["start"]
        if travel_time > 0:
            speed_line = (distance_m / travel_time) * 3.6  # перевод в км/ч
            return speed_line
    return None
