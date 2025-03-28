def update_vehicle_timestamp(vehicle_timestamp, cx, cy, frame_time, top_line, bottom_line, is_above_line):

    #     Updates the timestamps for a vehicle based on its position relative to the top and bottom lines.

    # Parameters:
    #     vehicle_timestamp (dict): Dictionary with the keys “start”, “end”, “last_position”, and “done”.
    #     cx, cy (int): The coordinates of the center of the vehicle.
    #     frame_time (float): The time of the current frame.
    #     top_line (tuple): Coordinates (x1, y1, x2, y2) of the top line.
    #     bottom_line (tuple): Coordinates (x1, y1, x2, y2) of the bottom line.
    #     is_above_line (function): Function to check if a point is above the line.
    
    if vehicle_timestamp["start"] is None and is_above_line(cx, cy, *top_line):
        vehicle_timestamp["start"] = frame_time

    if vehicle_timestamp["end"] is None and not is_above_line(cx, cy, *bottom_line):
        vehicle_timestamp["end"] = frame_time
        vehicle_timestamp["done"] = True

    vehicle_timestamp["last_position"] = cy

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
    return None
