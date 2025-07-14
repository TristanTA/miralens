import os
from pydub import AudioSegment

def preprocess_audio(input_path, output_dir="processed_audio", chunk_length_sec=10, target_rate=16000, debug=False):
    os.makedirs(output_dir, exist_ok=True)
    processed_files = []

    if os.path.isdir(input_path):
        files = [os.path.join(input_path, f) for f in os.listdir(input_path)
                 if f.lower().endswith((".mp3", ".wav", ".flac", ".m4a"))]
    else:
        files = [input_path]

    for file_path in files:
        base = os.path.splitext(os.path.basename(file_path))[0]
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Input file {file_path} does not exist.")
        
        if debug:
            print(f"Processing {file_path} into {output_dir} with chunk length {chunk_length_sec}s and target rate {target_rate}Hz")
        audio = AudioSegment.from_file(file_path)
        audio = audio.set_frame_rate(target_rate).set_channels(1)

        if debug:
            print(f"Original duration: {len(audio) / 1000:.2f}s, Channels: {audio.channels}, Frame rate: {audio.frame_rate}")

        for i in range(0, len(audio), chunk_length_sec * 1000):
            chunk = audio[i:i + chunk_length_sec * 1000]
            chunk_path = os.path.join(output_dir, f"{base}_chunk{i//1000}.wav")
            chunk.export(chunk_path, format="wav")
            processed_files.append(chunk_path)

    return processed_files
