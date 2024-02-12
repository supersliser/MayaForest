import maya.cmds as cmds
import random as r
import math as m

def set_pivot_to_bottom(obj_name):
    # Get the bounding box of the object
    bbox = cmds.exactWorldBoundingBox(obj_name)
    
    # Calculate the height of the object
    height = bbox[4] - bbox[1]
    
    # Calculate the new pivot point
    new_pivot = [0.0, (-height/2) + (height / 50), 0.0]
    
    # Set the pivot point of the object
    cmds.xform(obj_name, piv=new_pivot, r=True)
    return new_pivot

def distortBranch(name):
	# cmds.polySelect(name, el=10)
	# # cmds.scale(0.2, 1, 0.2, ls=1)
	# cmds.select(cl=1)
	# cmds.polySelect(name, el=ySub * 2 * 10)
	# cmds.scale(0.2, 1, 0.2, ls=1)
	# cmds.select(cl=1)
	for j in range(20, (ySub * 2 * 10) - 10, 20):
		cmds.polySelect(name, el=j)
		cmds.polyMoveEdge(tx=r.random() * Ta * 2 - Ta, tz=r.random() * Ta * 2 - Ta, sz=r.random() * Sa + 0.8, sx=r.random() * Sa + 0.8, ws=0)
		cmds.select(cl=1)

def editRadius(name, factor, i):
	i * 5
	for j in range(20, (ySub * 2 * 10) - 10, 20):
		cmds.polySelect(name, el=j)
		cmds.scale(i * (1 - (j / (ySub * 2 * 10))) + i, 1, i * (1 - (j / (ySub * 2 * 10))) + i)
		cmds.select(cl=1)

def createBranch(i, dec, branch, den):
    Pointy = PointPlacer()
    # Pointy.placePoints(branch)
    num = 0
    if r.random() < i:
        Pointy.generatePointsAbove(branch, den, 0.5)
        for point in Pointy.points:
            newName = f"{branch}_Branch{str(num)}"
            print(f"Creating branch: {newName}")
            cmds.polyCylinder(n=newName, sx=1, sy=ySub, sz=1, radius=radius, height=height * i)
            cmds.parent(newName, branch)
            if deform:
                distortBranch(newName)
                editRadius(newName, widthFactor, i)
            pivot = set_pivot_to_bottom(newName)
            createBranch(i - dec, dec, newName, den)
            cmds.xform(newName, translation=(point[0] - pivot[0], point[1] - pivot[1], point[2] - pivot[2]), ws=1)
            # # cmds.scale(i, i, i)
            # # cmds.rotate("45deg", 0, 0, r=1)
            cmds.xform(
                newName,
                ws=1,
                ro=(
                    f"{str(90 * r.random())}deg",
                    f"{str(360 * r.random())}deg",
                    f"{str(90 * r.random())}deg",
                ),
            )
            createAnim(newName, cmds.xform(newName, q=1, ro=1), (1 - i) * animAmount, animationStart, animationStop, animationStep)
            num+= 1
    elif branch != "Trunk" and leaves:
        Pointy.generatePointsAbove(branch, (1 - (den * 10)) / 2, 0.5)
        for point in Pointy.points:
            newName = f"{branch}_Leaf{str(num)}"
            print(f"Creating leaf: {newName}")
            cmds.duplicate("Leaf1", n=newName)
            cmds.parent(newName, branch)
            cmds.xform(newName, translation=(point[0], point[1], point[2]), ws=1)
            cmds.xform(
                newName,
                ro=(
                    f"{str(360 * r.random())}deg",
                    f"{str(360 * r.random())}deg",
                    f"{str(360 * r.random())}deg",
                ),
            )
            createAnim(newName, cmds.xform(newName, q=1, ro=1), animAmount, animationStart, animationStop, animationStep)
            num += 1

def createAnim(itemName, itemRotation, rotationFactor, start, stop, step):
	for i in range(start, stop, step * 2):
		cmds.setKeyframe(itemName, at="rotateX", time=i, v=itemRotation[0])
		cmds.setKeyframe(itemName, at="rotateY", time=i, v=itemRotation[1])
		cmds.setKeyframe(itemName, at="rotateZ", time=i, v=itemRotation[2])
		cmds.setKeyframe(itemName, at="rotateX", time=i + step, v=itemRotation[0] + ((r.random() * rotationFactor) - rotationFactor/2))
		cmds.setKeyframe(itemName, at="rotateY", time=i + step, v=itemRotation[1] + ((r.random() * rotationFactor) - rotationFactor/2))
		cmds.setKeyframe(itemName, at="rotateZ", time=i + step, v=itemRotation[2] + ((r.random() * rotationFactor) - rotationFactor/2))
	
	

r.seed(2)

radius = 1
height = 40
ySub = 10
n = "Trunk"
Ta = 0.1
Sa = 0.5
Density = 0.5
leaves = True
deform = True
animAmount = 10
widthFactor = 2
animationStart = 0
animationStop = 200
animationStep = 50

try:
    cmds.delete(n)
except:
	pass
cmds.polyCylinder(n=n, sx=1, sy=ySub, sz=1, radius=radius, height=height)


createBranch(0.8, 0.2, n, Density / 10)

editRadius(n, 1, 2)


distortBranch(n)

cmds.select(n)
cmds.polySmooth(dv=2, kb=1)
set_pivot_to_bottom(n)

cmds.playbackOptions(minTime=animationStart, maxTime=animationStop, l="continuous")

cmds.refresh(f=1)