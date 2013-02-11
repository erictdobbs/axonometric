from pygame import *
import random
from math import *
from pygame.locals import *
import pygame3d as p3d
import pygame3dGlobals as ag
import axon as ax

#sampleCubes = genSampleCubes(5)

sampleTerrain = ax.genSampleTerrain(20,50)
terrainFaces, terrainShades = ax.prepareTerrain(sampleTerrain)
    
    
demoMode = True
    
done = False
clock = time.Clock()
key.set_repeat(200,3) # Allows user to hold down keyboard keys
heldMouseButtons = [0, False, False, False, False, False]
shiftHeld = False
mousescreenX = 0
mousescreenY = 0
dragStartX = 0
dragStartY = 0
spinTimer = 0
spinDegrees = [0,1,6,3,1.5,1,0.5,0.5,0.5,0.5,0.5]
tiltTimer = 0
tiltDegrees = [0,0.5,5.5,1.5,0.5,0.5,0.5,0.5,0.5]
zoomTimer = 0
zoomRates = [0, 1.02, 1.20, 1.11, 1.02, 1.02, 1.02, 1.02, 1.02]
while done==False:
    clock.tick()
    ag.screen.fill(ag.BLACK)
    
    ########### Sample grid drawing ##########################################
    numGridLines = 20
    gridSize = 50
    for ii in range(-numGridLines,numGridLines+1):
        p3d.gridDrawLine((ii * gridSize, -gridSize * numGridLines,0), (ii * gridSize, numGridLines * gridSize,0))
    for jj in range(-numGridLines,numGridLines+1): 
        p3d.gridDrawLine((-gridSize * numGridLines, jj * gridSize,0), (numGridLines * gridSize, jj * gridSize,0))
    p3d.gridDrawLine((0, -gridSize * numGridLines,0), (0, numGridLines * gridSize,0), ag.RED)
    p3d.gridDrawLine((-gridSize * numGridLines, 0,0), (numGridLines * gridSize, 0,0), ag.RED)
       
    ##########################################################################
    
    #drawCubeList(sampleCubes)
    ax.drawTerrain(terrainFaces, terrainShades)
       
    ##########################################################################
    
    # Draw white crosshairs
    p3d.screenDrawLine((ag.screenwidth/2-3,ag.screenheight/2),(ag.screenwidth/2+3,ag.screenheight/2),color=ag.WHITE)
    p3d.screenDrawLine((ag.screenwidth/2,ag.screenheight/2-3),(ag.screenwidth/2,ag.screenheight/2+3),color=ag.WHITE)
    
    p3d.screenDrawStrings( ("Axonometric Experiment by Eric Dobbs",
                            "FPS: " + str(round(clock.get_fps(),1)),
                            "spin: "+ str(degrees(ag.spin)),
                            "tilt: "+ str(degrees(ag.tilt)),
                            "zoom: "+ str(ag.zoom),
                            "horizontal offset: " + str(ag.horoff),
                            "vertical offset: " + str(ag.veroff)
                            ) )
    if demoMode == True:
        ag.spin += radians(0.5)
        ag.tilt = 0.1*sin( (ag.spin-radians(50)) ) + radians(75)
    if spinTimer != 0:
        sign = spinTimer/abs(spinTimer)
        ag.spin += sign*radians(spinDegrees[sign*spinTimer])
        spinTimer += sign
        if abs(spinTimer) == len(spinDegrees): spinTimer = 0
    if tiltTimer != 0:
        sign = tiltTimer/abs(tiltTimer)
        ag.tilt += sign*radians(tiltDegrees[sign*tiltTimer])
        tiltTimer += sign
        if abs(tiltTimer) == len(tiltDegrees): tiltTimer = 0
    if zoomTimer != 0:
        if zoomTimer > 0:
            ag.zoom *= zoomRates[zoomTimer]
            zoomTimer += 1
        else:
            ag.zoom /= zoomRates[-zoomTimer]
            zoomTimer -= 1
        if abs(zoomTimer) == len(zoomRates): zoomTimer = 0
        
    for myevent in event.get(): # User did something
        if myevent.type == QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop
        if myevent.type == MOUSEMOTION:
            mousescreenX = myevent.pos[0]
            mousescreenY = myevent.pos[1]
            if heldMouseButtons[1] == True: 
                # Drag to pan view
                deltaX = (mousescreenX - dragStartX) * cos(ag.tilt)
                deltaY = mousescreenY - dragStartY 
                radius = sqrt(deltaX**2+deltaY**2)
                angle = atan2(deltaY,deltaX)+ag.spin
                ag.horoff -= ( radius * cos(angle) / cos(ag.tilt) ) / ag.zoom
                ag.veroff += ( radius * sin(angle) / cos(ag.tilt) ) / ag.zoom
                dragStartX = mousescreenX
                dragStartY = mousescreenY
            if heldMouseButtons[3] == True:
                # Drag to tilt and spin
                deltaX = mousescreenX - dragStartX
                deltaY = mousescreenY - dragStartY 
                ag.tilt -= radians(deltaY)/10.0
                ag.spin += radians(deltaX)/5.0
                dragStartX = mousescreenX
                dragStartY = mousescreenY
        if myevent.type == MOUSEBUTTONDOWN and sum(heldMouseButtons) == 0:
            demoMode = False
            heldMouseButtons[myevent.button] = True
            if myevent.button == 4 and zoomTimer == 0: zoomTimer = 1
            if myevent.button == 5 and zoomTimer == 0: zoomTimer = -1
            if sum(heldMouseButtons) > 0: 
                dragStartX = mousescreenX
                dragStartY = mousescreenY
        if myevent.type == MOUSEBUTTONUP:
            heldMouseButtons[myevent.button] = False
            
        if myevent.type == KEYDOWN:
            demoMode = False
            shiftHeld = key.get_mods() & KMOD_SHIFT
            if myevent.key == K_q: 
                done=True
            # Keys LEFT and RIGHT rotate the view
            if myevent.key == K_LEFT and spinTimer == 0:
                if shiftHeld:
                    ag.spin += radians(.5)
                    if ag.spin >= radians(360): ag.spin -= radians(360)
                else: spinTimer = 1
            if myevent.key == K_RIGHT and spinTimer == 0:
                if shiftHeld: 
                    ag.spin -= radians(.5)
                    if ag.spin < 0: ag.spin += radians(360)
                else: spinTimer = -1
            # Keys UP and DOWN tilt the view
            if myevent.key == K_UP and tiltTimer == 0: 
                if shiftHeld: 
                    ag.tilt += radians(.2)
                    if ag.tilt > radians(90): ag.tilt = radians(90)
                else: tiltTimer = 1
            if myevent.key == K_DOWN and tiltTimer == 0: 
                if shiftHeld: 
                    ag.tilt -= radians(.2)
                    if ag.tilt < 0: ag.tilt = 0
                else: tiltTimer = -1
            # Keys w a s d pan the grid
            multiplier = 1
            if shiftHeld: multiplier = 25
            if myevent.key == K_a: 
                ag.veroff += multiplier* sin(ag.spin)
                ag.horoff -= multiplier* cos(ag.spin)
            if myevent.key == K_d: 
                ag.veroff -= multiplier* sin(ag.spin)
                ag.horoff += multiplier* cos(ag.spin)
            if myevent.key == K_w: 
                ag.veroff += multiplier* cos(ag.spin)/cos(ag.tilt)
                ag.horoff += multiplier* sin(ag.spin)/cos(ag.tilt)
            if myevent.key == K_s: 
                ag.veroff -= multiplier* cos(ag.spin)/cos(ag.tilt)
                ag.horoff -= multiplier* sin(ag.spin)/cos(ag.tilt)
                
            if myevent.key == K_SPACE: 
                print ag.tilt, ag.spin
    ag.checkBounds()
    ag.display.flip()
    
    
   ##########################
   # TO DO:
   # * Create quick draw func - triangle?, vectors
   # * ag.zoom
   # * Mouse functionality - pan w/m3 click/drag, ag.zoom w/m3 scroll
   # * edit items, click+drag to move vectors?
   # * terrain!
   # Something is wrong, are x and y swapped in the coordinate system??