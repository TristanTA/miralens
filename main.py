import sys, os
import argparse
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.birdnet_wrapper import detect_birds
from utils.audio_preprocessor import preprocess_audio
from utils.eco_lookup import load_all_eco_packs, get_bird_info
from utils.logger import log_detection
from utils.video_preprocessor import run_video

DEBUG = True
eco_data = load_all_eco_packs(debug=DEBUG)

def run_audio_pipeline():
    files = preprocess_audio("test_assets", debug=DEBUG)
    for path in files:
        print(f"\nAnalyzing {path}")
        detections = detect_birds(path, debug=DEBUG)
        if detections:
            top = max(detections, key=lambda d: d["confidence"])
            log_detection(path, top)
            info = get_bird_info(top["common_name"], eco_data, region="utah_birds", debug=DEBUG)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["audio", "vision", "all"], default="all")
    parser.add_argument("--vision_mode", choices=["file", "live"], default="file")
    parser.add_argument("--vision_source", default="test_assets/")
    args = parser.parse_args()

    if args.mode in ("audio", "all"):
        run_audio_pipeline()

    if args.mode in ("vision", "all"):
        run_video(mode=args.vision_mode, source_path=args.vision_source)

if __name__ == "__main__":
    main()
