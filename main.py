import os
from audio import AudioCommandProcessor

def main():    
    # Access environment variables
    picovoice_access_key = os.getenv('PICOVOICE_ACCESS_KEY')
    keywords = os.getenv('KEYWORDS').split(',') if os.getenv('KEYWORDS') else None
    keyword_paths = os.getenv('KEYWORD_PATHS').split(',') if os.getenv('KEYWORD_PATHS') else None
    library_path = os.getenv('LIBRARY_PATH')
    model_path = os.getenv('MODEL_PATH')
    sensitivities = [float(s) for s in os.getenv('SENSITIVITIES').split(',')] if os.getenv('SENSITIVITIES') else None
    audio_device_index = int(os.getenv('AUDIO_DEVICE_INDEX', -1))
    audio_output_dir = os.getenv('OUTPUT_PATH', 'audio')
    show_audio_devices = os.getenv('SHOW_AUDIO_DEVICES')
    voice_probability_threshold = float(os.getenv('VOICE_PROBABILITY_THRESHOLD', 0.75))
    silence_threshold = int(os.getenv("COMMAND_SILENCE_THRESHOLD", 2))

    audioCommandProcessor = AudioCommandProcessor(
        picovoice_access_key=picovoice_access_key,
        keywords=keywords, 
        keyword_paths=keyword_paths,
        library_path=library_path,
        model_path=model_path,
        sensitivities=sensitivities,
        audio_device_index=audio_device_index,
        audio_output_dir=audio_output_dir,
        voice_probability_threshold=voice_probability_threshold,
        silence_threshold=silence_threshold
    )

    # Start the recording and text processing
    audioCommandProcessor.start()

    while True:
        command = audioCommandProcessor.tryGetCommand()

        if command != None:
            print(command)

        
    

if __name__ == '__main__':
    main()