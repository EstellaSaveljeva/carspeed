import numpy as np

def compute_speed_shift(real_y_history, fps, last_speed=None, y_min=0, y_max=None):

    # Calculates speed based on point history in real coordinates.
    #     real_y_history (iterable): List or deque with points (x, y) in real coordinates.
    #     fps (int): Video frame rate.
    #     last_speed (float, optional): Previous speed to limit sudden jumps.
    # Returns:
    #     Float or None: Speed in km/h or None if there is not enough data.

    # Check if there are enough points to calculate speed
    # If there are less than 2 points, we cannot calculate speed.
    if len(real_y_history) < 2:
        return None

    # Calculate distance and time between points
    points = np.array(real_y_history, dtype=np.float32)
    distances = np.linalg.norm(np.diff(points, axis=0), axis=1)
    total_distance = np.sum(distances)
    time_delta = len(real_y_history) / fps
    # Calculate speed in km/h
    if time_delta > 0 and total_distance > 0.1:
        # Get last known y-position
        latest_y = real_y_history[-1][1]

        # Normalize position along the road
        y_norm = (latest_y - y_min) / (y_max - y_min)
        y_norm = np.clip(y_norm, 0.0, 1.0)
        
        k=0.5 # compensation factor for perspective
        # Perspective compensation factor
        compensation = 1 + (0.5 - y_norm) * k  

        # Calculate speed with compensation
        speed_transformed = (total_distance / time_delta) * 3.6 * compensation

        # Prevent large jumps
        if last_speed is not None and abs(speed_transformed - last_speed) > last_speed * 0.1:
            speed_transformed = last_speed

        return speed_transformed
    return None
 
