"""
VideoSender.py

Opens a video file, reduces the frame to fit in the 64x64 matrix, adjusts the colours to compensate for LED characteristics.

"""
import socket
import time
import cv2
from PIL import Image
import numpy as np
import sys


HOST = "192.168.1.xxx"  # server IP address as reoported by the interstate 75W when the receiver code runs
PORT = 8000             # server port

MATRIX_X,MATRIX_Y=64,64

# LED colour correction factors
gain_r=1.0
gain_g=0.8
gain_b=0.5

DEFAULT_FPS=27

SOURCE="your mp4 video"

# check the source file exists
try:
    # just try to open the video
    with open(SOURCE) as fp:
       print(f"Source {SOURCE} exists")

except Exception as e:
    print(f"Unable to open {SOURCE}. Error was {e}.Quitting")
    sys.exit(0)

print(f"Sending to host {HOST} on port {PORT}")

serverSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

vid=cv2.VideoCapture(SOURCE)

# work out aspect ratio using the first frame (not sent)

(grabbed, frame) = vid.read()
frame_h,frame_w=frame.shape[:2]

ASPECT_RATIO=frame_h/frame_w


# work out the video frame rate
# Find OpenCV version
(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
FPS=DEFAULT_FPS
if int(major_ver)  < 3 :
    FPS = vid.get(cv2.cv.CV_CAP_PROP_FPS)
    print(f"Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {FPS}")
else :
    FPS = vid.get(cv2.CAP_PROP_FPS)
    print(f"Frames per second using video.get(cv2.CAP_PROP_FPS) : {FPS}")

FRAMETIME=1.0/FPS

def resizeKeepAspect(img):
    global ASPECT_RATIO, frame_h,frame_y

    DSIZE=(MATRIX_Y,MATRIX_X) # default

    if ASPECT_RATIO>1: # Height>width
        DSIZE=(int(MATRIX_Y*ASPECT_RATIO),MATRIX_X)
    elif ASPECT_RATIO<1:
        DSIZE=(MATRIX_Y,int(MATRIX_X*ASPECT_RATIO))

    return cv2.resize(frame, dsize=DSIZE, interpolation=cv2.INTER_CUBIC)

#########################################################
while True:
    frame_start = time.monotonic()
    (grabbed, frame) = vid.read()

    if not grabbed:
        print(f"Frame not grabbed from source! End of video?")
        break


	# reducing the frame now makes other stuff faster
	res = resizeKeepAspect(frame) 

    # colour correction required for LED matrix
    res[:,:,0]=np.minimum(res[:,:,0]*gain_r,255)
    res[:,:,1]=np.minimum(res[:,:,1]*gain_g,255)
    res[:,:,2]=np.minimum(res[:,:,2]*gain_b,255)

    # convert to RGB565
    R5 = (res[..., 0] >> 3).astype(np.uint16) << 11
    G6 = (res[..., 1] >> 2).astype(np.uint16) << 5
    B5 = (res[..., 2] >> 3).astype(np.uint16)

    # Assemble components into RGB565 uint16 image
    image_data = R5 | G6 | B5


	# paste the image_data into the 64x64 shape of my matrix
	# allowing for landscape/portrait orientation
	if ASPECT_RATIO<1: # h<w
		res_h,res_w=RGB565.shape[:2]
		Yoffset=(MATRIX_Y-res_h)//2
		image_data=np.zeros((MATRIX_Y,MATRIX_X),dtype=np.uint16)
		image_data[Yoffset:Yoffset+res_h,:]=RGB565 # [:,:]
	elif ASPECT_RATIO>1:
        res_h,res_w=RGB565.shape[:2]
        Xoffset=(MATRIX_X-res_w)//2
        image_data=np.zeros((MATRIX_Y,MATRIX_X),dtype=np.uint16)
        image_data[:,Xoffset:Xoffset+res_w]=RGB565

		
	# convert to a 1D array of pixels
	flat=image_data.flatten() 
	frame_bytes=flat.tobytes() # we now have a bytearray
	bytes_sent = serverSocket.sendto(frame_bytes, (HOST, PORT))

    # match the video frame rate
    while (time.monotonic() - frame_start) < FRAMETIME:
        pass

