import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.birdnet_wrapper import detect_birds
from utils.audio_preprocessor import preprocess_audio
from utils.eco_lookup import load_all_eco_packs, get_bird_info
from utils.logger import log_detection

DEBUG = True
eco_data = load_all_eco_packs(debug=DEBUG)

def main():
    files = preprocess_audio("test_assets", debug=DEBUG)
    for path in files:
        print(f"\nAnalyzing {path}")
        detections = detect_birds(path, debug=DEBUG)
        if detections:
            top = max(detections, key=lambda d: d["confidence"])
            log_detection(path, top)
            info = get_bird_info(top["common_name"], eco_data, region="utah_birds", debug=DEBUG)

if __name__ == "__main__":
    main()
