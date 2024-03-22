import os
from settings import ConfigSingleton
# Load our configuration
config = ConfigSingleton("defaults.yaml", "overrides.yaml")
# Set these environment variables that get used by the respective clients.
os.environ['OPENAI_API_KEY'] = config.get_open_ai_key()
os.environ['ELEVENLABS_API_KEY'] = config.get_open_ai_key()

import cv2
import time
from PIL import Image
import numpy as np

import interactions.narrator_edge_tts as narrator

# Folder
frames_folder = config.get_image_dir()
audio_folder = config.get_audio_dir()
min_humans = config.get_minimum_humans_required()


# Create the frames folder if it doesn't exist
frames_dir = os.path.join(os.getcwd(), frames_folder)
os.makedirs(frames_dir, exist_ok=True)

# Create the audio dir if it doesn't exist
audio_dir = os.path.join(os.getcwd(), audio_folder)
os.makedirs(audio_folder, exist_ok=True)

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Initialize HOG for detecting people in photos
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")

# Wait for the camera to initialize and adjust light levels
time.sleep(2)

def resize_image(frame: Image, max_size=250) -> Image:
    # Convert the frame to a PIL image
    pil_img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    # Resize the image    
    ratio = max_size / max(pil_img.size)
    new_size = tuple([int(x*ratio) for x in pil_img.size])
    resized_img = pil_img.resize(new_size, Image.LANCZOS)

    # Convert the PIL image back to an OpenCV image
    frame = cv2.cvtColor(np.array(resized_img), cv2.COLOR_RGB2BGR) 
    
    return frame

def process_frames():
    script = []
    while True:
        print("Running while loop.")
        ret, frame = cap.read()

        if ret:                
            path = f"{frames_dir}/frame.jpg"

            # If humans are required, check if there are enough
            if min_humans > 0:
                # Convert to grayscale
                frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                (humans, _) = hog.detectMultiScale(frame_gray)
                
                # Print locations of humans
                print(humans)
                
                if len(humans) >= min_humans:                
                    print(f"📸 {len(humans)} people found! Saving frame.")                                
                    # Save the frame as an image file
                    cv2.imwrite(path, resize_image(frame))                
                   
                    script = narrator.interact_with_image(image_path=path, script=script)                   
                else:
                    print("Nobody found in frame... Ignoring photo.")
            else:
                print(f"📸 Saving Frame.")
                cv2.imwrite(path, resize_image(frame))

        else:
            print("Failed to capture image")

        # Wait for 2 seconds
        time.sleep(2)


def main():   
    process_frames()
    print("Finished processing frames")
    
    # Release the camera and close all windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":    
    main()



