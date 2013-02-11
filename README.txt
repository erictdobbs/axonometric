
##############################################################
##############################################################
                                                     
AXONOMETRIC EXPERIMENT                               
Eric Dobbs                                           
                                                     
                                                     
  This was an experiment with pygame, a graphics     
library for Python. Pygame provides great functions  
for 2-d graphics, but has no built-in support for    
3-d graphics.                                        
  My goal was to create a light-weight set of 
functions to easily plug right in to pygame's pre-
existing functions, and I may have gotten a bit
carried away.


##############################################################
##############################################################


SETUP/REQUIREMENTS

  This program requires Python 2.7 (free download
at http://www.python.org) and pygame (free download
at http://www.pygame.org). It was created for version
1.9.1 of pygame, but may work with newer versions.
  Once those are installed, make sure you have all four
files (main.py, axon.py, pygame3d.py, pygame3dGlobals.py)
downloaded. You can launch this program with the command 
	python main.py
once you navigate to the directory that you've downloaded
the files to.


##############################################################
##############################################################


CONTROLS

  Though this was mostly meant to be used for my other
small projects, I've included a little demo behavior to
show what this does. 

Arrow keys
  Left and right rotate the view, up and down tilt the view. 
WASD
  Lets you pan the view. Hold shift for quicker panning. 
Scroll wheel
  Zooms in and out, centered on the middle of the screen.
Left-click
  Drag while holding the left mouse button to pan the view.
Right-click
  Drag while holding the right mouse button to rotate and 
  tilt the view.


##############################################################
##############################################################


THE FILES

pygame3d.py
  This one does the heavy lifting. gridToScreen is
the crucial function, which takes a point (x,y,z) 
in a 3-d space and converts it to a point (x,y) on 
the 2-d plane of the screen. 
  The other functions in this file draw lines and 
polygons in that 3-d space. 

pygame3dGlobals.py
  This file holds the globally accessed variables 
needed for keeping track of how to view a 3-d space
through a 2-d plane. Mainly, the rotation (spin) and
pitch (tilt) of the view.

axon.py
  This file has a few functions that I've used for
creating some sample polygons. This one also handles
sorting polygons to be drawn in order, but doesn't 
handle general cases or ANY intersection cases.

main.py
  This file handles the interface and creates the
sample polygons.


##############################################################
##############################################################


