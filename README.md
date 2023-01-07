# Pico Balls

A bouncing balls demo using the multicore features of the Raspberry Pi Pico. Requires the PicoGraphics library to display on a 240x240 LCD SPI screen.

* Uses core0 to maintain a draw loop and handle screen updates
* Uses core1 to maintain the balls and calculate the physics

Uploading VID_20230107_191156.mp4…

## Hardware
* Raspberry Pi Pico - https://thepihut.com/products/raspberry-pi-pico-w
* LCD Screen - https://thepihut.com/products/1-3-spi-colour-lcd-240x240-breakout

## Installation
Copy ```bouncyballs.py``` and ```main.py``` to your Pico and restart.

## Settings
* Change ```MULTICORE``` to enable or disable the second core.
* Update the ball settings and number to suit

## Notes
With 1 ball still can't get a display frame rate above 22 fps.

## Things to try
* Collision detection and bounce
* Optimising code for maximum efficiency
* Why is frame rate capped at 22fps?


