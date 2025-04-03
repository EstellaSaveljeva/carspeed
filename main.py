import cv2
import numpy as np
from collections import defaultdict, deque
import supervision as sv

from coordinates import get_coordinates
from speed_by_shift import compute_speed_shift
from speed_by_lines import update_vehicle_timestamp, compute_speed_line
from video import (
    setup_video, get_video_params, calculate_scaling,
    create_video_writer, draw_initial_frame
)
from tracking import (
    load_model, initialize_tracker,
    get_detections_in_roi, transform_point,
    moving_average_position
)

# Add this at the beginning of the file to define the output file path
output_txt_path = "yolo_output.txt"

# Clear the file at the start of the program
with open(output_txt_path, "w") as f:
    f.write("")


# def is_above_line(cx, cy, x1, y1, x2, y2):
#     if x1 == x2:
#         return cx <= x1
#     m = (y2 - y1) / (x2 - x1)
#     b = y1 - m * x1
#     y_on_line = m * cx + b
#     return cy <= y_on_line

def is_above_line(cx, cy, x1, y1, x2, y2):
   
    # Vector AB
    ABx = x2 - x1 #blue line
    ABy = y2 - y1
    # Vector AC
    ACx = cx - x1 # line to car vector
    ACy = cy - y1

    cross = ABx * ACy - ABy * ACx
    # if result <0, point is above the line
    return cross < 0


def main():
    model = load_model("yolo11m.pt")
    video_path = "80kmh_ropazi.mov"
    cap = setup_video(video_path)

    try:
        (x1, y1, x2, y2, x3, y3, x4, y4, distance_m,
         blue_x1_top, blue_y1_top, blue_x2_top, blue_y2_top,
         blue_x1_bottom, blue_y1_bottom, blue_x2_bottom, blue_y2_bottom,
         blue_line_thickness) = get_coordinates(video_path)
    except ValueError as e:
        print(e)
        cap.release()
        return

    ret, frame = cap.read()
    if not ret:
        print("Error: cannot read frame.")
        cap.release()
        return

    frame_width, frame_height, fps = get_video_params(cap)
    scale, new_width, new_height = calculate_scaling(frame_width, frame_height)
    output_path = "output.mp4"
    out = create_video_writer(output_path, 'mp4v', fps, (frame_width, frame_height))

    # Scale coordinates
    x1, x2, x3, x4 = int(x1 * scale), int(x2 * scale), int(x3 * scale), int(x4 * scale)
    y1, y2, y3, y4 = int(y1 * scale), int(y2 * scale), int(y3 * scale), int(y4 * scale)
    blue_x1_top, blue_x2_top = int(blue_x1_top * scale), int(blue_x2_top * scale)
    blue_y1_top, blue_y2_top = int(blue_y1_top * scale), int(blue_y2_top * scale)
    blue_x1_bottom, blue_x2_bottom = int(blue_x1_bottom * scale), int(blue_x2_bottom * scale)
    blue_y1_bottom, blue_y2_bottom = int(blue_y1_bottom * scale), int(blue_y2_bottom * scale)

    # Perspective transformation matrix
    src = np.array([
        [blue_x1_top, blue_y1_top],
        [blue_x2_top, blue_y2_top],
        [blue_x1_bottom, blue_y1_bottom],
        [blue_x2_bottom, blue_y2_bottom]
    ], dtype=np.float32)

    dst = np.array([
        [0, 0],
        [6, 0],
        [0, distance_m],
        [6, distance_m]
    ], dtype=np.float32)

    matrix = cv2.getPerspectiveTransform(src, dst)
    pts = np.array([[x1, y1], [x2, y2], [x3, y3], [x4, y4]], np.int32)

    # Show first frame with ROI and speed lines
    frame_with_lines = draw_initial_frame(
        frame,
        pts,
        ((blue_x1_top, blue_y1_top), (blue_x2_top, blue_y2_top)),
        ((blue_x1_bottom, blue_y1_bottom), (blue_x2_bottom, blue_y2_bottom)),
        blue_line_thickness
    )
    resized_frame = cv2.resize(frame_with_lines, (new_width, new_height))
    cv2.imshow("First frame", resized_frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    box_annotator = sv.BoxAnnotator(color=sv.Color.GREEN, thickness=2)
    label_annotator = sv.LabelAnnotator(text_color=sv.Color.BLACK)

    tracker = initialize_tracker()
    vehicle_timestamps = {}
    vehicle_speeds_shift = defaultdict(list)
    
    real_y_history = defaultdict(lambda: deque(maxlen=int(fps)))
    

    top_line = (blue_x1_top, blue_y1_top, blue_x2_top, blue_y2_top)
    bottom_line = (blue_x1_bottom, blue_y1_bottom, blue_x2_bottom, blue_y2_bottom)

    frame_count = 0
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_time = frame_count / fps
        frame_count += 1

        results = model(frame)
        boxes_for_tracking = get_detections_in_roi(results, pts)
        tracks = tracker.update_tracks(boxes_for_tracking, frame=frame)

        tracked_boxes = []
        confidences = []
        class_ids = []
        labels = []

        for track in tracks:
            if not track.is_confirmed():
                continue

            track_id = track.track_id
            l, t, r, b = map(int, track.to_ltrb())
            cx = (l + r) // 2 # Center x-coordinate
            cy = b  # Bottom y-coordinate

            # Вычисление результатов для проверки пересечения
            above_top = is_above_line(cx, cy, *top_line)
            above_bottom = is_above_line(cx, cy, *bottom_line)

            # Рисуем точку в центре (cx, cy)
            cv2.circle(frame, (cx, cy), radius=5, color=(0, 255, 255), thickness=-1)  # Жёлтая точка

            # Выводим текстовые метки рядом с точкой
            debug_text_top = f"Above top: {above_top}"
            debug_text_bottom = f"Above bottom: {above_bottom}"
            cv2.putText(frame, debug_text_top, (cx + 10, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.putText(frame, debug_text_bottom, (cx + 10, cy - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Write YOLO output to the text file
            with open(output_txt_path, "a") as f:
                f.write(f"Frame {frame_count}, Track ID {track_id}, BBox: ({l}, {t}, {r}, {b}), Confidence: 1.0, Class ID: 2\n")

            # Transform pixel coordinates to real-world coordinates
            real_point = transform_point(cx, cy, matrix)
            real_y_history[track_id].append(real_point)

            # Calculate the moving average of the recent positions for smoother coordinates
            moving_avg = moving_average_position(real_y_history[track_id], smooth_size=10)
            if moving_avg is not None:
                avg_cx, avg_cy = moving_avg
            else:
                avg_cx, avg_cy = cx, cy  # Fallback to current coordinates if insufficient data

            # Update timestamps for line-based speed estimation
            if track_id not in vehicle_timestamps:
                vehicle_timestamps[track_id] = {"start": None, "end": None, "last_position": None, "done": False}


            if not vehicle_timestamps[track_id]["done"]:
                update_vehicle_timestamp(vehicle_timestamps[track_id], cx, cy, frame_time, top_line, bottom_line, is_above_line)

            
            # Estimate speed using the shift method (only between the two blue lines)
            speed_transformed = None
            if is_above_line(cx, cy, *bottom_line) and not is_above_line(cx, cy, *top_line):
                last_speed = vehicle_speeds_shift[track_id][-1] if vehicle_speeds_shift[track_id] else None
                speed_transformed = compute_speed_shift(real_y_history[track_id], fps, last_speed)
                if speed_transformed is not None:
                    vehicle_speeds_shift[track_id].append(speed_transformed)
            # Предположим, что real_position_history хранит реальные координаты или пиксельные координаты объекта.



            # Use the smoothed coordinates to check if the vehicle is between the two blue lines
            if is_above_line(avg_cx, avg_cy, *bottom_line) and not is_above_line(avg_cx, avg_cy, *top_line):
                last_speed = vehicle_speeds_shift[track_id][-1] if vehicle_speeds_shift[track_id] else None
                speed_transformed = compute_speed_shift(real_y_history[track_id], fps, last_speed)
                if speed_transformed is not None:
                    vehicle_speeds_shift[track_id].append(speed_transformed)

            if not is_above_line(avg_cx, avg_cy, *top_line):
                print(f"Car {track_id} is under the top line.")


            # Compose label
            label_parts = []
            if speed_transformed is not None:
                label_parts.append(f"T: {speed_transformed:.1f} km/h")
            speed_line = compute_speed_line(vehicle_timestamps[track_id], distance_m)
            if speed_line is not None:
                label_parts.append(f"L: {speed_line:.1f} km/h")
            if not label_parts:
                label_parts.append("Tracking...")

            labels.append(" | ".join(label_parts))
            tracked_boxes.append([l, t, r, b])
            confidences.append(1.0)
            class_ids.append(2)

        if tracked_boxes:
            detections_sv = sv.Detections(
                xyxy=np.array(tracked_boxes),
                confidence=np.array(confidences),
                class_id=np.array(class_ids)
            )
            frame = box_annotator.annotate(scene=frame, detections=detections_sv)
            frame = label_annotator.annotate(scene=frame, detections=detections_sv, labels=labels)

        # Draw speed lines and ROI
        cv2.line(frame, (blue_x1_top, blue_y1_top), (blue_x2_top, blue_y2_top), (255, 0, 0), blue_line_thickness)
        cv2.line(frame, (blue_x1_bottom, blue_y1_bottom), (blue_x2_bottom, blue_y2_bottom), (255, 0, 0), blue_line_thickness)
        cv2.polylines(frame, [pts], isClosed=True, color=(0, 0, 255), thickness=2)

        out.write(frame)

    # Output final average speeds (line-based)
    print("\nFinal average speed (lines method):")
    for vehicle_id, times in vehicle_timestamps.items():
        speed_kmh = compute_speed_line(times, distance_m)
        if speed_kmh is not None:
            print(f"Car {vehicle_id}: speed: {speed_kmh:.2f} km/h")

    # Output final average speeds (shift method)
    print("\nFinal average speed (shift method):")
    for vehicle_id, speeds in vehicle_speeds_shift.items():
        if speeds:
            avg_speed_shift = sum(speeds) / len(speeds)
            print(f"Car {vehicle_id}: speed: {avg_speed_shift:.2f} km/h")

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print(f"Video saved as {output_path}")


if __name__ == "__main__":
    main()
