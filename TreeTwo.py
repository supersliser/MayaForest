import random as r

def rN(min, max):
    return (r.random * max) + min

class Tree:
    Nodes = []

    def addNode(self, name="Node" + Nodes.count(), parent = None, location = [0.0, 0.0, 0.0], isBranch = True):
        newNode = Node(name, parent, self)
        newNode.Position = location
        self.Nodes.append(newNode)
        if parent is not None:
            if isBranch:
                parent.Branch.append(newNode)
            else:
                parent.Continuer.append(newNode)
        return newNode

    def getNode(self, name="", parent=None, index=-1):
        if name != "":
            for node in self.Nodes:
                if node.Name == name:
                    return node
        elif parent is not None:
            output = []
            for node in self.Nodes:
                if node.Parent == parent:
                    output.append(node)
            return output
        elif index != -1:
            return output[index]
        raise Exception("Unable to get nodes")

    def generateTree(self, name, recursionDepth, recursionMax, recursionDecrease, treeHeight, density, branchStartPercentage):
        self.Nodes = []
        trunk = self.addNode(name)
        baseBranchCount = rN(3, 20 * density)
        BaseTreeHeight = treeHeight - (treeHeight * branchStartPercentage)
        previousNode = self.addNode(parent=trunk, location=[0, BaseTreeHeight, 0], isBranch=False)
        if rN(0, 1) < recursionDepth:
            for i in range(baseBranchCount):
                self.addNode(parent=previousNode, location=[(recursionMax - recursionDepth) * recursionDepth, BaseTreeHeight + ((treeHeight * branchStartPercentage) * (i / baseBranchCount)), (recursionMax - recursionDepth) * recursionDepth], isBranch=False)
                self.generateTree(name + f"_Branch {i + recursionDepth}", recursionDepth - recursionDecrease, recursionMax, recursionDecrease, treeHeight * rN(recursionDepth / 2, recursionDepth + (recursionDepth / 2)), density, branchStartPercentage)
        else:
            pass
            #generate leaves        


class Node:
    Position = [0.0, 0.0, 0.0]
    Name = ""
    Parent = None
    Graph = Tree
    Continuer = None
    Branch = None
    Leaves = False

    def __init__(self, name, parent, graph, leaves = False):
        self.Name = name
        self.Parent = parent
        self.Graph = graph
        self.Leaves = leaves
    
    def __str__(self):
        return f"{self.Name} at {self.Position} owned by {self.Parent.Name} and owns {self.Continuer.Name} & {self.Branch.Name}"