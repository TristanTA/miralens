import os
import tempfile
import moviepy.editor as mp # type: ignore
from moviepy.editor import VideoFileClip # type: ignore
from utils.video_processor import process_video
from utils.audio_processor import process_audio

def extract_audio_from_video(video_path, output_path):
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(output_path, codec='pcm_s16le', verbose=False, logger=None)

def process_media(input_path, fps=1.0, chunk_duration=5.0):
    """
    Accepts an MP4 or WAV file, returns unified detections.
    """
    detections = []

    # Create temp folder for audio if needed
    with tempfile.TemporaryDirectory() as temp_dir:
        file_ext = os.path.splitext(input_path)[-1].lower()

        if file_ext in [".mp4", ".mov", ".avi"]:
            # Extract audio from video
            audio_path = os.path.join(temp_dir, "extracted_audio.wav")
            extract_audio_from_video(input_path, audio_path)

            # Process both
            video_results = process_video(input_path, fps=fps)
            audio_results = process_audio(audio_path, chunk_duration=chunk_duration)

        elif file_ext in [".wav", ".mp3"]:
            video_results = []
            audio_results = process_audio(input_path, chunk_duration=chunk_duration)

        else:
            raise ValueError(f"Unsupported file type: {file_ext}")

        detections.extend(video_results)
        detections.extend(audio_results)

    # Sort by timestamp for easier downstream processing
    detections.sort(key=lambda x: x["timestamp"])
    return detections
