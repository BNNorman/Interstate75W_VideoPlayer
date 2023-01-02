# ImageReceiver.py
# using Adafruit CircuitPython 8.0.0-beta.6 on 2022-12-21; Raspberry Pi Pico W with rp2040

import wifi
import socketpool
import displayio
import framebufferio
import bitmaptools
import array
import time

from MyMatrix import matrix
from secrets import secrets

PORT=8000
FRAME_SIZE=8192	# 64x64x2 bytes per pixel - RGB565

wifi.radio.connect(ssid=secrets["ssid"],password=secrets["password"])
print("IP addr:", wifi.radio.ipv4_address," listening on port",PORT)


# setup the matrix as a display
display = framebufferio.FramebufferDisplay(matrix, auto_refresh=True)

# create the display background image
image_bitmap=displayio.Bitmap(display.width, display.height, 65536) # RGB565 

# attach it to a group and display it with auto-refresh
g = displayio.Group()
g.append(displayio.TileGrid(image_bitmap, pixel_shader=displayio.ColorConverter(input_colorspace=displayio.Colorspace.RGB565)))
display.show(g)

# set up this server
pool=socketpool.SocketPool(wifi.radio)
server=pool.socket(pool.AF_INET,pool.SOCK_DGRAM) 
server.bind((str(wifi.radio.ipv4_address),PORT))


# somewhere to capture the image frame data
# declaring it's size ensures contiguous memory is used
# in an effort to avoid memory copying which could slow
# the business of receiving and converting the image frames
image_frame=bytearray(8192)

def collectFrame():
    """
    Called to collect the next frame bytes
    """
    global image_frame,image_bitmap,server
    
    total_bytes_recvd=0
    bytes_remaining=FRAME_SIZE
    view=memoryview(image_frame) # prevents copying memory
    
    try:
        # in case the frame bytes don't all arrive at the same time.
        while total_bytes_recvd<8192:
            bytes_recvd,addr= server.recvfrom_into(view[:bytes_remaining])
            total_bytes_recvd+=bytes_recvd
            bytes_remaining-=bytes_recvd
            view=view[bytes_recvd:] # push the insertion point
        
    except Exception as e:
        print(f"collectFrame() error {e}")
        
def displayFrame():
    """
    convert the image_frame bytearray into an RGB565 array then blit it to the
    displayed bitmap.
    """
    global image_frame, image_bitmap
    this_frame=array.array('H',image_frame) # converts back to uint16 per pixel
    bitmaptools.arrayblit(image_bitmap,this_frame)
    image_bitmap.dirty() # tell the display to refresh

print("Waiting for frames from image sender")

while True:
    
    try:
        collectFrame()
        displayFrame()
          
    except Exception as e:
        server.close()
        break

