import maya.cmds as cmds
import math as m

def create_tree(trunk_height=5, trunk_radius=0.5, num_branches=3, branch_length=3, branch_angle=30):
    # Create trunk
    trunk_curve = cmds.curve(d=1, p=[(-trunk_radius, 0, 0), (trunk_radius, 0, 0)])
    cmds.scale(1, trunk_height, 1, trunk_curve)

    # Create branches
    for i in range(num_branches):
        angle_rad = m.radians(branch_angle * i)
        branch_curve = cmds.duplicate(trunk_curve)[0]
        cmds.rotate(0, 0, angle_rad, branch_curve)
        cmds.move(0, trunk_height, 0, branch_curve, r=True)
        cmds.scale(1, branch_length, 1, branch_curve)

    # Group all the curves
    tree_group = cmds.group(trunk_curve, "curve*", name="tree_grp")

    return tree_group

# Example usage:
tree = create_tree(trunk_height=5, trunk_radius=0.5, num_branches=3, branch_length=3, branch_angle=45)
