
def update_vehicle_timestamp(vehicle_timestamp, cx, cy, frame_time, top_line, bottom_line, is_above_line):
    if vehicle_timestamp["done"]:
        return

    # if there is no previous position, we get the current one and exit
    # remember the current position
    if "prev_above_top" not in vehicle_timestamp or "prev_above_bottom" not in vehicle_timestamp:
        vehicle_timestamp["prev_above_top"] = is_above_line(cx, cy, *top_line)
        vehicle_timestamp["prev_above_bottom"] = is_above_line(cx, cy, *bottom_line)
        return
    # if there is a previous position, we check if the current position is above or below the lines
    current_above_top = is_above_line(cx, cy, *top_line)
    current_above_bottom = is_above_line(cx, cy, *bottom_line)
    # get the direction of the vehicle
    direction = vehicle_timestamp.get("direction", None)

    # if there is no direction, we determine it based on the previous and current positions
    if direction is None:
        # if the vehicle was above the top line and is now below it, it is going down
        if vehicle_timestamp["prev_above_top"] and not current_above_top:
            direction = "down"
        # if the vehicle was below the bottom line and is now above it, it is going up 
        elif not vehicle_timestamp["prev_above_bottom"] and current_above_bottom:
            direction = "up"
        if direction:
            vehicle_timestamp["direction"] = direction

    # if the vehicle is going down, code checks if it has passed the top line and is now below it
    if direction == "down":
        # if the vehicle was above the top line and is now below it, set the start time
        if vehicle_timestamp["start"] is None and vehicle_timestamp["prev_above_top"] and not current_above_top:
            vehicle_timestamp["start"] = frame_time
        # if the vehicle was above the bottom line and is now bellow it, set the end time 
        if vehicle_timestamp["start"] is not None and vehicle_timestamp["end"] is None and vehicle_timestamp["prev_above_bottom"] and not current_above_bottom:
            vehicle_timestamp["end"] = frame_time
            vehicle_timestamp["done"] = True

    # if the vehicle is going up, code checks if it has passed the bottom line and is now above it
    elif direction == "up":
        # if the vehicle was below the bottom line and is now above it, set the start time
        if vehicle_timestamp["start"] is None and not vehicle_timestamp["prev_above_bottom"] and current_above_bottom:
            vehicle_timestamp["start"] = frame_time
        # if the vehicle was below the top line and is now above it, set the end time
        if vehicle_timestamp["start"] is not None and vehicle_timestamp["end"] is None and not vehicle_timestamp["prev_above_top"] and current_above_top:
            vehicle_timestamp["end"] = frame_time
            vehicle_timestamp["done"] = True

    # update the state for the next frame
    vehicle_timestamp["prev_above_top"] = current_above_top
    vehicle_timestamp["prev_above_bottom"] = current_above_bottom


def compute_speed_line(vehicle_timestamp, distance_m):

    # Calculates vehicle speed based on the time difference between passing the upper and lower lines.
    # Check if there are enough data to calculate speed
    if vehicle_timestamp["start"] is not None and vehicle_timestamp["end"] is not None:
        travel_time = vehicle_timestamp["end"] - vehicle_timestamp["start"]
        # If the vehicle moved in the forward direction (from top to bottom)
        if travel_time > 0:
            speed_line = (distance_m / travel_time) * 3.6  # convert to km/h
            return speed_line
        # If the vehicle moved in the reverse direction (from bottom to top)
        elif travel_time < 0:
            travel_time = abs(travel_time)
            speed_line = (distance_m / travel_time) * 3.6
            return speed_line
    return None