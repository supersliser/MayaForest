import contextlib
import maya.cmds as cmds
import random as r
import math as m

class Tree:
    
    radius = 1
    height = 20
    n = "Trunk"
    Density = 0.2
    leaves = True
    deform = False
    animAmount = 10
    animationStart = 0
    animationStop = 500
    animationStep = 100
    genHeight = 1 - 0.6
    branchDivStart = 0.8
    branchDec = 3
    fast = True
    
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
            for _ in range(
                r.randint(
                    m.floor(density * 100 * 0.5), m.floor(density * 100 * 1.5)
                )
            )
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
                rotation = (f"{str(r.uniform(20, 60))}deg",f"{str(r.uniform(45, 90) * num)}deg",f"{str(r.uniform(20, 60))}deg")
                cmds.xform(newName,ws=1,rp=point, ro=rotation)
                self.createAnim(
                    newName,
                    cmds.xform(newName, q=1, ro=1),
                    (1 - i) * self.animAmount,
                    self.animationStart,
                    self.animationStop,
                    self.animationStep,
                )
                self.sweepCurve(newName, point, self.radius * i, i)
                num+= 1
            elif branch != "Trunk" and self.leaves:
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
                self.createAnim(newName, cmds.xform(newName, q=1, ro=1), self.animAmount, self.animationStart, self.animationStop, self.animationStep)
                num += 1

    def createAnim(self, name, itemRotation, rotationFactor, start, stop, step):
        for i in range(start, stop, step * 2):
            cmds.setKeyframe(name, at="rotateX", time=i, v=itemRotation[0])
            cmds.setKeyframe(name, at="rotateY", time=i, v=itemRotation[1])
            cmds.setKeyframe(name, at="rotateZ", time=i, v=itemRotation[2])
            cmds.setKeyframe(
                name,
                at="rotateX",
                time=i + step,
                v=itemRotation[0]
                + (r.uniform(rotationFactor / 2, rotationFactor)),
            )
            cmds.setKeyframe(
                name,
                at="rotateY",
                time=i + step,
                v=itemRotation[1]
                + (r.uniform(rotationFactor / 2, rotationFactor)),
            )
            cmds.setKeyframe(
                name,
                at="rotateZ",
                time=i + step,
                v=itemRotation[2]
                + (r.uniform(rotationFactor / 2, rotationFactor)),
            )

    def generateTree(self):
        r.seed(5)

        with contextlib.suppress(Exception):
            cmds.delete(self.n)
        self.generateCurve(self.n, self.height, (0, 0, 0), 1)

        self.sweepCurve(self.n, (0,0,0), self.radius * 2, 1)

        self.createBranch(self.branchDivStart, self.branchDivStart / self.branchDec, self.n, self.Density / 2)

        cmds.playbackOptions(minTime=self.animationStart, maxTime=self.animationStop, l="continuous")

        cmds.refresh(f=1)
        
temp = Tree()
temp.generateTree()