# Object-Detection-People-Counting
This repository is to share a test pipeline of different object detection architectures. You can run different models using a video, WebCam or an ip from a external camera.

The main code of this repository was cloned from two other gits: 

Object Detection: https://github.com/lbeaucourt/Object-detection

mAP:
https://github.com/Cartucho/mAP

# What you can do with this repository?
- Run differents models just changing the weights
- Predict using a video, camera or a ip from a online camera
- Get the mAP from a video with ground truth
- Save the results and analyze it using jupyter notebook

# Start

- Clone the repository
- Install Docker [Download guide](https://docs.docker.com/install/linux/docker-ce/ubuntu/#set-up-the-repository)

Run in your working directory to build the docker image
> docker build -t realtime-objectdetection .

Run the docker image to predict using a WebCam
> bash runDocker.sh

To run using another video source, change the Object-detection/exec.sh file:
>python3 my-object-detection.py -d 1 -o 1 -I 0 -w 4 -q-size 100

>python3 my-object-detection.py -d 1 -o 1 -i MOC.mp4 -w 4 -q-size 100

To understand the parameters check the original repository

## Calculate mAP

## Changing Models

## Models Analysis

## Future works
