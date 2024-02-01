import maya.cmds as cmds

def create_branch(parent, branch_length, num_sub_branches, angle):
    if num_sub_branches == 0:
        return

    # Create a new joint for the branch
    branch_joint = cmds.createNode('joint')
    cmds.setAttr(branch_joint + '.translateY', branch_length)
    cmds.setAttr(branch_joint + '.radius', 0.1)

    # Rotate the joint
    cmds.rotate(angle, 0, 0, branch_joint, relative=True)

    # Parent the joint to the hierarchy
    cmds.parent(branch_joint, parent)

    # Recursive call for sub-branches
    create_branch(branch_joint, branch_length * 0.7, num_sub_branches - 1, angle)
    create_branch(branch_joint, branch_length * 0.7, num_sub_branches - 1, -angle)

def create_tree():
    # Create a base joint for the trunk
    trunk_joint = cmds.createNode('joint')
    cmds.setAttr(trunk_joint + '.radius', 0.2)

    # Set up parameters for the tree
    trunk_length = 5.0
    num_sub_branches = 3
    angle = 30.0

    # Create branches independently and then parent them
    for _ in range(2):
        create_branch(trunk_joint, trunk_length, num_sub_branches, angle)

# Run the function to create the tree
create_tree()
