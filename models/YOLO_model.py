from ultralytics import YOLO 
import cv2

model = YOLO("yolov8n.pt") 

def detect_objects(frame):
    results = model(frame)[0]
    detections = []

    for box in results.boxes:
        cls_id = int(box.cls[0])
        label = model.names[cls_id]
        conf = float(box.conf[0])
        detections.append((label, conf))

    return detections
