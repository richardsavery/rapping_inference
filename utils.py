import os
import time
import wave
import shutil

def is_file_complete(file_path):
    """ Check if the file size has stabilized. """
    previous_size = -1
    while True:
        current_size = os.path.getsize(file_path)
        if current_size == previous_size:
            break
        previous_size = current_size
        time.sleep(1)  # Wait a bit before checking the size again

def check_wav_duration(file_path, expected_duration=8):
    """ Verify the WAV file duration. """
    with wave.open(file_path, 'rb') as wav_file:
        frames = wav_file.getnframes()
        rate = wav_file.getframerate()
        duration = frames / float(rate)
        return duration == expected_duration

