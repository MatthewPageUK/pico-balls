#
#  Time the display
#
import _thread
import utime
import random
import micropython
import gc
from picographics import PicoGraphics, DISPLAY_LCD_240X240, PEN_P8
from bouncyballs import Bounds, Vector, Ball

# Display settings
display = PicoGraphics(display=DISPLAY_LCD_240X240, pen_type=PEN_P8)
display.set_backlight(1)
display.set_font('bitmap8')
WIDTH, HEIGHT = display.get_bounds()
MIDX = int(WIDTH/2)
MIDY = int(WIDTH/2)

# Create some colours
BG = display.create_pen(0, 0, 0)
FG = display.create_pen(180, 50, 180)
WHITE = display.create_pen(255, 255, 255)

# Core frame rates
core0Fps = 0

# Main Loop core 0
while True:
    
    core0Start = utime.ticks_ms()

    display.set_pen(BG)
    #display.clear()
    display.set_pen(WHITE)
    
    #for i in range(0, 100):
    #    display.rectangle(100, 100, 10, 10)
    
    display.circle(100, 100, 20)    

    # Frame rate and memory display
    display.text("C0 {} fps".format(round(core0Fps, 1)), 20, 210, 200, 2)
    
    # Update the display
    display.update()

    timeTaken = utime.ticks_diff(utime.ticks_ms(), core0Start);
    
    core0Fps = 1000 / utime.ticks_diff(utime.ticks_ms(), core0Start)

    gc.collect()