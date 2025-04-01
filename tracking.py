import cv2
import numpy as np
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort

# Load YOLO model
def load_model(model_path="yolo11x.pt"):
    return YOLO(model_path)

# Initialize DeepSort tracker
def initialize_tracker():
    return DeepSort(max_age=30)

# Get detections in the region of interest
def get_detections_in_roi(results, polygon_pts):
    detections = []
    for result in results:
        for box in result.boxes:
            x_min, y_min, x_max, y_max = map(int, box.xyxy[0])
            conf = box.conf[0].item()
            cls = int(box.cls[0].item())

            if cls != 2:  # Only cars
                continue

            # Calculate center of the bounding box
            cx = (x_min + x_max) // 2
            cy = (y_min + y_max) // 2

            # Check if the center is inside the polygon
            if not cv2.pointPolygonTest(polygon_pts, (cx, cy), False) >= 0:
                continue

            # Add the detection
            detections.append(([x_min, y_min, x_max - x_min, y_max - y_min], conf, 'car'))
    return detections

# Transform pixel coordinates to real-world coordinates
def transform_point(cx, cy, matrix):
    point = np.array([[[cx, cy]]], dtype=np.float32)
    return cv2.perspectiveTransform(point, matrix)[0][0]

def moving_average_position(position_history, smooth_size=10):
    # If less frames are accumulated than required for the window, we use the existing ones
    window = list(position_history)[-smooth_size:] if len(position_history) >= smooth_size else list(position_history)
    avg_x = sum(pos[0] for pos in window) / len(window)
    avg_y = sum(pos[1] for pos in window) / len(window)
    return avg_x, avg_y
