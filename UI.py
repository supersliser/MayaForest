import maya.cmds as cmds
def createTreeUI():
    winControl = cmds.window(t="Tree Generator")
    cmds.columnLayout(adj=True)
    cmds.text(l="Tree Name")
    TreeName = cmds.textField()
    
    
    cmds.showWindow(winControl)
    
def treeNameEdited():
    
    
    
    
createTreeUI()