import sys, os
import argparse
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.eco_lookup import load_all_eco_packs
from utils.main_processor import process_media

DEBUG = False
eco_data = load_all_eco_packs(debug=DEBUG)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["audio", "vision", "all"], default="all")
    parser.add_argument("--vision_mode", choices=["file", "live"], default="file")  # kept for future
    parser.add_argument("--source_path", default="test_assets/forest_clip.mp4")
    args = parser.parse_args()

    detections = process_media(input_path=args.source_path)
    for d in detections:
        print(d)

if __name__ == "__main__":
    main()
