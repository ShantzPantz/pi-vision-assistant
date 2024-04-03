import base64
import time
import numpy as np
import os
import openai_helpers
from PIL import Image
import io
import picamera2

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

class CameraSightProcessor:
    def __init__(self):
        # Folder
        self.folder = "frames"

        # Create the frames folder if it doesn't exist
        self.frames_dir = os.path.join(os.getcwd(), self.folder)
        os.makedirs(self.frames_dir, exist_ok=True)

    def start(self):
        # Initialize the camera
        self.camera = picamera2.Picamera2()
        
        self.camera.start()

        # Wait for the camera to initialize
        time.sleep(2)

    def capture_image_as_base64(self):
        # Capture image to a stream
        metadata = self.camera.capture_file("test.png")
        print(metadata)

        # Getting the base64 encoding
        base64_image = encode_image("test.png")

        base64_image
