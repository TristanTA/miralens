import cv2
import sys
import os
import glob
from models.YOLO_model import detect_objects

NATURE_CLASSES = {
    "bird", "tree", "flower", "plant", "mammal", "insect", "reptile", "fish", "butterfly"
}

def run_video(mode="file", source_path="test_assets/"):
    if mode == "live":
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            print("Error opening webcam")
            sys.exit(1)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            results = detect_objects(frame)

            for label, conf in results:
                if label in NATURE_CLASSES:
                    print(f"Detected: {label} ({conf:.2f})")

            cv2.imshow("Live Feed", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    else:
        video_files = sorted(glob.glob(os.path.join(source_path, "*.mp4")))
        if not video_files:
            print(f"No .mp4 files found in {source_path}")
            sys.exit(1)

        for video_path in video_files:
            print(f"\n--- Processing: {video_path} ---")
            cap = cv2.VideoCapture(video_path)

            if not cap.isOpened():
                print(f"Error opening video file: {video_path}")
                continue

            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                results = detect_objects(frame)

                for label, conf in results:
                    if label in NATURE_CLASSES:
                        print(f"Detected: {label} ({conf:.2f})")

                cv2.imshow("Video Playback", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            cap.release()
            cv2.destroyAllWindows()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["file", "live"], default="file")
    parser.add_argument("--source", default="test_assets/")
    args = parser.parse_args()

    run_video(mode=args.mode, source_path=args.source)
    print("Video processing complete.")
