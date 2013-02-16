
import random
from math import *
import pygame3d as p3d
import pygame3dGlobals as ag    



def genSampleCubes(size=5):
    def randomColor(randSeed="none"):
        if randSeed=="none": random.seed()
        else:random.seed(randSeed)
        return [random.randint(0,255),random.randint(0,255),random.randint(0,255)]
    sampleCubes = []
    for ii in reversed(range(-size/2,size/2+2)):
        for jj in reversed(range(-size/2,size/2+2)):
            random.seed()
            sampleCubes.append(((ii*50,jj*50,0),((ii+0.5)*50,(jj+0.5)*50,random.randint(10,100)), randomColor(10*ii+jj)))
    return sampleCubes

def drawCubeList(cubes, style="filledwire"):
    # drawCubes orders the provided list of cubes such that they're drawn back to front
    if ag.spin >= radians(0) and ag.spin < radians(90): cubes.sort(key=lambda i: -i[0][0]-i[0][1])
    elif ag.spin >= radians(90) and ag.spin < radians(180): cubes.sort(key=lambda i: -i[0][0]+i[0][1])
    elif ag.spin >= radians(180) and ag.spin < radians(270): cubes.sort(key=lambda i: i[0][0]+i[0][1])
    elif ag.spin >= radians(270) and ag.spin < radians(360): cubes.sort(key=lambda i: i[0][0]-i[0][1])
    for cube in cubes: 
        drawCube(cube[0], cube[1], cube[2], style)
    
def drawCube((x1,y1,z1),(x2,y2,z2),color=ag.LINECOLOR, style="filledwire"):
    # drawCube takes two opposite corners of a cube and a color and
    # draws two front faces (based on rotation), then the top face
    if ag.spin < radians(90) or ag.spin > radians(270): 
        p3d.gridDrawPolygon([(x1,y1,z1),(x1,y1,z2),(x2,y1,z2),(x2,y1,z1)],color,style)
    if ag.spin > radians(90) and ag.spin < radians(270): 
        p3d.gridDrawPolygon([(x1,y2,z1),(x1,y2,z2),(x2,y2,z2),(x2,y2,z1)],color,style)
    if ag.spin < radians(180): 
        p3d.gridDrawPolygon([(x1,y1,z1),(x1,y1,z2),(x1,y2,z2),(x1,y2,z1)],color,style)
    if ag.spin > radians(180): 
        p3d.gridDrawPolygon([(x2,y1,z1),(x2,y1,z2),(x2,y2,z2),(x2,y2,z1)],color,style)
    p3d.gridDrawPolygon([(x1,y1,z2),(x2,y1,z2),(x2,y2,z2),(x1,y2,z2)],color,style)

    
    
def genSampleTerrain(size, scale=50):
    array = []
    randomshift = random.randint(-scale,scale)
    for ii in range(size):
        array.append([])
        for jj in range(size):
            height = random.randint(50,90)
            height +=  2*(size/2 - ii)*(size/2 - jj) + randomshift
            if height < 0: height = 0
            array[ii].append( ((ii-size/2)*scale, (jj-size/2)*scale, height) )
    return array
    
def prepareTerrain(array, color=ag.BLUE):
    terrainFaces = []
    terrainShades = {}
    # each element is of the form [ coord, coord, coord ], each coord of the form ( pt, pt, pt)
    for ii in range(len(array)-1):
        for jj in range(len(array[ii])-1):
            face1 = ( array[ii+1][jj], array[ii][jj], array[ii][jj+1] )
            face2 = ( array[ii+1][jj], array[ii+1][jj+1], array[ii][jj+1] )
            terrainFaces.append( face1 )
            terrainFaces.append( face2 )
            terrainShades[face1] = p3d.shadedPlaneColor( p3d.planeNormal(face1), color )
            terrainShades[face2] = p3d.shadedPlaneColor( p3d.planeNormal(face2), color )
    return terrainFaces, terrainShades

def drawTerrain(terrainFaces, terrainShades, style="flat"):
    if ag.spin >= radians(0) and ag.spin < radians(90): terrainFaces.sort(key=lambda i: -i[0][0]-i[0][1]-.5*i[1][0])
    elif ag.spin >= radians(90) and ag.spin < radians(135): terrainFaces.sort(key=lambda i: i[0][1]-i[0][0]-.5*i[1][0])
    elif ag.spin >= radians(135) and ag.spin < radians(180): terrainFaces.sort(key=lambda i: i[0][1]-i[0][0]+.5*i[1][0])
    elif ag.spin >= radians(180) and ag.spin < radians(270): terrainFaces.sort(key=lambda i: i[0][0]+i[0][1]+.5*i[1][0])
    elif ag.spin >= radians(270) and ag.spin < radians(315): terrainFaces.sort(key=lambda i: i[0][0]-i[0][1]+.5*i[1][0])
    elif ag.spin >= radians(315) and ag.spin < radians(360): terrainFaces.sort(key=lambda i: i[0][0]-i[0][1]-.5*i[1][0])
    for face in terrainFaces: p3d.gridDrawPolygon(face, terrainShades[face], style)
    
    
    
def genSierpinski(iterations, size):
    numLevels = int(pow(2,iterations))
    heightPerLevel = size * 1.0 / numLevels
    sizeOfSide = size * 1.0 / numLevels
    peaks = []
    for level in range(numLevels):
        base = heightPerLevel * (numLevels - level - 1)
        top = base + heightPerLevel
        if level == 0: peaks.append( (0,0,top) )
        else: 
            previousCorners = []
            for point in peaks:
                if point[2] == top + heightPerLevel:
                    previousCorners.append( (point[0]+sizeOfSide/2,point[1]+sizeOfSide/2,point[2]-heightPerLevel) )
                    previousCorners.append( (point[0]-sizeOfSide/2,point[1]+sizeOfSide/2,point[2]-heightPerLevel) )
                    previousCorners.append( (point[0]-sizeOfSide/2,point[1]-sizeOfSide/2,point[2]-heightPerLevel) )
                    previousCorners.append( (point[0]+sizeOfSide/2,point[1]-sizeOfSide/2,point[2]-heightPerLevel) )
            for point in previousCorners: # If only one pyramid touched this point, spawn new pyramid
                if previousCorners.count(point) == 1: peaks.append( point )
    return peaks
    
def drawSierpinski(peaks, color=ag.LINECOLOR, style="filledwire"):
    def shade(color, ratio=1):
        newcolor = [int( (x*ratio) ) for x in color]
        for x in range(len(newcolor)):
            if newcolor[x] > 255: newcolor[x] = 255
            if newcolor[x] < 0: newcolor[x] = 0
        return newcolor
    heightPerLevel = 1; sizeOfSide=1; top=0
    if len(peaks) > 1: 
        peaks.sort(key=lambda i: -i[2] )
        heightPerLevel = peaks[0][2] - peaks[1][2]
        sizeOfSide = 2 * abs( peaks[0][0] - peaks[1][0] )
        top = peaks[0][2]
    numLevels = top / heightPerLevel
    # Sort peaks by draw distance
    if ag.spin >= radians(0) and ag.spin < radians(90): 
        peaks.sort(key=lambda i: -i[0]-i[1]+1000*i[2] )
    elif ag.spin >= radians(90) and ag.spin < radians(180): 
        peaks.sort(key=lambda i: -i[0]+i[1]+1000*i[2] )
    elif ag.spin >= radians(180) and ag.spin < radians(270): 
        peaks.sort(key=lambda i: i[0]+i[1]+1000*i[2] )
    elif ag.spin >= radians(270) and ag.spin < radians(360): 
        peaks.sort(key=lambda i: i[0]-i[1]+1000*i[2] )
    # For each peak, draw faces in order of draw distance
    faces = [] 
    for point in peaks:
        base = point[2] - heightPerLevel
        x1 = point[0]-sizeOfSide/2
        y1 = point[1]-sizeOfSide/2
        x2 = point[0]+sizeOfSide/2
        y2 = point[1]+sizeOfSide/2
        faces.append( ( point, (x1,y1,base), (x2,y1,base) ) )
        faces.append( ( point, (x1,y2,base), (x2,y2,base) ) )
        faces.append( ( point, (x1,y1,base), (x1,y2,base) ) )
        faces.append( ( point, (x2,y1,base), (x2,y2,base) ) )
        if ag.spin < radians(45): faces.sort(key=lambda i: -i[1][0]-3*i[1][1] - i[2][0]-3*i[2][1] )
        elif ag.spin < radians(90): faces.sort(key=lambda i: -3*i[1][0]-i[1][1] - 3*i[2][0]-i[2][1] )
        elif ag.spin < radians(135): faces.sort(key=lambda i: -3*i[1][0]+i[1][1] - 3*i[2][0]+i[2][1] )
        elif ag.spin < radians(180): faces.sort(key=lambda i: -i[1][0]+3*i[1][1] - i[2][0]+3*i[2][1] )
        elif ag.spin < radians(225): faces.sort(key=lambda i: i[1][0]+3*i[1][1] + i[2][0]+3*i[2][1] )
        elif ag.spin < radians(270): faces.sort(key=lambda i: 3*i[1][0]+i[1][1] + 3*i[2][0]+i[2][1] )
        elif ag.spin < radians(315): faces.sort(key=lambda i: 3*i[1][0]-i[1][1] + 3*i[2][0]-i[2][1] )
        else: faces.sort(key=lambda i: i[1][0]-3*i[1][1] + i[2][0]-3*i[2][1] )
        #faces.sort(key=lambda i: -i[0]+i[1]-10000*i[2])
        for ii in range(len(faces)): 
            drawColor = color
            if point[2] != top: drawColor = shade(color, 1.0*point[2]/top )
            p3d.gridDrawPolygon(faces[0], drawColor, style)
            faces.pop(0)
        
        
        