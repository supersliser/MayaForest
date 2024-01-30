import maya.cmds as cmds
import random as r
import math as m

def createBranch(i, dec, branch, num):
	if r.random() < i:
		newName = branch + "_Branch" + str(num)
		print("Creating branch: " + newName)
		cmds.polyCylinder(n=newName, sx=1, sy=ySub * i + 1, sz=1, radius=radius * (1 - i), height=height * (1 - i))
		cmds.parent(newName, branch, r=1, add=1)

		for i in range(10, ySub * 2 * 10, 10):
			cmds.polySelect(, el=i)
			cmds.polyMoveEdge(tx=i * (r.random() * Ta * 2 - Ta), tz=i * (r.random() * Ta * 2 - Ta), sz=i * (r.random() * Sa + 0.8), sx=i * (r.random() * Sa + 0.8))

		cmds.select(cl=1)
		cmds.polySmooth(n, dv=2, kb=1)

		cmds.select(newName)
		cmds.rotate("45deg", 0, 0, r=1)
		cmds.move(r=1, y=i * 50, os=1)
		cmds.select(cl=1)
		createBranch(i - dec, dec, newName, 1)

cmds.file( f=True, new=True )

r.seed(1)

radius = 0.5
height = 20
ySub = 10
n = "Trunk"
Ta = 0.1
Sa = 0.5
minBranch = (ySub * 2 * 10) - 300

cmds.polyCylinder(n=n, sx=1, sy=ySub, sz=1, radius=radius, height=height)

for i in range(10, ySub * 2 * 10, 10):
	cmds.polySelect(n, el=i)
	cmds.polyMoveEdge(tx=r.random() * Ta * 2 - Ta, tz=r.random() * Ta * 2 - Ta, sz=r.random() * Sa + 0.8, sx=r.random() * Sa + 0.8)

cmds.select(cl=1)
cmds.polySmooth(n, dv=2, kb=1)

createBranch(0.5, 0.1, n, 1)