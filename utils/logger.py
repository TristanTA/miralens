import os
import json
from datetime import datetime

LOG_DIR = "data/sightings"
os.makedirs(LOG_DIR, exist_ok=True)

def log_detection(audio_path, detection, mode="birding"):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "mode": mode,
        "input_file": audio_path,
        "top_species": detection["common_name"],
        "confidence": round(detection["confidence"], 2),
        "start_time": detection["start_time"],
        "end_time": detection["end_time"]
    }

    filename = os.path.join(LOG_DIR, "session_log.json")

    # Append to log file
    if os.path.exists(filename):
        with open(filename, "r+") as f:
            logs = json.load(f)
            logs.append(log_entry)
            f.seek(0)
            json.dump(logs, f, indent=2)
    else:
        with open(filename, "w") as f:
            json.dump([log_entry], f, indent=2)

    return log_entry