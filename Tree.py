import contextlib
import maya.cmds as cmds
import random as r
import math as m

class Tree:
    def generateCurve(name: str, height, start: tuple, i: int = 1):
        points:list = [start]
        for j in range(m.floor(height * i) + 1):
            points.append((start[0] + (r.uniform(0, 0.2)) * j, start[1] + j * i * 2, start[2] + (r.uniform(0, 0.2)) * j,))
        cmds.curve(n=name, p=points, bez=1)

    def generatePoints(name, density: float, height, i):
        output = []
        for j in range(r.randint(m.floor(density * 100 * 0.5), m.floor(density * 100 * 1.5))):
            output.append(cmds.pointOnCurve(name, p=1, top=1, pr=r.uniform(height, 1)))
        return output

    def sweepCurve(name, point, radius, i):
        cmds.circle(n=name+"_profile", r=radius)
        cmds.xform(t=point)
        cmds.parent(name+"_profile", name)
        cmds.xform(name+"_profile", ro=(90,0,0))
        cmds.extrude(name+"_profile", name, et=2, n=name+"_mesh", fpt=1, p=point, sc=i, rb=1, po=1)
        cmds.parent(name+"_mesh", name)
        cmds.delete(name+"_profile")
        cmds.polyNormal(name+"_mesh", nm=0)
        cmds.hyperShade(name+"_mesh", a="BarkMat")

    def createBranch(self, dec, branch, den):
        num = 0
        points = generatePoints(branch, den, genHeight, self + dec)
        for point in points:
            if r.random() < self:
                newName = f"{branch}_Branch{str(num)}"
                print(f"Creating branch: {newName}")
                generateCurve(newName, height, point, self)
                cmds.parent(newName, branch)
                rotation = (f"{str(r.uniform(20, 60))}deg",f"{str(r.uniform(0, 90) * num)}deg",f"{str(r.uniform(20, 60))}deg")
                cmds.xform(newName,ws=1,rp=point, ro=rotation)
                createAnim(
                    newName,
                    cmds.xform(newName, q=1, ro=1),
                    (1 - self) * animAmount,
                    animationStart,
                    animationStop,
                    animationStep,
                )
                sweepCurve(newName, point, radius * self, self)
                createBranch(self - dec, dec, newName, den)
                num+= 1
            elif branch != "Trunk" and leaves:
                newName = f"{branch}_Leaf{str(num)}"
                print(f"Creating leaf: {newName}")
                cmds.duplicate("Leaf1", n=newName)
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
                createAnim(newName, cmds.xform(newName, q=1, ro=1), animAmount, animationStart, animationStop, animationStep)
                num += 1

    def createAnim(self, itemRotation, rotationFactor, start, stop, step):
        for i in range(start, stop, step * 2):
            cmds.setKeyframe(self, at="rotateX", time=i, v=itemRotation[0])
            cmds.setKeyframe(self, at="rotateY", time=i, v=itemRotation[1])
            cmds.setKeyframe(self, at="rotateZ", time=i, v=itemRotation[2])
            cmds.setKeyframe(
                self,
                at="rotateX",
                time=i + step,
                v=itemRotation[0]
                + (r.uniform(rotationFactor / 2, rotationFactor)),
            )
            cmds.setKeyframe(
                self,
                at="rotateY",
                time=i + step,
                v=itemRotation[1]
                + (r.uniform(rotationFactor / 2, rotationFactor)),
            )
            cmds.setKeyframe(
                self,
                at="rotateZ",
                time=i + step,
                v=itemRotation[2]
                + (r.uniform(rotationFactor / 2, rotationFactor)),
            )

    def generateTree(self):
        r.seed(5)

        radius = 1
        height = 20
        n = "Trunk"
        Density = 0.2
        leaves = True
        deform = False
        animAmount = 10
        animationStart = 0
        animationStop = 200
        animationStep = 25
        genHeight = 1 - 0.6
        branchDivStart = 0.8
        branchDec = 3

        with contextlib.suppress(Exception):
            cmds.delete(n)
        self.generateCurve(n, height, (0, 0, 0), 1)

        self.sweepCurve(n, (0,0,0), radius * 2, 1)

        self.createBranch(branchDivStart, branchDivStart / branchDec, n, Density / 2)

        cmds.playbackOptions(minTime=animationStart, maxTime=animationStop, l="continuous")

        cmds.refresh(f=1)