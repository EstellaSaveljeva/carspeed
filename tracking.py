import cv2
import numpy as np
from ultralytics import YOLO
import torch
from deep_sort_realtime.deepsort_tracker import DeepSort

# Load YOLO model
def load_model(model_path="", use_gpu=True):
    model = YOLO(model_path)
    if use_gpu and torch.cuda.is_available():
        model.to("cuda")
    else:
        model.to("cpu")
    return model

# Initialize DeepSort tracker
def initialize_tracker(fps):
    # max_age is the maximum number of frames to keep a track alive without detection
    return DeepSort(max_age=fps*2)

# Get detections in the region of interest
def get_detections_in_roi(results, polygon_pts):
    detections = []
    for result in results:
        for box in result.boxes:
            # Get bounding box coordinates and class
            x_min, y_min, x_max, y_max = map(int, box.xyxy[0])
            conf = box.conf[0].item()
            cls = int(box.cls[0].item())

            if cls != 0:  # Only cars
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


