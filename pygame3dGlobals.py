

from math import *
from pygame import *

BLACK = [0,0,0]
GREEN = [0,255,0]
BLUE = [0,0, 255]
RED = [255,0,0]
WHITE = [255,255,255]
LINECOLOR = GREEN

spin = radians(50) # spin is the radian measure of the grid's rotation
                   #    0 degrees has positive x to the right 
                   #    default 50
tilt = radians(75) # tilt is the radian measure of the grid's pitch
                   #    90 degrees is elevation, 0 is plan 
                   #    default 75
maxtilt = radians(85)
mintilt = radians(0)                   
zoom = 1           # zoom is the level of magnification
                   #    1 is default, 2 is zoomed to double size, 0.5 is half
horoff = 0         # horoff is the x coordinate on the grid that is in
                   #    the center of the screen. 
veroff = 0         # veroff is the y coordinate on the grid that is in
                   #    the center of the screen. 
            
init()            
screenwidth = 1200
screenheight = 800
screen = display.set_mode([screenwidth,screenheight])

display.set_caption("Axonometric")

def checkBounds():
    global tilt, spin
    if tilt > maxtilt: tilt = maxtilt
    if tilt < mintilt: tilt = mintilt
    if spin < 0: spin += radians(360)
    if spin >= radians(360): spin -= radians(360)