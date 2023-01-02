# Readme.md

# CircuitPython

This code works using "Adafruit CircuitPython 8.0.0-beta.6 on 2022-12-21; Raspberry Pi Pico W with rp2040". However, this version does not expose the RGB and ADDR pin definitions for the board as you can see from this REPL output:-


You can download it from here:- https://circuitpython.org/board/raspberry_pi_pico_w/

```

Adafruit CircuitPython 8.0.0-beta.6 on 2022-12-21; Raspberry Pi Pico W with rp2040
>>> import board
>>> dir(board)
['__class__', '__name__', 'A0', 'A1', 'A2', 'A3', 'GP0', 'GP1', 'GP10', 'GP11', 'GP12', 'GP13', 'GP14', 'GP15', 'GP16', 'GP17', 'GP18', 'GP19', 'GP2', 'GP20', 'GP21', 'GP22', 'GP26', 'GP26_A0', 'GP27', 'GP27_A1', 'GP28', 'GP28_A2', 'GP3', 'GP4', 'GP5', 'GP6', 'GP7', 'GP8', 'GP9', 'LED', 'SMPS_MODE', 'STEMMA_I2C', 'VBUS_SENSE', 'VOLTAGE_MONITOR', 'board_id']
>>> 
```

## I75W Matrix Pins

Using the Interstate75 schematic the Matrix pins are as follows. You can see this in MyMatrix.py.

```
	R0	GPIO0
	G0	GPIO1
	B0	GPIO2
	R1	GPIO3
	G1	GPIO4
	B1 	GPIO5
	ROW_A	GPIO6
	ROW_B	GPIO7
	ROW_C	GPIO8
	ROW_D	GPIO9
	ROW_E	GPIO10
```

# VideoReceiver.py

This is CircuitPython code to receive the video frames and throw them onto the matrix. It expects 8192 bytes per frame which is 64x64x2 - CircuitPython uses RGB565 to hold pixel values in uint16 variables. When this runs it tells you the IP address and port number to configure the VideoSender.py for.

# MyMatrix.py

This is the CircuitPython rgbmatrix definition for my matrix which is a daisy chained pair of 64x32 HUB75 panels bought from AliExpress years ago.

# secrets.py

This file holds the network SSID and password. It has the following format:-

```
secrets = {
    'ssid' : 'your ssid',
    'password' : 'your password',
    }
```
