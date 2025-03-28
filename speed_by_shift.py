import numpy as np

def compute_speed_shift(real_y_history, fps, last_speed=None):

    # Calculates velocity based on point history in real coordinates.
    # Parameters:
    #     real_y_history (iterable): List or deque with points (x, y) in real coordinates.
    #     fps (int): Video frame rate.
    #     last_speed (float, optional): Previous speed to limit sudden jumps.
    # Returns:
    #     Float or None: Speed in km/h or None if there is not enough data.

    if len(real_y_history) < 2:
        return None

    points = np.array(real_y_history, dtype=np.float32)
    distances = np.linalg.norm(np.diff(points, axis=0), axis=1)
    total_distance = np.sum(distances)
    time_delta = len(real_y_history) / fps

    if time_delta > 0 and total_distance > 0.1:
        speed_transformed = (total_distance / time_delta) * 3.6  # convert to km/h
        
        # Limit sudden changes in speed (no more than 30% change)
        if last_speed is not None and abs(speed_transformed - last_speed) > last_speed * 0.3:
            speed_transformed = last_speed
        
        return speed_transformed
    return None
