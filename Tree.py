import maya.cmds as cmds
import random as r
import math as m
import time

def set_pivot_to_bottom(obj_name):
    # Get the bounding box of the object
    bbox = cmds.exactWorldBoundingBox(obj_name)
    
    # Calculate the height of the object
    height = bbox[4] - bbox[1]
    
    # Calculate the new pivot point
    new_pivot = [0.0, -height/2, 0.0]
    
    # Set the pivot point of the object
    cmds.xform(obj_name, piv=new_pivot, r=True)
    return new_pivot

def createBranchNonRecursive(i, dec, branch, high, den):
    stack = []
    Pointy = PointPlacer()
    num = 0

    while True:
        if r.random() < i:
            if branch == "Trunk":
                Pointy.generatePointsAbove(branch, den, height)
            else:
                Pointy.generatePoints(branch, den)

            for point in Pointy.points:
                newName = branch + "_Branch" + str(num)
                print("Creating branch: " + newName)
                cmds.instance(branch, n=newName)
                cmds.parent(newName, branch)
                cmds.scale(i, i * 2, i)
                cmds.xform(newName, translation=(point[0] - pivot[0], point[1] - pivot[1], point[2] - pivot[2]), ws=1, ro=(str(90 * r.random()) + "deg", str(180 * r.random()) + "deg", str(90 * r.random()) + "deg"))                
                # Push the branch onto the stack along with its parameters
                stack.append((i - dec, dec, newName, high, den, num))
                num += 1

        elif branch != "Trunk":
            Pointy.generatePoints(branch, den)

            for point in Pointy.points:
                newName = branch + "_Leaf" + str(num)
                print("Creating leaf: " + newName)
                cmds.instance("Leaf1", n=newName)
                cmds.parent(newName, branch)
                cmds.xform(newName, translation=(point[0], point[1], point[2]), ws=1, ro=(str(180 * r.random()) + "deg", str(180 * r.random()) + "deg", str(180 * r.random()) + "deg"))
                num += 1

        if not stack:
            break

        # Pop the parameters from the stack
        i, dec, branch, high, den, num = stack.pop()
    
r.seed(1)

radius = 0.5
height = 50
ySub = 10
n = "Trunk"
Ta = 0.1
Sa = 0.5
Density = 0.1

# rnums = []
# for i in range(100000):
# 	rnums.append(r.random())
print("random numbers generated")


cmds.polyCylinder(n=n, sx=1, sy=ySub, sz=1, radius=radius, height=height)
pivot = set_pivot_to_bottom(n)
createBranchNonRecursive(0.4, 0.2, n, height, Density)

for i in range(10, ySub * 2 * 10, 10):
	cmds.polySelect(n, el=i)
	cmds.polyMoveEdge(tx=r.random() * Ta * 2 - Ta, tz=r.random() * Ta * 2 - Ta, sz=r.random() * Sa + 0.8, sx=r.random() * Sa + 0.8)

cmds.select(cl=1)
cmds.polySmooth(n, dv=2, kb=1)
set_pivot_to_bottom(n)
