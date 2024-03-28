from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

from openai import OpenAI

client = OpenAI()

def text_from_audio(file_path): 
    audio_file= open(file_path, "rb")
    transcription = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file
    )

    print("Audio Transcript:")
    print(transcription.text)

    return transcription.text