from birdnetlib import Recording
from birdnetlib.analyzer_lite import LiteAnalyzer

def detect_birds(audio_path, lat=None, lon=None, date=None, min_conf=0.25):
    analyzer = LiteAnalyzer()
    rec = Recording(analyzer, audio_path, lat=lat or 0,
                    lon=lon or 0, date=date, min_conf=min_conf)
    rec.analyze()
    return rec.detections  # list of dicts

if __name__ == "__main__":
    audio = "path/to/test.wav"
    detections = detect_birds(audio)
    for det in detections:
        print(f"{det['start_time']:.1f}-{det['end_time']:.1f}s: "
              f"{det['common_name']} ({det['confidence']:.2f})")
