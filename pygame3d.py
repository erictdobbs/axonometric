

from pygame import *
from math import *
import pygame3dGlobals as ag

def crossProduct( (x1,y1,z1), (x2,y2,z2) ):
    # Calculates the cross product of two vectors
    xcross = (y1*z2 - z1*y2)
    ycross = (z1*x2 - x1*z2)
    zcross = (x1*y2 - y1*x2)
    return (xcross,ycross,zcross)
    
def planeNormal( ((x1,y1,z1), (x2,y2,z2), (x3,y3,z3)) ):
    # Calculates the normal vector of the plane defined by three points
    return crossProduct( (x1-x2,y1-y2,z1-z2), (x1-x3,y1-y3,z1-z3) )
    
def shadedPlaneColor((x,y,z),color):
    # Returns a color darkened based on its angle in relation to the z-axis
    radius = sqrt(x**2+y**2)
    angle = atan2(z,radius)
    shade = abs(angle/(radians(90)))
    return [int(color[0]*shade),int(color[1]*shade),int(color[2]*shade)]

def screenDrawLine((x1,y1),(x2,y2),color=ag.LINECOLOR):
    # Draws a single line to the coordinates based on the screen's
    #   coordinate system
    draw.aaline(ag.screen,color,(x1,y1),(x2,y2))
	
def screenDrawPolygon(pointList,color=ag.LINECOLOR,style="flat"):
    # Draws a polygon to the coordinates based on the screen's
    #   coordinate system
    darkercolor = [color[0]/2, color[1]/2, color[2]/2]
    lightercolor = [(color[0]+255)/2, (color[1]+255)/2, (color[2]+255)/2]
    if style != "wire": draw.polygon(ag.screen,color,pointList)
    if style != "flat": draw.aalines(ag.screen,darkercolor,True,pointList)
	  
def screenDrawStrings(stringList, alignment="topleft", color=ag.WHITE):
    myfont = font.SysFont("Courier", 10)
    lineCounter = 0
    for string in stringList:
        label = myfont.render(string, 1, color)
        if alignment=="topleft": ag.screen.blit(label,(5, 5 + 10*lineCounter) )
        elif alignment=="bottomleft": ag.screen.blit(label,(5, ag.screenheight - 10*lineCounter - 10) )
        lineCounter += 1

gridScreenCoords = {}
# gridScreenCoords dictionary increases fps by about 5% by storing any previously
# seen combination of coordinates, spin, and tilt with its appropriate screen
# coordinate. A sort of manual cache
def gridToScreen((gridx,gridy,gridz)):
    # Translates a 3-d grid coordinate to a 2-d screen coordinate for drawing
    global gridScreenCoords
    try:
        (screenx,screeny) = gridScreenCoords[(gridx,gridy,gridz,ag.spin,ag.tilt)]
    except(KeyError):
        radius = sqrt(gridx**2+gridy**2)
        oldangle = atan2(gridy,gridx)
        newangle = oldangle + ag.spin
        screenx = radius * cos(newangle) + ag.screenwidth/2
        screeny = -(radius * sin(newangle)) * cos(ag.tilt) - gridz*sin(ag.tilt) + ag.screenheight/2
        gridScreenCoords[(gridx,gridy,gridz,ag.spin,ag.tilt)] = (screenx,screeny)
    return((int(screenx),int(screeny)))
    
def gridDrawText(str, (gridx,gridy,gridz)):
    # Draws text to the coordinates based on the in-game
    #   grid's coordinate system. Takes the tilt, spin, and
    #   zoom and pan into account automatically
    (screenx,screeny) = gridToScreen(((gridx-ag.horoff)*ag.zoom, (gridy-ag.veroff)*ag.zoom, gridz*ag.zoom))
    myfont = font.SysFont("Courier", 10)
    label = myfont.render(str, 1, [255,255,255])
    ag.screen.blit(label,(screenx,screeny))
	
def gridDrawLine((x1,y1,z1),(x2,y2,z2),color=ag.LINECOLOR):
    # Draws a line to the coordinates based on the in-game
    #   grid's coordinate system. Takes the tilt, spin, and
    #   zoom and pan into account automatically
    point1 = gridToScreen(((x1-ag.horoff)*ag.zoom, (y1-ag.veroff)*ag.zoom, z1*ag.zoom))
    point2 = gridToScreen(((x2-ag.horoff)*ag.zoom, (y2-ag.veroff)*ag.zoom, z2*ag.zoom))
    screenDrawLine(point1, point2, color)
	
def gridDrawPolygon(pointList, color=ag.LINECOLOR, style="flat"):
    # Draws a polygon to the coordinates based on the in-game
    #   grid's coordinate system. Takes the tilt, spin, and
    #   zoom and pan into account automatically
    if len(pointList) < 3: return
    newPoints = []
    for point in pointList:
        newPoints.append(gridToScreen(((point[0]-ag.horoff)*ag.zoom, (point[1]-ag.veroff)*ag.zoom, point[2]*ag.zoom)))
    screenDrawPolygon(newPoints, color, style)
    