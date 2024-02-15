import maya.cmds as cmds

class TextInput:
    inpControl = 0
    default = ""
    def __init__(self, name, default, nullable=False):
        if not nullable:
            self.inpControl = cmds.textFieldGrp(label=name, ec=self.checkEmpty)
            self.default = default
        else:
            self.inpControl = cmds.textFieldGrp(label=name)
    def checkEmpty(self):
        if self.getValue() == "":
            cmds.textFieldGrp(self.inpControl, e=1, v=self.default)
    def getValue(self):
        return cmds.textFieldGrp(self.inpControl, q=1, v=1)
    
class IntInput:
    inpControl = 0
    def __init__(self, name, minValue, maxValue, defaultValue = 0):
        self.inpControl = cmds.intSliderGrp(l=name, min=minValue, max=maxValue, v=defaultValue)
    def getValue(self):
        return cmds.intSliderGrp(self.inpControl, q=1, v=1)
    
class FloatInput:
    inpControl = 0
    def __init__(self, name, minValue, maxValue, defaultValue = 0):
        self.inpControl = cmds.floatSliderGrp(l=name, min=minValue, max=maxValue, v=defaultValue)
    def getValue(self):
        return cmds.floatSliderGrp(self.inpControl, q=1, v=1)
    
class BoolInput:
    inpControl = 0
    def __init__(self, name, defaultState):
        self.inpControl = cmds.checkBox(l=name, v=defaultState)
    def getValue(self):
        return cmds.checkBox(self.inpControl, q=1, v=1)
class UI:
    WinControl = 0
    NameInput = 0
    RadiusInput = 0
    HeightInput = 0
    LeavesPresentInput = 0
    GenerateLeavesFastInput = 0
    BranchChangeStartInput = 0
    BranchRecursionAmountInput = 0
    BranchAndLeafDensityInput = 0
    PlacementHeightInput = 0
    AnimationStartInput = 0
    AnimationStopInput = 0
    AnimationStepInput = 0
    AnimationVarianceInput = 0
    RSeedInput = 0
    GenerateButton = 0
    CancelButton = 0

    def createTreeUI(self):    
        self.WinControl = cmds.window(t="Tree Generator")
        cmds.columnLayout(adj=True)
        self.NameInput = TextInput("Name of tree", "Tree")
        self.RadiusInput = FloatInput("Radius of Trunk", 0.1, 5, 1)
        self.HeightInput = IntInput("Height of Trunk", 1, 500, 20)
        self.LeavesPresentInput = BoolInput("Generate Leaves", True)
        self.GenerateLeavesFastInput = BoolInput("Generate leaves quickly", True)

        self.BranchChangeStartInput = FloatInput("Branch size start point", 0, 1, 0.8)
        self.BranchRecursionAmountInput = IntInput("Branch recursion count", 1, 5, 3)
        self.BranchAndLeafDensityInput = FloatInput("Density of branches and leaves", 0, 1, 0.3)
        self.PlacementHeightInput = FloatInput("Height to start generating objects on branches", 0, 1, 0.6)

        self.AnimationStartInput = IntInput("Animation Start frame", 0, 999999, 0)
        self.AnimationStopInput = IntInput("Animation Stop frame", 0, 999999, 500)
        self.AnimationStepInput = IntInput("Animation Step count", 0, 999999, 50)
        self.AnimationVarianceInput = IntInput("Animation magnitude", 0, 90, 10)

        self.RSeedInput = IntInput("Randomness seed", 1, 999999, 1)

        self.GenerateButton = cmds.button(l="Generate Tree", )
        cmds.showWindow(winControl)
        
        
    def GenerateTree(self):
        treeItem = Tree(RadiusInput.getValue(), HeightInput.getValue(), LeavesPresentInput.getValue(), AnimationVarianceInput.getValue(), AnimationStartInput.getValue(), AnimationStopInput.getValue(), AnimationStepInput.getValue(), PlacementHeightInput.getValue(), GenerateLeavesFastInput.getValue())
        
        name = NameInput.getValue()
        density = BranchAndLeafDensityInput.getValue()
        branchStart = BranchChangeStartInput.getValue()
        branchRec = BranchRecursionAmountInput.getValue()
        seed = RSeedInput.getValue()
        
        cmds.deleteUI(self.WinControl)
        
        treeItem.generateTree(name, density, branchStart, branchRec, seed)