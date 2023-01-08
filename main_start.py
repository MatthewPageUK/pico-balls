#
#  Balls
#
import _thread
import utime
import random
import micropython
import gc
from picographics import PicoGraphics, DISPLAY_LCD_240X240, PEN_P8
from bouncyballs import Bounds, Vector, Ball

# Do we want single or multi core
MULTICORE = True

# Ball settings
BALLS_MAX = 50
BALLS_RADIUS_MAX = 5
BALLS_RADIUS_MIN = 2

# Max frame rate
FPS_TARGET = 50

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
COLOURS = [
    display.create_pen(255, 0, 0),
    display.create_pen(0, 255, 0),
    display.create_pen(0, 0, 255),
    display.create_pen(255, 255, 0),
    display.create_pen(0, 255, 255),
    display.create_pen(255, 0, 255),
    WHITE,
]

# Bounding box
BOUNDS = Bounds(5, 10, WIDTH - 10, HEIGHT - 20)

# Create some balls
balls = []
for i in range(0, BALLS_MAX):
    r = random.randint(BALLS_RADIUS_MIN, BALLS_RADIUS_MAX)
    px = random.randint(r, BOUNDS.w - r)
    py = random.randint(r, BOUNDS.h - r)
    vx = random.randint(40, 100) / 100
    vy = random.randint(40, 100) / 100
    
    balls.append(Ball(
        Vector(px, py),
        Vector(vx, vy),
        r,
        COLOURS[i % len(COLOURS)]
    ))

# Core frame rates
core0Fps = 0
core1Fps = 0
moving = False


"""Core 1 process - move the balls and track frame rate"""
def core1_thread():
    global core1Fps, moving, balls, BOUNDS
    
    while True:
        core1Start = utime.ticks_ms()
        moving = True
        for ball in balls:
            ball.move(BOUNDS)

        moving = False
        timeTaken = utime.ticks_diff(utime.ticks_ms(), core1Start);
        if timeTaken < (1 / FPS_TARGET) * 1000:
            utime.sleep((1 / FPS_TARGET)-(timeTaken / 1000))
            #print("Core 1 sleep {}".format((1 / FPS_TARGET)-(timeTaken / 1000)))
    
        core1Fps = 1000 / utime.ticks_diff(utime.ticks_ms(), core1Start)

# Start the core 1 process
if MULTICORE:
    core1 = _thread.start_new_thread(core1_thread, ())

# Main Loop core 0 - draw the balls
while True:
    
    # Don't do anything if we are moving things in core 1
    while moving:
        pass
    
    core0Start = utime.ticks_ms()

    # Draw the bounds and balls
    BOUNDS.draw(FG, BG, display)
    for ball in balls:
        
        # Move the balls if we're not using multicore
        if not MULTICORE:
            ball.move(BOUNDS)
            
        # Draw the ball
        ball.draw(display, BOUNDS)    
    
    # Frame rate and memory display
    display.set_pen(WHITE)
    display.text("C0 {} fps".format(round(core0Fps, 1)), 20, 210, 200, 2)
    display.text("C1 {} fps".format(round(core1Fps, 1)), 135, 210, 200, 2)
    display.text("{}kb free".format(round(gc.mem_free() / 1000, 1)), 20, 185, 200, 2)
    
    # Update the display
    display.update()

    timeTaken = utime.ticks_diff(utime.ticks_ms(), core0Start);
    if timeTaken < (1 / FPS_TARGET) * 1000:
        utime.sleep((1 / FPS_TARGET) - (timeTaken / 1000))
        #print("Core 0 sleep {}".format((1 / FPS_TARGET)-(timeTaken / 1000)))
    
    core0Fps = 1000 / utime.ticks_diff(utime.ticks_ms(), core0Start)
    
    gc.collect()