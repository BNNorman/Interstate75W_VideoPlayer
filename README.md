# Readme.md

This repository is my Python code which allows one device to send video frames to a Pimoroni Interstate 75W (I75W) running CircuitPython from another device running Python. The 'other' device must be able to perform fast openCV and numpy operations in order to maintain a decent frame rate.

In my setup the video sender is my Windows PC and the Interstate 75W (I75W) is the video receiver. The I75W is connected to a 64x64 led matrix formed by daisy chaining two HUB75 64x32 matrices.

The code uses UDP to send a video frame by frame to the I75W which then displays the frame on the HUB75 matrix. This could be a video or a slideshow (just slowdown the frames per second)

The I75W, in my case is running Adafruit CircuitPython 8.0.0-beta.6 on 2022-12-21; Raspberry Pi Pico W with rp2040

# VideoSender.py

This is a standard Python (3.10) which reads an MP4 video using openCV. CircuitPython cannot read MP4 files and the available disc space is too low to accomodate a video file hence the reason for sending the frames from a remote device.

# VideoReceiver.py

This is CircuitPython code to received the video frames and throw them onto the matrix. It expects 8192 bytes per frame which is 64x64x2 - CircuitPython uses RGB565 to hold pixel values in uint16 variables. When this runs it tells you the IP address and port number to configure the VideoSender.py for.

# MyMatrix.py

This is the CircuitPython rgbmatrix definition for my matrix.

# secrets.py

This file holds the network SSID and password. It has the following format:-
```
secrets = {
    'ssid' : 'your ssid',
    'password' : 'your password',
    }
```
