import contextlib
import maya.cmds as cmds
import random as r
import math as m

class TextInput:
    inpControl = 0
    default = ""
    def __init__(self, name, default, nullable=False):
        if not nullable:
            self.inpControl = cmds.textFieldGrp(label=name, tx=default, tcc=self.checkEmpty)
            self.default = default
        else:
            self.inpControl = cmds.textFieldGrp(label=name, tx=default)
    def checkEmpty(self, *args):
        if self.getValue() == "":
            cmds.textFieldGrp(self.inpControl, e=1, tx=self.default)
    def getValue(self):
        return cmds.textFieldGrp(self.inpControl, q=1, tx=1)
    
class IntInput:
    inpControl = 0
    def __init__(self, name, minValue, maxValue, defaultValue = 0):
        self.inpControl = cmds.intSliderGrp(l=name, f=1, min=minValue, max=maxValue, v=defaultValue)
    def getValue(self):
        return cmds.intSliderGrp(self.inpControl, q=1, v=1)
    
class FloatInput:
    inpControl = 0
    def __init__(self, name, minValue, maxValue, defaultValue = 0):
        self.inpControl = cmds.floatSliderGrp(l=name, f=1, min=minValue, max=maxValue, v=defaultValue, cw=[1, 300])
    def getValue(self):
        return cmds.floatSliderGrp(self.inpControl, q=1, v=1)
    
class BoolInput:
    inpControl = 0
    def __init__(self, name, defaultState):
        self.inpControl = cmds.checkBox(l=name, v=defaultState)
    def getValue(self):
        return cmds.checkBox(self.inpControl, q=1, v=1)
    
class terrainUI:
    def createTerrainUI(self):
        self.WinControl = cmds.window(t="TerrainUI")
        cmds.columnLayout(adj=True)
        self.NameInput = TextInput("Name of terrain", "Terrain")
        self.WidthInput = IntInput("Width of terrain", 1, 2000, 150)
        self.DepthInput = IntInput("Depth of terrain", 1, 2000, 150)
        self.XSubdivision = IntInput("Number of subdivisions on X axis", 1, 200, 5)
        self.YSubdivision = IntInput("Number of subdivisions on Y axis", 1, 200, 5)
        self.TreeVariants = IntInput("Number of different types of trees to use", 1, 10, 4)
        self.Amplitude = FloatInput("Difference between highest point and lowest point in terrain", 1, 10, 5)
        self.Tolerance = FloatInput("Percentage of vertices to generate trees", 0, 1, 0.4)
        self.Seed = IntInput("Randomness seed", 1, 9999999, 1)
        self.GenerateButton = cmds.button(l="Generate Terrain", c=self.GenerateTerrain)
        self.CancelButton = cmds.button(l="Cancel", c=self.Cancel)
        cmds.showWindow(self.WinControl)
    def Cancel(self, *args):
        cmds.deleteUI(self.WinControl)
        
    def GenerateTerrain(self, *args):
        r.seed(self.Seed.getValue())
        terrainItem = Terrain(self.NameInput.getValue(), self.XSubdivision.getValue(), self.YSubdivision.getValue())
        terrainItem.generateTerrain(self.WidthInput.getValue(), self.DepthInput.getValue(), self.Amplitude.getValue())
        points = terrainItem.generateRandomSurfacePoints(self.Tolerance.getValue())
        trees = []
        for t in range(self.TreeVariants.getValue()):
            temp = Tree(terrainItem.name + "_Tree" + str(t), r.uniform(0.5, 1.5), True, 50, 0, 250, 50, 0.7)
            temp.generateTree(r.uniform(0.15, 0.25), 1, r.uniform(2, 4), self.Seed.getValue() + t, (0, 0, 0), terrainItem.name, r.uniform(15, 40))
            trees.append(temp)
        for p in points:
            trees[r.randint(0, len(trees))].placeTree(p, terrainItem.name)
        terrainItem.smooth()
        cmds.deleteUI(self.WinControl)

class Tree:
    name = ""
    radius = 0
    leaves = False
    animAmount = 0
    animStart = 0
    animStop = 0
    animStep = 0
    genHeight = 0
    instances = 0
    
    def placeTree(self, location, parent):
        newName = self.name + "_Inst" + str(self.instances)
        cmds.instance(self.name, n=newName)
        self.instances += 1
        cmds.parent(newName, parent)
        cmds.xform(newName, t=(location[0], location[1], location[2]))
        cmds.refresh(f=1)

        
    def generateTree(self, density, branchStart, branchRecLevel, seed, location, terrain, height):
        r.seed(seed)
        with contextlib.suppress(Exception):
            cmds.delete(self.name)
        self.generateCurve(self.name, [0,0,0], height * 2, branchStart)
        self.sweepCurve(self.name,[0,0,0], self.radius, branchStart)
        self.createBranch(branchStart, branchStart / branchRecLevel, self.name, density / 2, height)
        cmds.xform(self.name, t=(location[0], location[1] - 1, location[2]))
        cmds.playbackOptions(minTime=self.animStart, maxTime=self.animStop, l="continuous")
        cmds.xform(self.name, ro=("0deg", str(r.uniform(0, 360)) + "deg", "0deg"), rp=(0, 0, 0), os=1)
        cmds.parent(self.name, terrain)
        cmds.refresh(f=1)
        
    def __init__(self, name = "", radius = 0, leaves = False, animAmount = 0, animStart = 0, animEnd = 0, animStep = 0, genHeight = 0):
        self.name = name
        self.radius = radius
        self.leaves = leaves
        self.animAmount = animAmount
        self.animStart = animStart
        self.animStop = animEnd
        self.animStep = animStep
        self.genHeight = genHeight
    def generateCurve(self, name, start, height, i: int = 1):
        points:list = [start]
        j = 0.0
        while j < 1:
            points.append(
                [
                    points[-1][0] + (m.asin(j) / 90) * r.uniform(0, 200 * i),
                    start[1] + (j * height),
                    points[-1][2] + (m.asin(j) / 90) * r.uniform(0, 200 * i),
                ]
            )
            j += 0.1
        # print(points)
        cmds.curve(n=name, p=points, bez=1)
        # cmds.smoothCurve(f"{name}.cv[*]", s=5)

    def generatePoints(self, n, density: float, height, i):
        items = []
        for _ in range(m.floor(density * 100)):
            temp = r.uniform(height, 1)
            items.append([cmds.pointOnCurve(n, p=1, top=1, pr=temp), temp])
        return items

    def sweepCurve(self, name, point, radius, i):
        cmds.circle(n=f"{name}_profile", r=radius)
        cmds.xform(f"{name}_profile", t=point)
        cmds.parent(f"{name}_profile", name)
        cmds.xform(f"{name}_profile", ro=(90,0,0))
        cmds.extrude(f"{name}_profile", name, et=2, n=f"{name}_mesh",fpt=1,p=point,sc=0.5,po=1)
        cmds.parent(f"{name}_mesh", name)
        cmds.delete(f"{name}_profile")
        cmds.polyNormal(f"{name}_mesh", nm=0)
        cmds.hyperShade(f"{name}_mesh", a="BarkMat")

    def createBranch(self, i, dec, branch, den, height):
        height *= i
        num = 0
        points = self.generatePoints(branch, den, self.genHeight, i + dec)
        if r.random() <= i:
            for point in points:
                newName = f"{branch}_Branch{str(num)}"
                print(f"Creating branch: {newName}")
                self.generateCurve(newName,point[0],  r.uniform(1, height), i)
                cmds.parent(newName, branch)
                self.createBranch(i - dec, dec, newName, den * (1 + den), height)
                cmds.xform(newName,ws=1,rp=point[0], ro=(f"{str(r.uniform(0, 45))}deg",f"{str(r.uniform(0, 360) * num)}deg",0))
                self.createAnim(newName,cmds.xform(newName, q=1, ro=1))
                self.sweepCurve(newName, point[0], self.radius * 0.5 * point[1], i)
                num+= 1
        elif branch != self.name and self.leaves:
            for point in points:
                newName = f"{branch}_Leaf{str(num)}"
                print(f"Creating leaf: {newName}")
                cmds.duplicate("Leaf1", n=newName)
                cmds.parent(newName, branch)
                cmds.xform(newName, translation=(point[0][0], point[0][1], point[0][2]), ws=1)
                cmds.xform(
                    newName,
                    ro=(
                        f"{str(r.uniform(0, 360))}deg",
                        f"{str(r.uniform(0, 360))}deg",
                        f"{str(r.uniform(0, 360))}deg",
                    ),
                    os=1
                )
                self.createAnim(newName, cmds.xform(newName, q=1, ro=1))
                num += 1

    def createAnim(self, name, itemRotation):
        for i in range(m.floor(self.animStart), m.floor(self.animStop), m.floor(self.animStep * 2)):
            cmds.setKeyframe(name, at="rotateX", time=i, v=itemRotation[0])
            cmds.setKeyframe(name, at="rotateY", time=i, v=itemRotation[1])
            cmds.setKeyframe(name, at="rotateZ", time=i, v=itemRotation[2])
            cmds.setKeyframe(
                name,
                at="rotateX",
                time=i + self.animStep,
                v=itemRotation[0]
                + (r.uniform(self.animAmount / 2, self.animAmount)),
            )
            cmds.setKeyframe(
                name,
                at="rotateY",
                time=i + self.animStep,
                v=itemRotation[1]
                + (r.uniform(self.animAmount / 2, self.animAmount)),
            )
            cmds.setKeyframe(
                name,
                at="rotateZ",
                time=i + self.animStep,
                v=itemRotation[2]
                + (r.uniform(self.animAmount / 2, self.animAmount)),
            )
            
            
class Terrain:
    name = ""
    xSub = 0
    ySub = 0
    
    def __init__(self, name, xSub, ySub):
        self.name = name
        self.xSub = xSub
        self.ySub = ySub
    
    def generateTerrain(self, xSize, ySize, a):
        
        try:
            cmds.delete(self.name, hr=1)
        except:  # noqa: E722
            pass
        cmds.polyPlane(n=self.name, w=xSize, h=ySize, sx=self.xSub, sy=self.ySub)
        cmds.setAttr(self.name+".rotate", 0, 90, 0, type="double3")

        for y in range(0, self.ySub):
            for x in range(0, self.xSub):
                v = x + (y * self.xSub)
                cmds.polyMoveVertex(self.name+".vtx[" + str(v) + "]", ty=(r.random() * a * 2) - a)
        cmds.hyperShade(self.name, a="MudMat")

    def smooth(self):
        cmds.polySmooth(self.name, dv=4, kb=0)        #algorithm to generate points along surface
        
    def generateRandomSurfacePoints(self, tolerance):
        """
        This function generates a list of points randomly placed on a polyPlane surface
        based on a given probability tolerance.

        Args:
        tolerance (float): The probability threshold for placing a point.

        Returns:
        list: A list of point coordinates on the surface.
        """
        surfacePoints = []
        for y in range(self.ySub + 1):
            for x in range(self.xSub + 1):
                v = x + (y * self.xSub)
                if r.random() <= tolerance:
                    pointPosition = cmds.xform(self.name + ".vtx[" + str(v) + "]", query=True, translation=True, worldSpace=True)
                    surfacePoints.append(pointPosition)

        return surfacePoints
    
    
GUIItem = terrainUI()
GUIItem.createTerrainUI()