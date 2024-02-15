import contextlib
import maya.cmds as cmds
import random as r
import math as m

class Tree:
    radius
    height
    leaves
    animAmount 
    animStart
    animStop
    animStep
    genHeight
    fast
    
    def generateTree(name, density, branchStart, branchRecLevel, seed):
    r.seed(seed)
    with contextlib.suppress(Exception):
        cmds.delete(name)
    self.generateCurve(name, self.height, (0, 0, 0), branchStart)
    self.sweepCurve(name, (0,0,0), self.radius * 2, branchStart)
    self.createBranch(branchStart, branchStart / branchRecLevel, name, density / 2)
    cmds.playbackOptions(minTime=animStart, maxTime=animStop, l="continuous")
    cmds.refresh(f=1)
        
    def __init__(self, radius, height, leaves, animAmount, animStart, animEnd, animStep, genHeight, fast):
        self.radius = radius
        self.height = height
        self.leaves = leaves
        self.animAmount = animAmount
        self.animStart = animStart
        self.animStop = animEnd
        self.animStep = animStep
        self.genHeight = genHeight
        self.fast = fast        
    def generateCurve(self, name, height, start: tuple, i: int = 1):
        points:list = [start]
        points.extend(
            (
                start[0] + (r.uniform(0, 0.2)) * j,
                start[1] + j * i * 2,
                start[2] + (r.uniform(0, 0.2)) * j,
            )
            for j in range(m.floor(height * i) + 1)
        )
        cmds.curve(n=name, p=points, bez=1)

    def generatePoints(self, n, density: float, height, i):
        return [
            cmds.pointOnCurve(n, p=1, top=1, pr=r.uniform(height, 1))
            for _ in range(m.floor(density * 100))
        ]

    def sweepCurve(self, name, point, radius, i):
        cmds.circle(n=f"{name}_profile", r=radius)
        cmds.xform(t=point)
        cmds.parent(f"{name}_profile", name)
        cmds.xform(f"{name}_profile", ro=(90,0,0))
        cmds.extrude(
            f"{name}_profile",
            name,
            et=2,
            n=f"{name}_mesh",
            fpt=1,
            p=point,
            sc=i,
            rb=1,
            po=1,
        )
        cmds.parent(f"{name}_mesh", name)
        cmds.delete(f"{name}_profile")
        cmds.polyNormal(f"{name}_mesh", nm=0)
        cmds.hyperShade(f"{name}_mesh", a="BarkMat")

    def createBranch(self, i, dec, branch, den):
        num = 0
        points = self.generatePoints(branch, den, self.genHeight, i + dec)
        for point in points:
            if r.random() < i:
                newName = f"{branch}_Branch{str(num)}"
                print(f"Creating branch: {newName}")
                self.generateCurve(newName, self.height, point, i)
                cmds.parent(newName, branch)
                self.createBranch(i - dec, dec, newName, den)
                rotation = (f"{str(r.uniform(20, 60))}deg",f"{str(r.uniform(60, 120) * num)}deg",f"{str(r.uniform(20, 60))}deg")
                cmds.xform(newName,ws=1,rp=point, ro=rotation)
                self.createAnim(newName,cmds.xform(newName, q=1, ro=1))
                self.sweepCurve(newName, point, self.radius * i, i)
                num+= 1
            elif branch != self.n and self.leaves:
                newName = f"{branch}_Leaf{str(num)}"
                print(f"Creating leaf: {newName}")
                if self.fast:
                    cmds.duplicate("Leaf1", n=newName)
                else:
                    cmds.instance("Leaf1", n=newName)
                cmds.parent(newName, branch)
                cmds.xform(newName, translation=(point[0], point[1], point[2]), ws=1)
                cmds.xform(
                    newName,
                    ro=(
                        f"{str(r.uniform(0, 360))}deg",
                        f"{str(r.uniform(0, 360))}deg",
                        f"{str(r.uniform(0, 360))}deg",
                    ),
                )
                self.createAnim(newName, cmds.xform(newName, q=1, ro=1))
                num += 1

    def createAnim(self, name, itemRotation):
        for i in range(animStart, animStop, animStep * 2):
            cmds.setKeyframe(name, at="rotateX", time=i, v=itemRotation[0])
            cmds.setKeyframe(name, at="rotateY", time=i, v=itemRotation[1])
            cmds.setKeyframe(name, at="rotateZ", time=i, v=itemRotation[2])
            cmds.setKeyframe(
                name,
                at="rotateX",
                time=i + step,
                v=itemRotation[0]
                + (r.uniform(animAmount / 2, animAmount)),
            )
            cmds.setKeyframe(
                name,
                at="rotateY",
                time=i + step,
                v=itemRotation[1]
                + (r.uniform(animAmount / 2, animAmount)),
            )
            cmds.setKeyframe(
                name,
                at="rotateZ",
                time=i + step,
                v=itemRotation[2]
                + (r.uniform(animAmount / 2, animAmount)),
            )