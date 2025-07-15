from birdnetlib import Recording
from birdnetlib.analyzer_lite import LiteAnalyzer
import os

# Custom model and label paths (in your repo)
MODEL_PATH = os.path.join("models", "birdnet_lite", "BirdNET_6K_GLOBAL_MODEL.tflite")
LABEL_PATH = os.path.join("models", "birdnet_lite", "labels.txt")

# Patch the paths before creating the analyzer
LiteAnalyzer.MODEL_PATH = MODEL_PATH
LiteAnalyzer.LABEL_PATH = LABEL_PATH

def detect_birds(audio_path, lat=None, lon=None, date=None, min_conf=0.25, debug=False):
    if debug:
        print(f"[DEBUG] Using local BirdNET Lite model:")
        print(f"[DEBUG] Model: {LiteAnalyzer.MODEL_PATH}")
        print(f"[DEBUG] Labels: {LiteAnalyzer.LABEL_PATH}")

    analyzer = LiteAnalyzer()

    if debug:
        print(f"[DEBUG] Analyzing file: {audio_path}")
        print(f"[DEBUG] Lat: {lat}, Lon: {lon}, Min Conf: {min_conf}")

    rec = Recording(analyzer, audio_path, lat=lat or 0,
                    lon=lon or 0, date=date, min_conf=min_conf)
    rec.analyze()

    if debug:
        print(f"[DEBUG] Detections:")
        for d in rec.detections:
            print(f"  {d['start_time']}s – {d['end_time']}s: "
                  f"{d['common_name']} ({d['confidence']:.2f})")

    return rec.detections
