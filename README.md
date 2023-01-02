# Readme.md

This repository is my Python code which allows one device to send video frames to a Pimoroni Interstate 75W (I75W) running CircuitPython from another device running Python. The 'other' device must be able to perform fast openCV and numpy operations in order to maintain a decent frame rate.

In my setup the video sender is my Windows PC and the Interstate 75W (I75W) is the video receiver. The I75W is connected to a 64x64 led matrix formed by daisy chaining two HUB75 64x32 matrices.

The code uses UDP to send a video frame by frame to the I75W which then displays the frame on the HUB75 matrix. This could be a video or a slideshow (just slowdown the frames per second)

The I75W, in my case is running Adafruit CircuitPython 8.0.0-beta.6 on 2022-12-21; Raspberry Pi Pico W with rp2040

# VideoSender.py

This is a standard Python (3.10) which reads an MP4 video using openCV. CircuitPython cannot read MP4 files and the available disc space is too low to accomodate a video file hence the reason for sending the frames from a remote device.

The program uses the frame rate of the video source to control the rate at which frames are sent to the host machine.

# interstate75W

This folder contains the code which runs on the interstate 75W.