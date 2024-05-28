import contextlib
import maya.cmds as cmds
import random as r
import math as m

class TextInput:
    def __init__(self, name, default, nullable=False):
        """
        Initializes the instance with the given name, default value, and nullable flag.

        Args:
            name (str): The name for the input control.
            default (str): The default value for the input control.
            nullable (bool, optional): Flag indicating if the input control can be nullable. Defaults to False.
        """
        # if the input can be set to "" then the default must be set and the input must check for if it has been left empty
        if not nullable:
            self.inpControl = cmds.textFieldGrp(name, label=name, tx=default, tcc=self.checkEmpty).split("|")[-1]
            self.default = default
        else:
            self.inpControl = cmds.textFieldGrp(name, label=name, tx=default)
    def checkEmpty(self, *args):
        """
        Check if the value is empty and update the text field if necessary.
        
        Parameters:
            *args: Variable length argument list.
        
        Returns:
            None
        """
        if self.getValue() == "":
            cmds.textFieldGrp(self.inpControl, e=1, tx=self.default)
    def getValue(self):
        """
        Method to get the value using cmds.textFieldGrp, and return the result.
        """
        print(self.inpControl)
        return cmds.textFieldGrp(self.inpControl, q=1, tx=1).replace(" ", "_")

class IntInput:
    def __init__(self, name, minValue, maxValue, defaultValue = 0):
        """
        Initialize the class with the given parameters.

        Args:
            name (str): The name of the intSliderGrp.
            minValue (int): The minimum value for the intSliderGrp.
            maxValue (int): The maximum value for the intSliderGrp.
            defaultValue (int, optional): The default value for the intSliderGrp. Defaults to 0.
        """
        self.inpControl = cmds.intSliderGrp(l=name, f=1, min=minValue, max=maxValue, v=defaultValue, cw=[1, 350])
    def getValue(self):
        """
        A function that retrieves the value of an intSliderGrp control.

        Args:
            self: the instance of the class
            No explicit parameters

        Returns:
            The value of the intSliderGrp control
        """
        return cmds.intSliderGrp(self.inpControl, q=1, v=1)

class FloatInput:
    def __init__(self, name, minValue, maxValue, defaultValue = 0):
        """
        Initialize the class with the given parameters.

        Args:
            name (str): The name of the floatSliderGrp.
            minValue (int): The minimum value for the floatSliderGrp.
            maxValue (int): The maximum value for the floatSliderGrp.
            defaultValue (int, optional): The default value for the floatSliderGrp. Defaults to 0.
        """
        self.inpControl = cmds.floatSliderGrp(l=name, f=1, min=minValue, max=maxValue, v=defaultValue, cw=[1, 350])
    def getValue(self):
        """
        A method to get the value from a float slider group control.
        """
        return cmds.floatSliderGrp(self.inpControl, q=1, v=1)

class BoolInput:
    def __init__(self, name, defaultState):
        """
        Initializes the class with the given name and default state.

        Args:
            name (str): The name for the checkbox.
            defaultState (bool): The default state of the checkbox.
        """
        self.inpControl = cmds.checkBox(l=name, v=defaultState)
    def getValue(self):
        """
        Method to get the value using cmds.checkBox.
        """
        return cmds.checkBox(self.inpControl, q=1, v=1)
class terrainUI:
    
    def updateProgress(self, text = "Please Wait..."):
        """
        Updates the progress window and sets the progress label text.

        Args:
            text (str): The label text to display in the progress window. Default is "Please Wait...").
        """
        self.progress += 1
        cmds.progressWindow(e=1, p=self.progress, label=text)
    def createTerrainUI(self):
        """
        Create the UI for terrain generation with input fields for name, width, depth, subdivisions, tree variants, amplitude, tolerance, seed, and buttons to generate and cancel.
        """
        self.WinControl = cmds.window(t="Forest UI")
        self.NameInput = TextInput("Name of terrain", "Terrain")
        cmds.columnLayout(adj=True, cat=["both", 0])
        self.TreesExist = BoolInput("Generate Trees", True)
        self.GrassExist = BoolInput("Generate Grass", True)
        self.FireFliesExist = BoolInput("Generate Fireflies", True)
        self.WidthInput = IntInput("Width of terrain", 1, 2000, 150)
        self.DepthInput = IntInput("Depth of terrain", 1, 2000, 150)
        self.TreeVariants = IntInput("Number of different types of trees to use", 1, 10, 4)
        self.Amplitude = FloatInput("Difference between highest point and lowest point in terrain", 1, 10, 5)
        self.TreeDensity = FloatInput("Percentage of space to generate trees", 0, 1, 0.4)
        self.GrassDensity = FloatInput("Percentage of space to generate grass", 0, 1, 0.7)
        self.FireFlyDensity = FloatInput("Percentage of space to generate fireflies", 0, 1, 0.2)
        self.Seed = IntInput("Randomness seed", 1, 9999999, 1)
        self.GenerateButton = cmds.button(l="Generate", c=self.GenerateTerrain)
        self.CancelButton = cmds.button(l="Cancel", c=self.Cancel)
        cmds.showWindow(self.WinControl)
        self.progress = 0
    def Cancel(self, *args):
        """
        Cancel the specified UI element, runs from the cancel button being clicked.
        """
        cmds.deleteUI(self.WinControl)
        
    def GenerateTerrain(self, *args):
        """
        Generate terrain and place trees on the terrain.
        """
        max = 3
        # The max number of things to do changes based on whether or not the user wants trees or grass
        if self.TreesExist.getValue():
            max += self.TreeVariants.getValue() + 2
        if self.GrassExist.getValue():
            max += 2
        if self.FireFliesExist.getValue():
            max += 1
        self.ProgressWindow = cmds.progressWindow(title="Generating Forest", progress=0, min=0, max=max, status="Generating Seed...", isInterruptable=0)
        r.seed(self.Seed.getValue())
        self.updateProgress(text="Generating Terrain")
        terrainItem = Terrain(self.NameInput.getValue(), 5, 5)
        terrainItem.generateTerrain(self.WidthInput.getValue(), self.DepthInput.getValue(), self.Amplitude.getValue())
        if self.GrassExist.getValue():
            self.updateProgress(text="Generating Grass Points")
            pointAmountMultiplier = 10
            points = terrainItem.generateRandomPointsOnPlane(plane=terrainItem.name, num_points=m.floor((self.GrassDensity.getValue() / pointAmountMultiplier) * self.WidthInput.getValue() * self.DepthInput.getValue()))
            self.updateProgress(text="Generating Grass")
            grass = Grass()
            grass.generateGrass(points, terrainItem.name)
        if self.TreesExist.getValue():
            self.updateProgress(text="Generating Trees")
            trees = []
            # generates template trees that are used for instancing
            for t in range(self.TreeVariants.getValue()):
                radiusMultiplier = r.uniform(0.5, 1.5)
                animationVariance = 5
                animationStartPoint = 0
                animationEndPoint = 250
                animationStepAmount = 50
                heightToStartGeneratingTrees = 0.7
                densityOfLeavesAndBranches = r.uniform(0.15, 0.25)
                branchMultiplierStart = 1
                branchRecursionAmount = r.randint(2, 3)
                treeRandomnessSeed = self.Seed.getValue() + t
                treeLocation = (0, 0, 0)
                parentTerrain = terrainItem.name
                height = r.randint(15, 40)

                temp = Tree(terrainItem.name + "_Tree" + str(t),radiusMultiplier , animationVariance, animationStartPoint, animationEndPoint, animationStepAmount, heightToStartGeneratingTrees)
                self.updateProgress(text="Generating Tree " + str(t))
                temp.generateTree(density=densityOfLeavesAndBranches, branchStart=branchMultiplierStart, branchRecLevel=branchRecursionAmount, seed=treeRandomnessSeed, location=treeLocation, terrain=parentTerrain, height=height)
                trees.append(temp)
            self.updateProgress(text="Generating Tree Instances")
            pointAmountMultiplier = 1000
            points = terrainItem.generateRandomPointsOnPlane(terrainItem.name, m.floor((self.TreeDensity.getValue() / pointAmountMultiplier) * self.WidthInput.getValue() * self.DepthInput.getValue()))
            #places a randomly chosen tree instance at each point on the plane
            for p in points:
                trees[r.randint(0, len(trees) - 1)].placeTree(p)
            # template trees can only be hidden once their instances are created
            for t in trees:
                t.hide()
        if self.FireFliesExist.getValue():
            self.updateProgress(text="Generating Fireflies")
            terrainItem.generateFireFlies(self.WidthInput.getValue(), self.DepthInput.getValue(), m.floor(self.FireFlyDensity.getValue() / 100 * self.WidthInput.getValue() * self.DepthInput.getValue()), animationStartPoint, animationEndPoint, animationStepAmount, animationVariance)
        self.updateProgress(text="Smoothing Terrain")
        terrainItem.smooth(2)
        self.updateProgress(text="Process Complete")
        cmds.deleteUI(self.WinControl)
        cmds.progressWindow(e=1, endProgress=1)

class Tree:
    instances = 0
    def placeTree(self, location):
        """
        Generate an instance of a tree at the specified location and rotation.

        Args:
            location (list): The x, y, z coordinates of the location.
        """
        newName = self.name + "_Inst" + str(self.instances)
        print("Placing tree: " + newName)
        cmds.instance(self.name, n=newName, st=0)
        self.instances += 1
        cmds.move(location[0], location[1], location[2], newName)
        cmds.rotate("0deg", "0deg", "-90deg", newName, os=1)
        cmds.xform(newName, ro=("0deg", str(r.randint(0, 360)) + "deg", "0deg"), r=1, os=1)

    def hide(self):
        """
        Hides the object by setting its visibility attribute to 0.
        """
        cmds.setAttr(self.name + ".visibility", 0)
    def generateTree(self, density, branchStart, branchRecLevel, seed, location, terrain, height):
        """
        Generate a tree based on the given arguments.

        Args:
            density (float): The density of the tree.
            branchStart (float): The starting point of the branches.
            branchRecLevel (int): The recursion level for branching.
            seed (int): The seed for randomization.
            location (list): The location of the tree.
            terrain (str): The terrain on which the tree is placed.
            height (float): The height of the tree.
        """
        r.seed(seed)
        with contextlib.suppress(Exception):
            cmds.delete(self.name)
        self.generateCurve(self.name, [0,0,0], height * 2, branchStart)
        self.sweepCurve(self.name,[0,0,0], self.radius, branchStart)
        self.createBranch(branchStart, branchStart / branchRecLevel, self.name, density / 2, height)
        cmds.xform(self.name, t=(location[0], location[1] - 1, location[2]))
        cmds.playbackOptions(minTime=self.animStart, maxTime=self.animStop, l="continuous")
        cmds.parent(self.name, terrain)
        
    def __init__(self, name = "", radius = 0, animAmount = 0, animStart = 0, animEnd = 0, animStep = 0, genHeight = 0):
        """
        Initialize the object with the given parameters.

        Args:
            name (str): The name of the object (default is an empty string).
            radius (int): The radius of the object (default is 0).
            animAmount (int): The amount of animation (default is 0).
            animStart (int): The start value of the animation (default is 0).
            animEnd (int): The end value of the animation (default is 0).
            animStep (int): The step of the animation (default is 0).
            genHeight (int): The height of the generation (default is 0).
        """
        self.name = name
        self.radius = radius
        self.animAmount = animAmount
        self.animStart = animStart
        self.animStop = animEnd
        self.animStep = animStep
        self.genHeight = genHeight
    def generateCurve(self, name, start, height, i: int = 1):
        """
        Generate a curve with given name, start, height, and optional integer parameter.
        
        Args:
            name (str): the name of the curve
            start (list): the starting point of the curve
            height (int): the height of the curve
            i (int, optional): the optional integer parameter
        """
        points:list = [start]
        j = 0.0
        while j < 1:
            # generates a curve using points that follow a generic sin curve with a random magnitude multiplier
            points.append(
                [
                    points[-1][0] + (m.asin(j) / 90) * r.uniform(0, 200 * i),
                    start[1] + (j * height),
                    points[-1][2] + (m.asin(j) / 90) * r.uniform(0, 200 * i),
                ]
            )
            j += 0.1
        cmds.curve(n=name, p=points, bez=1)

    def generatePoints(self, n, density: float, height):
        """
        Generate points with given name, density, height, and optional integer parameter.
        
        Args:
            n (str): the name of the curve
            density (float): the density of the curve
            height (int): the height of the curve
        """
        items = []
        for _ in range(m.floor(density * 100)):
            temp = r.uniform(height, 1)
            items.append([cmds.pointOnCurve(n, p=1, top=1, pr=temp), temp])
        return items

    def sweepCurve(self, name, point, radius, i):
        """
        This function sweeps a circle along a predefined curve.

        Args:
            self: the instance of the class
            name (str): the name of the curve
            point (tuple): the position of the curve
            radius (float): the radius of the curve
            i: an integer parameter
        """
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
        """
        Function to create branches with given parameters.

        Args:
            i: int, parameter for height calculation
            dec: float, parameter for height calculation
            branch: str, name of the branch
            den: float, parameter for generating points
            height: float, height of the branch
        """
        height *= i
        num = 0
        points = self.generatePoints(branch, den, self.genHeight)
        # checks whether this recursion should be a branch recursion or leaf recursion
        if r.random() <= i:
            for point in points:
                newName = f"{branch}_Branch{str(num)}"
                print(f"Creating branch: {newName}")
                self.generateCurve(newName,point[0],  r.uniform(1, height), i)
                cmds.parent(newName, branch)
                self.createBranch(i - dec, dec, newName, den * (1 + den), height)
                cmds.xform(newName,ws=1,rp=point[0], ro=(f"{str(r.uniform(0, 45))}deg",f"{str(r.uniform(0, 360) * num)}deg",0))
                # self.createAnim(newName,cmds.xform(newName, q=1, ro=1))
                self.sweepCurve(newName, point[0], self.radius * 0.5 * point[1], i)
                num+= 1
        elif branch != self.name:
            newName = f"{branch}_Leaf{str(num)}"
            #duplicates the original leaf to avoid too many instances of the same item (all instances are connected)
            cmds.duplicate("Leaf1", n=newName)
            cmds.parent(newName, branch)
            cmds.xform(newName, translation=(points[0][0][0], points[0][0][1], points[0][0][2]), ws=1)
            cmds.xform(
                newName,
                ro=(
                    f"{str(r.uniform(0, 360))}deg",
                    f"{str(r.uniform(0, 360))}deg",
                    f"{str(r.uniform(0, 360))}deg",
                ),
                os=1
            )
            num += 1
            #then generates multiple instances of the duplicated leaf
            for point in points[1:]:
                newIName = f"{branch}_Leaf{str(num)}"
                cmds.instance(newName, n=newIName, st=0)
                cmds.move(point[0][0], point[0][1], point[0][2], newIName)
                cmds.rotate(
                    f"{str(r.uniform(0, 360))}deg",
                    f"{str(r.uniform(0, 360))}deg",
                    f"{str(r.uniform(0, 360))}deg",
                    newIName,
                    os=1
                )
                num += 1

    def createAnim(self, name, itemRotation):
        """
        Create an animation for the given name with the specified itemRotation.
        
        Args:
            name (str): the name of the animation
            itemRotation (list): a list containing the rotation values for X, Y, and Z axes before being animated
        """
        for i in range(m.floor(self.animStart), m.floor(self.animStop), m.floor(self.animStep * 2)):
            #animation step has 2 parts, start and end point to make sure trees always return to original point
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
    def __init__(self, name, xSub, ySub):
        """
        Initialize the object with the given parameters.
        
        Args:
            name (str): the name of the terrain
            xSub (int): the number of subdivisions in the x direction
            ySub (int): the number of subdivisions in the y direction
        """
        self.name = name
        self.xSub = xSub
        self.ySub = ySub
    
    def generateTerrain(self, xSize, ySize, a):
        """
        A method to generate a terrain using the nurbsPlane function and randomize the height of each control vertex.
        
        Args:
            xSize (float): the width of the terrain
            ySize (float): the depth of the terrain
            a (float): the amplitude of the terrain
        """
        cmds.nurbsPlane(n=self.name, w=xSize, lr=ySize / xSize, u=self.xSub, v=self.ySub)
        cmds.setAttr(self.name+".rotate", 0, 0, 90, type="double3")
        a *= 2
        for y in range(0, self.ySub + 1):
            for x in range(0, self.xSub + 1):
                v = x + (y * self.xSub)
                cmds.xform(
                    self.name + ".cv[" + str(v) + "]", t=(0, r.uniform(-a, a), 0), r=1, ws=1
                )
        cmds.hyperShade(self.name, a="MudMat")

    def generateFireFlies(self, xSize, ySize, fireFlyDensity, animStart, animEnd, animStep, animVariance):
        for i in range(0, fireFlyDensity):
            cmds.polySphere(n="FireFly" + str(i), r=0.1)
            cmds.parent("FireFly" + str(i), self.name)
            cmds.hyperShade("FireFly" + str(i), a="FireFlyMat")
            currentPosition = [
                r.uniform(2, 50),
                r.uniform(-ySize / 2, ySize / 2),
                r.uniform(-xSize / 2, xSize / 2),
            ]
            cmds.rotate("0deg", "0deg", "0deg", "FireFly" + str(i))
            cmds.move(currentPosition[0], currentPosition[1], currentPosition[2], "FireFly" + str(i))
            for a in range(animStart, animEnd - animStep, animStep):
                cmds.setKeyframe("FireFly" + str(i), at="translateX", time=a, v=currentPosition[0])
                cmds.setKeyframe("FireFly" + str(i), at="translateY", time=a, v=currentPosition[1])
                cmds.setKeyframe("FireFly" + str(i), at="translateZ", time=a, v=currentPosition[2])
                currentPosition[0] += r.uniform(-animVariance, animVariance)
                currentPosition[1] += r.uniform(-animVariance, animVariance)
                currentPosition[2] += r.uniform(-animVariance, animVariance)
            lastEmission = 0
            for a in range(animStart, animEnd, m.floor(r.uniform(animStep / 2, animStep * 2))):
                    cmds.setKeyframe("FireFly" + str(i), at="FireFlyMat.emission", time=a, v=not lastEmission)
        
    def smooth(self, amount):
        """
        A method to apply smoothing to the surface using the polySmooth function.
        
        Args:
            amount (int): the amount of smoothing to apply
        """
        cmds.rebuildSurface(self.name, rt=0, dir=2, su=self.xSub ** amount, sv=self.ySub ** amount)
        
    def generateRandomPointsOnPlane(self, plane, num_points):
        """
        Generate random points on a given plane.

        Args:
            plane: The plane on which the points will be generated.
            num_points: The number of random points to generate.

        Returns:
            List: A list of randomly generated points on the plane.
        """
        points = []
        for _ in range(num_points):
            u = r.uniform(0, 1)
            v = r.uniform(0, 1)
            point_position = cmds.pointOnSurface(plane, u=u, v=v, p=True)
            print(point_position)
            points.append(point_position)
        return points

class Grass:

    def generateCurve(self, name, start, height):
        """
        Generate a curve with given name, start and height using a generic sin curve and a random magnitude multiplier.
        
        Args:
            name (str): the name of the curve
            start (list): the starting point of the curve
            height (int): the height of the curve
        """
        points:list = [start]
        j = 0.0
        while j < 1:
            points.append(
                [
                    points[-1][0] + (m.asin(j) / 90) * r.uniform(0, 200),
                    start[1] + (j * height),
                    points[-1][2] + (m.asin(j) / 90) * r.uniform(0, 200),
                ]
            )
            j += 0.2
        cmds.curve(n=name, p=points, bez=1)
        
    def generateGrass(self, points, parent):
        """
        Generate grass based on the given points and parent object.

        Args:
            points: The points to generate the grass on.
            parent: The parent object for the generated grass.
        """
        BaseCount = 1
        count:int = 50
        BaseName = "GrassTrueClump"
        self.generateGrassClump(count * BaseCount)
        ClumpName = "GrassClumpAxis_"+str(BaseCount)
        for p in points:
            #every 50 instances a new copy should be created to avoid an instancing issue (all instances of an object are connected so when attributes of an instance, all instances are edited)
            if count == 50:
                try:
                    cmds.delete(ClumpName)
                except:
                    pass
                ClumpName = "GrassClumpAxis_"+str(BaseCount)
                print("Generating Grass Clump: " + ClumpName)
                cmds.duplicate(BaseName, n=ClumpName)
                cmds.rotate(0, str(r.uniform(0, 360)) + "deg", 0, ClumpName, ws=1, r=1 )
                BaseCount += 1
                count = 0
            cmds.instance(ClumpName, n="Clump_"+str(BaseCount)+ "_" + str(count), st=0)
            cmds.move(p[0] + r.uniform(-1, 1), p[1], p[2] + r.uniform(-1, 1), "Clump_"+str(BaseCount)+ "_" + str(count))
            cmds.parent("Clump_"+str(BaseCount)+ "_" + str(count), parent)
            count += 1
        cmds.delete(BaseName)
        cmds.delete(ClumpName)

    def generateGrassClump(self, number):
        """
        Generates a grass clump group and its associated curves and meshes. The clump is focussed around a circle.

        Args:
            number (int): The number associated with the grass clump.
        """
        groupName = "GrassTrueClump"
        cmds.circle(n=groupName, r=0.5, s=5)
        cmds.xform(groupName, ro=(90,0,0))
        for i in range(5):
            prName = "GrassProfile_"+str(number)+"_"+str(i)
            point = cmds.xform(groupName+".cv["+str(i)+"]", q=1, t=1,)
            cmds.circle(n=prName, r=0.2, s=4)
            cmds.parent(prName, groupName)
            cmds.xform(prName, ro=(0,0,90))
            ptName = "GrassCurve_"+str(number)+"_"+str(i)
            mName = "GrassMesh_"+str(number)+"_"+str(i)
            self.generateCurve(ptName, [0, 0, 0], 10)
            cmds.parent(ptName, groupName)
            cmds.extrude(prName, ptName, et=2, n=mName,fpt=1,p=[0,0,0],sc=0,po=1)
            cmds.polyNormal(mName, nm=0)
            cmds.parent(mName, ptName)
            cmds.hyperShade(mName, a="GrassMat")
            cmds.xform(ptName, t=point)
            cmds.delete(prName)

cmds.scriptEditorInfo(sw=1, sr=1)
GUIItem = terrainUI()
GUIItem.createTerrainUI()