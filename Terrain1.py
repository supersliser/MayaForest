import maya.cmds as cmds
import random as r

#Generates a random number between the amplitude and its negative counterpart (e.g. from -1 to 1)
def getRandomNumber(a):
    return (r.random() * a * 2) - a

#Resets the view on each run
cmds.file( f=True, new=True )

#The name of the object in the outliner
name = "Terrain"
#The width and height of the plane
xSize = 150
ySize = 150
#The subdivision of the plane
xSub = 5
ySub = 5
#The difference between the lowest and highest possible points
amplitude = 5

#Creates a horizonatally flat plane
cmds.polyPlane(n=name, w=xSize, h=ySize, sx=xSub, sy=ySub)
cmds.setAttr(name+".rotate", 0, 90, 0, type="double3")

#iterates through each vertex and moves it my a randomly generated amount
for y in range(1, ySub):
    for x in range(1, xSub):
        v = x + (y * xSub)
        cmds.polyMoveVertex(name+".vtx[" + str(v) + "]", ty=getRandomNumber(amplitude / 2))

#smooths the resulting mesh
cmds.polySmooth(n=name, dv=4, kb=0)