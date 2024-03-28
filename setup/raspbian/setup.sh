#!/bin/bash

# Install Docker for Rhasspy
curl -sSL https://get.docker.com | sh
sudo usermod -aG docker brian

# install mpg123
sudo apt-get update 
sudo apt-get install mpg123

# Install the dependencies:
pip install -r requirements.txt