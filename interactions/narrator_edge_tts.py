import asyncio
import os
import subprocess
from typing import Dict, List
import wave
from openai import OpenAI
import base64
import time
import simpleaudio as sa
import errno
# from elevenlabs import generate, play, set_api_key, voices
import edge_tts
from pydub import AudioSegment
import platform

client = OpenAI()

# set_api_key(os.environ.get("ELEVENLABS_API_KEY"))
VOICE = 'en-GB-ThomasNeural'


def encode_image(image_path):
    while True:
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode("utf-8")
        except IOError as e:
            if e.errno != errno.EACCES:
                # Not a "file in use" error, re-raise
                raise
            # File is being written to, wait a bit and retry
            time.sleep(0.1)


def play_audio(text):
    communicate = edge_tts.Communicate(text, VOICE)

    unique_id = base64.urlsafe_b64encode(os.urandom(30)).decode("utf-8").rstrip("=")
    dir_path = os.path.join("narration2", unique_id)
    os.makedirs(dir_path, exist_ok=True)
    mp3_file = os.path.join(dir_path, "audio.mp3")
    
    asyncio.run(communicate.save(mp3_file)) 
  
    if platform.system() == 'Windows':
        print(mp3_file)
        command = ['start', 'wmplayer', mp3_file]
    elif platform.system() == 'Darwin':  # macOS
        command = ['afplay', mp3_file]
    else:  # Linux / Raspberry Pi
        command = ['mpg123', mp3_file]

    # Execute the command
    subprocess.run(command)    


def generate_new_line(base64_image):
    return [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Describe this image"},
                {
                    "type": "image_url",
                    "image_url": f"data:image/jpeg;base64,{base64_image}",
                },
            ],
        },
    ]


def analyze_image(base64_image, script):
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "system",
                "content": """
                You are Sir David Attenborough. Narrate the picture of the human as if it is a nature documentary.
                Make it snarky and funny. Don't repeat yourself. Make it short. If I do anything remotely interesting, make a big deal about it!
                """                
            }
        ]
        + script
        + generate_new_line(base64_image),
        max_tokens=500,
    )
    response_text = response.choices[0].message.content
    return response_text


def interact_with_image(image_path, script) -> List[Dict]:
    # getting the base64 encoding
    base64_image = encode_image(image_path)

    # analyze posture
    print("👀 David is watching...")
    analysis = analyze_image(base64_image, script=script)

    print("🎙️ David says:")
    print(analysis)
    play_audio(analysis)

    script = script + [{"role": "assistant", "content": analysis}]

    # wait for 5 seconds
    time.sleep(5)
    return script
    
