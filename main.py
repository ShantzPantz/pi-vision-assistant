import os
from audio import AudioCommandProcessor
from camera import CameraSightProcessor
import openai_helpers

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

    cameraSightProcessor = CameraSightProcessor()

    # Start the recording and text processing
    audioCommandProcessor.start()
    # Setup Camera processor
    cameraSightProcessor.start()

    while True:
        command = audioCommandProcessor.tryGetCommand()
        if command == None:
            return
        
        if openai_helpers.does_command_require_camera(command):
            image_output = cameraSightProcessor.capture_image_as_base64()
            
            response = openai_helpers.analyze_image('snoop', base64_image=image_output, command=command)
            #todo narrate here. 
            print(response)
        else:
            response = openai_helpers.generate_response('snoop', [{
                "role": "user",
                "content": command
            }])
            print(response)        
         
    

if __name__ == '__main__':
    main()