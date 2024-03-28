# NewName

This is a fork of [Charlie Holtz's](https://github.com/cbh123/narrator/tree/main) repository [narrator](https://github.com/cbh123/narrator/tree/main) with substantial changes.

## Introduction

Experiments with a Raspberry PI, Camera, Microphone and AI.

## Setup

Clone this repository and set up a virtual environment:

First, set up the environment.
For Windows:
```bat
cd setup/windows
setup.bat
```

For Raspberry Pi
```bash
cd setup/raspbian
./setup.sh
```

## Voice Recognition
- [Google Assistant Service](https://developers.google.com/assistant/sdk/guides/service/python)

### Thoughts & TODO
- Support different modes. Modes will determine how the application responds. 
- Add an SQLite DB do handle app configurations and persistent state.
- Modes:
    - Check if a human is in the frame, if they are, process the image, otherwise, do nothing. 
    - Add multiple personalites, keep a dictionary of available voices and assign them "personalities" via chatgpt commands. 
- Support voice commands, allow the user to interact with the pi, and have the pi respond with voice AI. I was hoping to utilize Google Assistant services for this. 