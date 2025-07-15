import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.perception.audio import detect_birds
from utils.audio_preprocessor import preprocess_audio

DEBUG = True

def main():
    files = preprocess_audio("test_assets", debug=DEBUG)
    for path in files:
        print(f"\nAnalyzing {path}")
        detections = detect_birds(path, debug=DEBUG)
        if detections:
            top = max(detections, key=lambda d: d["confidence"])
            log_detection(path, top)

if __name__ == "__main__":
    main()
