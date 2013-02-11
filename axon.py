
import random
from math import *
import pygame3d as p3d
import pygame3dGlobals as ag

def drawCubeList(cubes):
    # drawCubes orders the provided list of cubes such that they're drawn back to front
    if ag.spin >= radians(0) and ag.spin < radians(90): cubes.sort(key=lambda i: -i[0][0]-i[0][1])
    elif ag.spin >= radians(90) and ag.spin < radians(180): cubes.sort(key=lambda i: -i[0][0]+i[0][1])
    elif ag.spin >= radians(180) and ag.spin < radians(270): cubes.sort(key=lambda i: i[0][0]+i[0][1])
    elif ag.spin >= radians(270) and ag.spin < radians(360): cubes.sort(key=lambda i: i[0][0]-i[0][1])
    for cube in cubes: 
        drawCube(cube[0], cube[1], cube[2])
    
def drawCube((x1,y1,z1),(x2,y2,z2),color=ag.LINECOLOR):
    # drawCube takes two opposite corners of a cube and a color and
    # draws two front faces (based on rotation), then the top face
    if ag.spin < radians(90) or ag.spin > radians(270): 
        p3d.gridDrawPolygon([(x1,y1,z1),(x1,y1,z2),(x2,y1,z2),(x2,y1,z1)],color)
    if ag.spin > radians(90) and ag.spin < radians(270): 
        p3d.gridDrawPolygon([(x1,y2,z1),(x1,y2,z2),(x2,y2,z2),(x2,y2,z1)],color)
    if ag.spin < radians(180): 
        p3d.gridDrawPolygon([(x1,y1,z1),(x1,y1,z2),(x1,y2,z2),(x1,y2,z1)],color)
    if ag.spin > radians(180): 
        p3d.gridDrawPolygon([(x2,y1,z1),(x2,y1,z2),(x2,y2,z2),(x2,y2,z1)],color)
    p3d.gridDrawPolygon([(x1,y1,z2),(x2,y1,z2),(x2,y2,z2),(x1,y2,z2)],color)
    
def genSampleCubes(size):
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
            
def drawTerrain(terrainFaces, terrainShades):
    if ag.spin >= radians(0) and ag.spin < radians(90): terrainFaces.sort(key=lambda i: -i[0][0]-i[0][1]-.5*i[1][0])
    elif ag.spin >= radians(90) and ag.spin < radians(135): terrainFaces.sort(key=lambda i: i[0][1]-i[0][0]-.5*i[1][0])
    elif ag.spin >= radians(135) and ag.spin < radians(180): terrainFaces.sort(key=lambda i: i[0][1]-i[0][0]+.5*i[1][0])
    elif ag.spin >= radians(180) and ag.spin < radians(270): terrainFaces.sort(key=lambda i: i[0][0]+i[0][1]+.5*i[1][0])
    elif ag.spin >= radians(270) and ag.spin < radians(315): terrainFaces.sort(key=lambda i: i[0][0]-i[0][1]+.5*i[1][0])
    elif ag.spin >= radians(315) and ag.spin < radians(360): terrainFaces.sort(key=lambda i: i[0][0]-i[0][1]-.5*i[1][0])
    for face in terrainFaces: p3d.gridDrawPolygon(face, terrainShades[face])
    
def genSampleTerrain(size, scale=50):
    array = []
    for ii in range(size):
        array.append([])
        for jj in range(size):
            height = random.randint(50,90)
            height +=  2*(size/2 - ii)*(size/2 - jj) 
            if height < 0: height = 0
            array[ii].append( ((ii-size/2)*scale, (jj-size/2)*scale, height) )
    return array
    
