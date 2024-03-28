from datetime import datetime
import os
import struct
import pvporcupine
from pvrecorder import PvRecorder
import pvcobra
import wave
import openai_helpers

class AudioCommandProcessor:
    def __init__(self, 
            picovoice_access_key,
            keywords=None,
            keyword_paths=None,
            sensitivities=None,
            voice_probability_threshold=0.75,
            silence_threshold=2,
            library_path=None,
            model_path=None,
            audio_device_index=-1,
            audio_output_dir='audio'):     
        
        # Validate keyword paths and sensitivities
        if keyword_paths is None:
            if keywords is None:
                raise ValueError("Either 'keywords' or 'keyword_paths' must be set.")
            keyword_paths = [pvporcupine.KEYWORD_PATHS[keyword] for keyword in keywords]

        if sensitivities is None:
            sensitivities = [0.5] * len(keyword_paths)

        if len(keyword_paths) != len(sensitivities):
            raise ValueError('Number of keywords does not match the number of sensitivities.')
            
        self.voice_probability_threshold = voice_probability_threshold
        self.silence_threshold = silence_threshold
        self.audio_device_index = audio_device_index
        self.audio_output_dir = audio_output_dir

        try:
            # Intialize porcupine for keyword voice activation
            self.porcupine = pvporcupine.create(
                access_key=picovoice_access_key,
                library_path=library_path,
                model_path=model_path,
                keyword_paths=keyword_paths,
                sensitivities=sensitivities)
            
            # Initialize cobra for voice detection
            self.cobra = pvcobra.create(access_key=picovoice_access_key)

            self.keywords = list()
            for x in keyword_paths:
                keyword_phrase_part = os.path.basename(x).replace('.ppn', '').split('_')
                if len(keyword_phrase_part) > 6:
                    self.keywords.append(' '.join(keyword_phrase_part[0:-6]))
                else:
                    self.keywords.append(keyword_phrase_part[0])

            print('Porcupine version: %s' % self.porcupine.version)
            print('Cobra version: %s' % self.cobra.version)

        except pvporcupine.PorcupineInvalidArgumentError as e:
            print("One or more arguments provided to Porcupine is invalid")            
            raise e
        except pvporcupine.PorcupineActivationError as e:
            print("AccessKey activation error")
            raise e
        except pvporcupine.PorcupineActivationLimitError as e:
            print("AccessKey '%s' has reached it's temporary device limit" % picovoice_access_key)
            raise e
        except pvporcupine.PorcupineActivationRefusedError as e:
            print("AccessKey '%s' refused" % picovoice_access_key)
            raise e
        except pvporcupine.PorcupineActivationThrottledError as e:
            print("AccessKey '%s' has been throttled" % picovoice_access_key)
            raise e
        except pvporcupine.PorcupineError as e:
            print("Failed to initialize Porcupine")
            raise e
        
        self.recorder = None
        self.wav_file = None
        self.is_recording = False
        self.silence_start_time = None 
        self.running = False
        self.current_filename = None
        
    def start(self):
        self.running = True
        self.recorder = PvRecorder(
            frame_length=self.porcupine.frame_length,
            device_index=self.audio_device_index
        )
        self.recorder.start()

    def tryGetCommand(self):
        if not self.running:
            raise Exception("Call start() before trying to get a command.")
        
        pcm = self.recorder.read()
        result = self.porcupine.process(pcm)

        if(self.wav_file is not None):
            self.wav_file.writeframes(struct.pack("h" * len(pcm), *pcm))

        if result >= 0:
            print('[%s] Detected %s' % (str(datetime.now()), self.keywords[result]))
            if not self.is_recording:
                self.is_recording = True 
                if self.wav_file is not None:
                    self.wav_file.close()

                self.current_filename = f"{datetime.now().timestamp()}.wav"
                self.current_filepath = os.path.join(self.audio_output_dir, self.current_filename)
                self.wav_file = wave.open(self.current_filepath, "w")
                self.wav_file.setnchannels(1)
                self.wav_file.setsampwidth(2)
                self.wav_file.setframerate(16000)
        
        elif self.is_recording:
            voice_probability = self.cobra.process(pcm)

            if voice_probability < self.voice_probability_threshold:
                if self.silence_start_time is None:
                    self.silence_start_time = datetime.now() 

            elif (datetime.now() - self.silence_start_time).total_seconds() >= self.silence_threshold:
                # If silence exceeds threshold, stop recording
                print("Silence threshold exceeded. Stopping recording.")      
                self.is_recording = False
                self.silence_start_time = None
                if self.wav_file is not None:
                    self.wav_file.close()
                    self.wav_file = None
                    last_file_path = self.current_filepath
                    self.current_filename = None
                    
                    return openai_helpers.text_from_audio(file_path=last_file_path)
                
        return None

    # def waitForCommand(self):
        