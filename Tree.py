import maya.cmds as cmds
import maya.api.OpenMaya as om
import random

class PointPlacer:
    def __init__(self):
        self.points = []

    def is_vertex_at_height_percentage(self, mesh, vertex_index, percentage):
        min_bound, _, _, _, max_bound, _ = cmds.exactWorldBoundingBox(mesh)
        total_height = max_bound - min_bound
        target_height = max_bound - (total_height * percentage)
        vertex_pos = cmds.pointPosition(f"{mesh}.vtx[{vertex_index}]", w=True)
        return vertex_pos[1] >= target_height

    def generate_points_above(self, base_mesh, density, height):
        temp_points = cmds.ls(f"{base_mesh}.vtx[*]", fl=1)
        vertices = [f"{base_mesh}.vtx[{i}]" for i in range(len(temp_points))]
        vertex_positions = cmds.pointPosition(vertices, w=True)
        
        for i, point in enumerate(temp_points):
            if random.random() <= density and self.is_vertex_at_height_percentage(base_mesh, i, height):
                self.points.append(vertex_positions[i])

    def generate_points(self, base_mesh, density):
        temp_points = cmds.ls(f"{base_mesh}.vtx[*]", fl=1)
        vertices = [f"{base_mesh}.vtx[{i}]" for i in range(len(temp_points))]
        vertex_positions = cmds.pointPosition(vertices, w=True)

        for i, point in enumerate(temp_points):
            if random.random() <= density:
                self.points.append(vertex_positions[i])

    def place_points(self, branch):
        locators = cmds.spaceLocator(name=f"{branch}_loc#", position=self.points)
        cmds.parent(locators, branch)


def create_branch_non_recursive(i, dec, branch, high, den):
    stack = []
    pointy = PointPlacer()
    num = 0

    while True:
        if random.random() < i:
            if branch == "Trunk":
                pointy.generate_points_above(branch, den, height)
            else:
                pointy.generate_points(branch, den)

            instance_scale = [i, i * 2, i]
            rotation_values = [90 * random.random(), 180 * random.random(), 90 * random.random()]

            for point in pointy.points:
                new_name = f"{branch}_Branch{num}"
                print(f"Creating branch: {new_name}")
                new_instance = cmds.instance(branch, n=new_name)[0]
                cmds.parent(new_instance, branch)
                cmds.scale(instance_scale[0], instance_scale[1], instance_scale[2], new_instance)
                cmds.xform(new_instance, translation=(point[0] - pivot[0], point[1] - pivot[1], point[2] - pivot[2]), ws=1, ro=rotation_values)
                stack.append((i - dec, dec, new_name, high, den, num))
                num += 1

        elif branch != "Trunk":
            pointy.generate_points(branch, den)

            for point in pointy.points:
                new_name = f"{branch}_Leaf{num}"
                print(f"Creating leaf: {new_name}")
                new_instance = cmds.instance("Leaf1", n=new_name)[0]
                cmds.parent(new_instance, branch)
                cmds.xform(new_instance, translation=(point[0], point[1], point[2]), ws=1, ro=(180 * random.random(), 180 * random.random(), 180 * random.random()))
                num += 1

        if not stack:
            break

        i, dec, branch, high, den, num = stack.pop()


# Main code
random.seed(1)

radius = 0.5
height = 50
y_sub = 10
n = "Trunk"
ta = 0.1
sa = 0.5
density = 0.1

cmds.polyCylinder(n=n, sx=1, sy=y_sub, sz=1, radius=radius, height=height)
pivot = set_pivot_to_bottom(n)
create_branch_non_recursive(0.4, 0.2, n, height, density)

for i in range(10, y_sub * 2 * 10, 10):
    cmds.polySelect(n, el=i)
    cmds.polyMoveEdge(tx=random.random() * ta * 2 - ta, tz=random.random() * ta * 2 - ta,
                      sz=random.random() * sa + 0.8, sx=random.random() * sa + 0.8)

cmds.select(cl=1)
cmds.polySmooth(n, dv=2, kb=1)
set_pivot_to_bottom(n)
