#
#  Balls - a simple and optimised version for highest frame rate
#
import _thread
import utime
import random
import gc
from picographics import PicoGraphics, DISPLAY_LCD_240X240, PEN_P8

# Do we want single or multi core
MULTICORE = True

# Ball settings
BALLS_MAX = 50
BALLS_RADIUS_MAX = 5
BALLS_RADIUS_MIN = 2

# Max frame rate
FPS_TARGET = 500

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
BOUNDS = (5, 10, WIDTH - 10, HEIGHT - 20)

# Create some balls
balls = []
for i in range(0, BALLS_MAX):
    r = random.randint(BALLS_RADIUS_MIN, BALLS_RADIUS_MAX)
    px = random.randint(r, BOUNDS[2] - r)
    py = random.randint(r, BOUNDS[3] - r)
    vx = random.randint(40, 100) / 100
    vy = random.randint(40, 100) / 100
    balls.append([
        px,
        py,
        vx,
        vy,
        r,
        COLOURS[i % len(COLOURS)]
    ])

# Core frame rates
core0Fps = 0
core1Fps = 0
moving = False

# The magnitude calc from Vector class
@micropython.native
def getMagnitude(ball):
    return (ball[2]**2 + ball[3]**2)**0.5

# Move ball routine
@micropython.native
def moveBall(ball):
    global BOUNDS

    m = getMagnitude(ball)
    ball[0] += ball[2] * (m * 4)
    ball[1] += ball[3] * (m * 4)

    # Bounce off the walls and move inside if gone out of bounds
    if ball[0] - ball[4] < 0:
        ball[0] = ball[4]
        ball[2] *= -1            

    if ball[0] + ball[4] > BOUNDS[2]:
        ball[0] = BOUNDS[2] - ball[4]
        ball[2] *= -1
        
    if ball[1] - ball[4] < 0:
        ball[1] = ball[4]
        ball[3] *= -1
        
    if ball[1] + ball[4] > BOUNDS[3]:
        ball[1] = BOUNDS[3] - ball[4]
        ball[3] *= -1

    return ball

"""Core 1 process - move the balls and track frame rate"""
@micropython.native
def core1_thread():
    global core1Fps, moving, balls, BOUNDS
    
    while True:
        core1Start = utime.ticks_ms()
        moving = True
        for ball in balls:
            ball = moveBall(ball)

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

    # Draw the bounds
    display.set_pen(BG)
    display.clear()
    display.set_pen(FG)
    display.rectangle(BOUNDS[0] - 1, BOUNDS[1] - 1, BOUNDS[2] + 2, BOUNDS[3] + 2)
    display.set_pen(BG)
    display.rectangle(BOUNDS[0], BOUNDS[1], BOUNDS[2], BOUNDS[3])

    for ball in balls:
        
        # Move the balls if we're not using multicore
        if not MULTICORE:
            ball = moveBall(ball)
            
        # Draw the ball
        display.set_pen(ball[5])
        display.circle(int(ball[0] + BOUNDS[0]), int(ball[1] + BOUNDS[1]), ball[4])    

    
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