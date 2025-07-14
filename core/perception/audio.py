from utils.birdnet_wrapper import detect_birds

detections = detect_birds("latest.wav", lat=40.0, lon=-111.8, debug=False)
if detections:
    top = max(detections, key=lambda d: d['confidence'])
    print("Top species:", top['common_name'], round(top['confidence'], 2))
