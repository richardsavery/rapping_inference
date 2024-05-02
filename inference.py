print('loading lyric generator')
from interactive.offline_lyrics import setup_model
from transformers import pipeline

print('loading transcriber')
from interactive.voice_transcription import transcribe_audio

print('loading voice model')
from interactive.voice_gen import *
from utils import save_wavs
from scipy.io.wavfile import read, write

model, tokenizer = setup_model()
pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
)

generation_args = {
    "max_new_tokens": 500,
    "return_full_text": False,
    "temperature": 0.0,
    "do_sample": False,
}




checked_files = set()
while True:
    for filename in os.listdir(folder_path):
        if filename.endswith('.wav') and filename not in checked_files:
            file_path = os.path.join(folder_path, filename)
            print(f"Checking file: {file_path}")
            is_file_complete(file_path)
            if check_wav_duration(file_path):
                print(f"File {filename} is complete and correct duration. Moving and deleting...")

                input_text = transcribe_audio()
                print('Human: ', input_text)    

                # PARAPHRASE, WRITE AUDIO

                # SEND OVER

                # GENERATE, WRITE AUDIO


                # SEND OVER



            else:
                print(f"File {filename} is not the correct duration.")
            checked_files.add(filename)
    print("Waiting 10 seconds before next check...")
    time.sleep(10)  # Wait 10 seconds before checking for new files
