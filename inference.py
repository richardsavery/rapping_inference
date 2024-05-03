print('loading transcription model')
from interactive.offline_lyrics import setup_model
from transformers import pipeline

from interactive.voice_transcription import transcribe_audio

print('loading voice model')
from interactive.voice_gen import *
from interactive.utils import *
from scipy.io.wavfile import read, write
import os
import subprocess

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

def generate_clean(from_human):
    message = [{"role": "user", "content": from_human}]
    output = pipe(message, **generation_args)
    robot_response = output[0]['generated_text']
    robot_response = robot_response.replace(',\n',' ')
    robot_response = robot_response.replace('\n',' ')
    print('Robot: ', robot_response)
    return robot_response
    



folder_path = 'audio'
audio_length = 0

while True:
    checked_files = set()
    for filename in os.listdir(folder_path):
        if filename.endswith('.wav') and filename not in checked_files:
            file_path = os.path.join(folder_path, filename)
            print(f"Checking file: {file_path}")
            is_file_complete(file_path)
            if check_wav_duration(file_path):
                print(f"File {filename} is complete and correct duration. Changing Name")
                target_fp = 'voice.wav'
                shutil.move(file_path, target_fp)
                input_text = transcribe_audio()
                print('Human: ', input_text)    

                # PARAPHRASE, WRITE AUDIO
                from_human = "Can you repeat this in rhyme, but keep it short : you asked" + input_text
                
                robot_response = generate_clean(from_human)
                spec, audio = infer(spec_model, vocoder, 
                                    robot_response, 
                                    speaker=None)
                write('gen/para.wav', 22050, audio[0])

                audio_length = len(audio[0])/22050
                # SEND
                command = [
                    "scp",
                    "-i", "/home/richard/.ssh/id_rsa",
                    "-o", "StrictHostKeyChecking=no",
                    "gen/para.wav",
                    "keirzomac@192.168.50.189:~/Desktop/zokeir/recordings/to_play/para.wav"]
                    
                subprocess.run(command)

                
                # ANSWER
                from_human = "Can you answer in rhyme, but keep it short :" + input_text
                robot_response = generate_clean(from_human)
                spec, audio = infer(spec_model, vocoder, 
                                    robot_response, 
                                    speaker=None)
                write('gen/response.wav', 22050, audio[0])

                command = [
                    "scp",
                    "-i", "/home/richard/.ssh/id_rsa",
                    "-o", "StrictHostKeyChecking=no",
                    "gen/response.wav",
                    "keirzomac@192.168.50.189:~/Desktop/zokeir/recordings/to_play/response.wav"]
                    
                subprocess.run(command)
                audio_length += len(audio[0])/22050
                

                time.sleep(int(audio_length))
                print("Waiting " + str(int(audio_length)))



            else:
                print(f"File {filename} is not the correct duration.")
            checked_files.add(filename)
            
    print("Waiting ` seconds before next check...")
    time.sleep(1)  # Wait 10 seconds before checking for new files

