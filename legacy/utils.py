import datetime
import shutil
import os
import time
import wave

def save_wavs(human_fp, robot_fp):
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")

    new_human_filename = f"saved_interactions/{formatted_datetime}_human.wav"
    new_robot_filename = f"saved_interactions/{formatted_datetime}_robot.wav"

    shutil.copyfile(human_fp, new_human_filename)
    shutil.copyfile(robot_fp, new_robot_filename)

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

