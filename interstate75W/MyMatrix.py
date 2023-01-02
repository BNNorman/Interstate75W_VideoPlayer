# MyMatrix 64x64 but tiled one above other (2 tiles)
# Uses Adafruit CircuitPython 8.0.0-beta.6 on 2022-12-21; Raspberry Pi Pico W with rp2040
# May also work with later 8.0.0 betas/releases
#
import rgbmatrix
import board
import displayio


displayio.release_displays()

# intiailise the matrix
RGB_PINS=[board.GP0,board.GP1,board.GP2,board.GP3,board.GP4,board.GP5] # R0,G0,B0,R1,G1,B1
ADR_PINS=[board.GP6,board.GP7,board.GP8,board.GP9] #,board.GP10] ADDR_A..ADDR_E

matrix = rgbmatrix.RGBMatrix(
    width=64, tile=2, bit_depth=6,
    rgb_pins=RGB_PINS,
    addr_pins=ADR_PINS,
    clock_pin=board.GP11, latch_pin=board.GP12, output_enable_pin=board.GP13,
    doublebuffer=True,serpentine=False)



if __name__=="__main__":

    # test the display with an image
    # if your image is bigger than 64x64 pixels you will only get a segment
    # of itdisplayed
    display = framebufferio.FramebufferDisplay(matrix, auto_refresh=True)


    # Setup the bitmap data source
    bitmap = displayio.OnDiskBitmap("your image.bmp") # only bmp palette images are supported

    # Create a TileGrid to hold the bitmap
    tile_grid = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)

    # Create a Group to hold the TileGrid
    group = displayio.Group()

    # Add the TileGrid to the Group
    group.append(tile_grid)

    # Add the Group to the Display
    display.show(group)

    # Loop forever so you can enjoy your image
    while True:
        pass

