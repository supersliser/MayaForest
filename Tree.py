import maya.cmds as cmds
import random as r
import math as m

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

def createBranch(i, dec, branch, high, den):
	Pointy = PointPlacer()
	# Pointy.placePoints(branch)
	num = 0
	if r.random() < i:
		Pointy.generatePoints(branch, den)
		for point in Pointy.points:
			newName = branch + "_Branch" + str(num)
			print("Creating branch: " + newName)
			cmds.polyCylinder(n=newName, sx=1, sy=ySub, sz=1, radius=radius - i, height=high * i)
			cmds.parent(newName, branch)
			pivot = set_pivot_to_bottom(newName)
			cmds.xform(newName, translation=(point[0] - pivot[0], point[1] - pivot[1], point[2] - pivot[2]), ws=1)
			# # cmds.scale(i, i, i)
			# # cmds.rotate("45deg", 0, 0, r=1)
			cmds.xform(newName, ro=(str(90 * r.random()) + "deg", str(180 * r.random()) + "deg", str(90 * r.random()) + "deg"))

			# for j in range(10, (ySub * 2 * 10), 10):
			# 	cmds.polySelect(newName, el=j)
			# 	cmds.polyMoveEdge(tx=r.random() * Ta * 2 - Ta, tz=r.random() * Ta * 2 - Ta, sz=r.random() * Sa + 0.8, sx=r.random() * Sa + 0.8)

			# cmds.select(cl=1)
			# cmds.polySmooth(n, dv=2, kb=1)
			createBranch(i - dec, dec, newName, high, den)
	elif branch != "Trunk":
		Pointy.generatePoints(branch, 1 - den)
		for point in Pointy.points:
			newName = branch + "_Leaf" + str(num)
			print("Creating leaf: " + newName)
			cmds.instance("Leaf1", n=newName)
			cmds.parent(newName, branch)
			cmds.xform(newName, translation=(point[0], point[1], point[2]), ws=1)
			cmds.xform(newName, ro=(str(180 * r.random()) + "deg", str(180 * r.random()) + "deg", str(180 * r.random()) + "deg"))
		num += 1
# cmds.file( f=True, new=True )

r.seed(1)

radius = 0.5
height = 50
ySub = 10
n = "Trunk"
Ta = 0.1
Sa = 0.5
Density = 0.05


cmds.polyCylinder(n=n, sx=1, sy=ySub, sz=1, radius=radius, height=height)

for i in range(10, ySub * 2 * 10, 10):
	cmds.polySelect(n, el=i)
	cmds.polyMoveEdge(tx=r.random() * Ta * 2 - Ta, tz=r.random() * Ta * 2 - Ta, sz=r.random() * Sa + 0.8, sx=r.random() * Sa + 0.8)

cmds.select(cl=1)
cmds.polySmooth(n, dv=2, kb=1)
set_pivot_to_bottom(n)
createBranch(0.2, 0.1, n, height, Density)