import os
import tempfile
from pydub import AudioSegment
from utils.birdnet_wrapper import detect_birds as birdnet_detect

def detect_birds(audio_chunk_path):
    detections = birdnet_detect(audio_chunk_path)
    return [(d["common_name"], d["confidence"]) for d in detections]

def process_audio(audio_path, chunk_duration=5.0):
    """
    Splits audio into chunks and returns list of detection dicts.
    """
    results = []
    audio = AudioSegment.from_file(audio_path)
    chunk_ms = int(chunk_duration * 1000)
    total_chunks = len(audio) // chunk_ms

    with tempfile.TemporaryDirectory() as temp_dir:
        for i in range(total_chunks):
            start_ms = i * chunk_ms
            chunk = audio[start_ms:start_ms + chunk_ms]
            chunk_path = os.path.join(temp_dir, f"chunk_{i}.wav")
            chunk.export(chunk_path, format="wav")

            detections = detect_birds(chunk_path)
            for label, conf in detections:
                results.append({
                    "timestamp": round(i * chunk_duration, 2),
                    "source": "audio",
                    "raw_label": label,
                    "confidence": conf,
                    "location": None
                })

    return results
