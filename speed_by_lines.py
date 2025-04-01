# def update_vehicle_timestamp(vehicle_timestamp, cx, cy, frame_time, top_line, bottom_line, is_above_line):

#     #     Updates the timestamps for a vehicle based on its position relative to the top and bottom lines.

#     # Parameters:
#     #     vehicle_timestamp (dict): Dictionary with the keys “start”, “end”, “last_position”, and “done”.
#     #     cx, cy (int): The coordinates of the center of the vehicle.
#     #     frame_time (float): The time of the current frame.
#     #     top_line (tuple): Coordinates (x1, y1, x2, y2) of the top line.
#     #     bottom_line (tuple): Coordinates (x1, y1, x2, y2) of the bottom line.
#     #     is_above_line (function): Function to check if a point is above the line.
    
#     # If the computation for this vehicle is already complete, exit.
#     # If the computation for this vehicle is already complete, exit.
#     if vehicle_timestamp["done"]:
#         return

#     # Determine the direction of movement if it is not already set.
#     # Compare the current vertical position with the last recorded position.
#     if "direction" not in vehicle_timestamp:
#         # If no previous position is recorded, set the current position and exit.
#         if vehicle_timestamp["last_position"] is None:
#             vehicle_timestamp["last_position"] = cy
#             return
#         # Determine direction based on comparison with the last position.
#         if cy > vehicle_timestamp["last_position"]:
#             vehicle_timestamp["direction"] = "down"  # Moving downwards (e.g., towards the camera)
#         elif cy < vehicle_timestamp["last_position"]:
#             vehicle_timestamp["direction"] = "up"    # Moving upwards (e.g., away from the camera)
#         else:
#             # If the position hasn't changed, we cannot determine direction yet; return early.
#             return
#         # Update the last recorded vertical position.
#         vehicle_timestamp["last_position"] = cy

#     # Retrieve the movement direction.
#     direction = vehicle_timestamp["direction"]

#     if direction == "down":
#         # When the vehicle is moving downwards:
#         # Set the start time when the vehicle is above the top line.
#         if vehicle_timestamp["start"] is None and is_above_line(cx, cy, *top_line):
#             vehicle_timestamp["start"] = frame_time
#         # Set the end time when the vehicle is below the bottom line.
#         if vehicle_timestamp["end"] is None and not is_above_line(cx, cy, *bottom_line):
#             vehicle_timestamp["end"] = frame_time
#             vehicle_timestamp["done"] = True
#     elif direction == "up":
#         # When the vehicle is moving upwards:
#         # Set the start time when the vehicle is below the bottom line.
#         if vehicle_timestamp["start"] is None and not is_above_line(cx, cy, *bottom_line):
#             vehicle_timestamp["start"] = frame_time
#         # Set the end time when the vehicle is above the top line.
#         if vehicle_timestamp["end"] is None and is_above_line(cx, cy, *top_line):
#             vehicle_timestamp["end"] = frame_time
#             vehicle_timestamp["done"] = True

#     # Update the last recorded vertical position.
#     vehicle_timestamp["last_position"] = cy
def update_vehicle_timestamp(vehicle_timestamp, cx, cy, frame_time, top_line, bottom_line, is_above_line):
    if vehicle_timestamp["done"]:
        return

    # if there is no previous position, we get the current one and exit
    # remember the current position
    if "prev_above_top" not in vehicle_timestamp or "prev_above_bottom" not in vehicle_timestamp:
        vehicle_timestamp["prev_above_top"] = is_above_line(cx, cy, *top_line)
        vehicle_timestamp["prev_above_bottom"] = is_above_line(cx, cy, *bottom_line)
        return

    current_above_top = is_above_line(cx, cy, *top_line)
    current_above_bottom = is_above_line(cx, cy, *bottom_line)

    direction = vehicle_timestamp.get("direction", None)

    # if there is no direction, we determine it based on the previous and current positions
    if direction is None:
        if vehicle_timestamp["prev_above_top"] and not current_above_top:
            direction = "down"
        elif not vehicle_timestamp["prev_above_bottom"] and current_above_bottom:
            direction = "up"
        if direction:
            vehicle_timestamp["direction"] = direction

  
    # direction down, 
    if direction == "down":
        if vehicle_timestamp["start"] is None and vehicle_timestamp["prev_above_top"] and not current_above_top:
            vehicle_timestamp["start"] = frame_time
        if vehicle_timestamp["start"] is not None and vehicle_timestamp["end"] is None and vehicle_timestamp["prev_above_bottom"] and not current_above_bottom:
            vehicle_timestamp["end"] = frame_time
            vehicle_timestamp["done"] = True

    # direction up,
    elif direction == "up":
        if vehicle_timestamp["start"] is None and not vehicle_timestamp["prev_above_bottom"] and current_above_bottom:
            vehicle_timestamp["start"] = frame_time
        if vehicle_timestamp["start"] is not None and vehicle_timestamp["end"] is None and not vehicle_timestamp["prev_above_top"] and current_above_top:
            vehicle_timestamp["end"] = frame_time
            vehicle_timestamp["done"] = True

    # update the state for the next frame
    vehicle_timestamp["prev_above_top"] = current_above_top
    vehicle_timestamp["prev_above_bottom"] = current_above_bottom


def compute_speed_line(vehicle_timestamp, distance_m):

    # Calculates vehicle speed based on the time difference between passing the upper and lower lines.
    # Parameters:
    #     vehicle_timestamp (dict): Dictionary with “start” and “end” timestamps.
    #     distance_m (float): The actual distance between lines in meters.
    # Returns:
    #     Float or None: Speed in km/h or None if there is not enough data.

    if vehicle_timestamp["start"] is not None and vehicle_timestamp["end"] is not None:
        travel_time = vehicle_timestamp["end"] - vehicle_timestamp["start"]
        if travel_time > 0:
            speed_line = (distance_m / travel_time) * 3.6  # convert to km/h
            return speed_line
        elif travel_time < 0:
            # If vehicle moved in reverse direction (from bottom to top)
            travel_time = abs(travel_time)
            speed_line = (distance_m / travel_time) * 3.6
            return speed_line
    return None


# def update_vehicle_timestamp(vehicle_data, cx, cy, frame_time, top_line, bottom_line, is_above_fn):
#     """
#     Обновляет временные метки входа/выхода автомобиля при пересечении линий.

#     :param vehicle_data: словарь для конкретного автомобиля: {start, end, last_position, done}
#     :param cx, cy: текущая координата объекта (центр нижней рамки)
#     :param frame_time: текущее время в секундах
#     :param top_line, bottom_line: координаты линий (x1, y1, x2, y2)
#     :param is_above_fn: функция для проверки, выше ли точка линии
#     """
#     top_above = is_above_fn(cx, cy, *top_line)
#     bottom_above = is_above_fn(cx, cy, *bottom_line)
#     last = vehicle_data["last_position"]

#     if last is not None:
#         last_top = is_above_fn(*last, *top_line)
#         last_bottom = is_above_fn(*last, *bottom_line)

#         # Направление: вперёд (снизу вверх)
#         if last_bottom and not bottom_above and vehicle_data["start"] is None:
#             vehicle_data["start"] = frame_time
#         elif last_top and not top_above and vehicle_data["end"] is None:
#             vehicle_data["end"] = frame_time
#             vehicle_data["done"] = True

#         # Направление: назад (сверху вниз)
#         elif not last_top and top_above and vehicle_data["start"] is None:
#             vehicle_data["start"] = frame_time
#         elif not last_bottom and bottom_above and vehicle_data["end"] is None:
#             vehicle_data["end"] = frame_time
#             vehicle_data["done"] = True

#     vehicle_data["last_position"] = (cx, cy)

# def compute_speed_line(vehicle_data, distance_m):
#     """
#     Вычисляет скорость автомобиля на основе времён пересечения линий.

#     :param vehicle_data: словарь с метками времени
#     :param distance_m: расстояние между линиями (в метрах)
#     :return: скорость в км/ч или None
#     """
#     if vehicle_data["start"] is not None and vehicle_data["end"] is not None:
#         delta_time = vehicle_data["end"] - vehicle_data["start"]
#         if delta_time > 0:
#             speed_mps = distance_m / delta_time
#             return speed_mps * 3.6
#     return None

