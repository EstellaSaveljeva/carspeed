import cv2
import numpy as np

# load video
def setup_video(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise IOError("Error: cannot open video.")
    return cap

# load video parameters
def get_video_params(cap):
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    return width, height, fps

# calculate scaling for the video
def calculate_scaling(original_width, original_height, screen_width=1280, screen_height=720):
    scale = min(screen_width / original_width, screen_height / original_height)
    new_width = int(original_width * scale)
    new_height = int(original_height * scale)
    return scale, new_width, new_height

# create video writer 
def create_video_writer(output_path, fourcc_str, fps, size):
    fourcc = cv2.VideoWriter_fourcc(*fourcc_str)
    return cv2.VideoWriter(output_path, fourcc, fps, size)

# draw initial frame with ROI and speed lines
def draw_initial_frame(frame, zone_pts, top_line_pts, bottom_line_pts, line_thickness):
    frame_copy = frame.copy()
    cv2.polylines(frame_copy, [zone_pts], isClosed=True, color=(0, 0, 255), thickness=3)
    cv2.line(frame_copy, top_line_pts[0], top_line_pts[1], (255, 0, 0), line_thickness)
    cv2.line(frame_copy, bottom_line_pts[0], bottom_line_pts[1], (255, 0, 0), line_thickness)
    return frame_copy
