import cv2
from ultralytics import YOLO

model = YOLO("yolov8n.pt")

def detect_objects(frame):
    results = model(frame)[0]
    detections = []
    for box in results.boxes:
        label = results.names[int(box.cls)]
        confidence = float(box.conf)
        bbox = box.xyxy[0].tolist()
        x, y, x2, y2 = map(int, bbox)
        detections.append((label, confidence, [x, y, x2 - x, y2 - y]))
    return detections

def process_video(video_path, fps=1.0):
    """
    Processes video at a fixed sampling rate, returns list of detection dicts.
    """
    results = []
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Could not open video file: {video_path}")
    
    video_fps = cap.get(cv2.CAP_PROP_FPS)
    if video_fps <= 0:
        raise ValueError("Invalid FPS detected in video file.")
    frame_interval = int(video_fps / fps)
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frame_interval == 0:
            timestamp = frame_count / video_fps
            detections = detect_objects(frame)
            for label, conf, bbox in detections:
                results.append({
                    "timestamp": round(timestamp, 2),
                    "source": "video",
                    "raw_label": label,
                    "confidence": conf,
                    "location": bbox
                })

        frame_count += 1

    cap.release()
    return results
