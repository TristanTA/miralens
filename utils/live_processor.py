import cv2
import time
import tempfile
import sounddevice as sd
import scipy.io.wavfile as wavfile
from utils.audio_processor import detect_birds
from utils.video_processor import detect_objects


def record_audio_chunk(duration=5, sample_rate=44100):
    print("Recording audio...")
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()

    temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    wavfile.write(temp_audio.name, sample_rate, audio_data)
    return temp_audio.name


def process_live_stream(chunk_duration=5.0):
    """
    Captures webcam + mic input every chunk_duration seconds,
    runs both processors, and prints timestamped results.
    """
    print("Starting live Mira Lens stream...")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Could not open webcam.")

    try:
        while True:
            start_time = time.time()
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame from webcam.")
                continue

            # --- Process video frame ---
            video_detections = []
            detections = detect_objects(frame)
            for label, conf, bbox in detections:
                video_detections.append({
                    "timestamp": round(time.time() - start_time, 2),
                    "source": "video",
                    "raw_label": label,
                    "confidence": conf,
                    "location": bbox
                })

            # --- Process audio chunk ---
            audio_file = record_audio_chunk(duration=chunk_duration)
            bird_results = detect_birds(audio_file)
            audio_detections = []
            for label, conf in bird_results:
                audio_detections.append({
                    "timestamp": round(time.time() - start_time, 2),
                    "source": "audio",
                    "raw_label": label,
                    "confidence": conf,
                    "location": None
                })

            # --- Print results ---
            for d in video_detections + audio_detections:
                print(d)

            elapsed = time.time() - start_time
            if elapsed < chunk_duration:
                time.sleep(chunk_duration - elapsed)

    except KeyboardInterrupt:
        print("\nLive stream stopped by user.")
    finally:
        cap.release()