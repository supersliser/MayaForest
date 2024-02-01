import maya.cmds as cmds
import random as r


class PointPlacer:
    points = []
    target_height = 0
    vertex_y = 0

    def __init__(self):
        self.points = []
        self.target_height = 0
        self.vertex_y = 0

    def is_vertex_at_height_percentage(self, meshName, vertexIndex, percentage):
        # Get bounding box dimensions
        if self.target_height != 0:
            min_bound = cmds.exactWorldBoundingBox(meshName)[1]
            max_bound = cmds.exactWorldBoundingBox(meshName)[4]

            # Calculate total height and target height
            top_y = max_bound
            bottom_y = min_bound
            total_height = top_y - bottom_y
            self.target_height = top_y - (total_height * percentage)

            # Get vertex position
            vertex_pos = cmds.pointPosition(
                meshName + ".vtx[" + str(vertexIndex) + "]", w=True
            )
            self.vertex_y = vertex_pos[1]

            # Compare vertex and target heights
        return self.vertex_y >= self.target_height

    def generatePointsAbove(self, baseMesh, density, height):
        self.points = []
        tempPoints = cmds.ls(baseMesh + ".vtx[*]", fl=1)
        for p in tempPoints:
            if r.random() <= density:
                if self.is_vertex_at_height_percentage(meshName=baseMesh, vertexIndex=tempPoints.index(p), percentage=height):
                    self.points.append(cmds.pointPosition(p, w=1))

    def generatePoints(self, baseMesh, density):
        self.points = []
        tempPoints = cmds.ls(baseMesh + ".vtx[*]", fl=1)
        for p in tempPoints:
            if r.random() <= density:
                self.points.append(cmds.pointPosition(p, w=1))


    def placePoints(self, branch):
        for p in self.points:
            name = cmds.spaceLocator(p=p)
            cmds.parent(name, branch)
