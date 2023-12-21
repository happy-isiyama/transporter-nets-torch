
# coding=utf-8
# Adapted from Ravens - Transporter Networks, Zeng et al., 2021
# https://github.com/google-research/ravens

"""Aligning task with Sandwich."""

import os

import numpy as np
from ravens_torch.tasks.task import Task
from ravens_torch.utils import utils


class AlignSandwichCorner(Task):
    """Aligning task with Sandwich."""

    def __init__(self):
        super().__init__()
        self.max_steps = 3
        self.fixed_sandwich_size = (0.1, 0.1, 0.1)

    def reset(self, env):
        super().reset(env)
        env.render()
        self._add_instance(env)

    def _add_instance(self, env):
        box_size = self.get_random_size(0.05, 0.15, 0.05, 0.15, 0.01, 0.06)
        box_size = (0.1, 0.1, 0.1)
        # Add sandwich URDF as an object
        # = 'convenience/box-template.urdf'
        #sandwich_template = 'bowl/bowl.urdf'
        #sandwich_urdf = self.fill_template(sandwich_template, {'DIM': self.fixed_sandwich_size})
        #sandwich_size = self.fixed_sandwich_size
        #sandwich_pose = self.get_random_pose(env, self.fixed_sandwich_size)
        #sandwich_pose = (sandwich_pose[0], utils.eulerXYZ_to_quatXYZW((0, np.pi/2, 0)))
        #sandwich_id = env.add_object(sandwich_urdf, sandwich_pose)
        #os.remove(sandwich_urdf)
        #self.color_random_brown(sandwich_id)
        # Add possible placing poses.
                #box_template = 'box/box-template.urdf'
        # Add corner.
        # Add possible placing poses.


        # Add corner.
        corner_template = 'corner/corner-template.urdf'
        #replace = {'DIMX': (0, 0), 'DIMY': (0, 0)}
        replace = {'DIMX': (0, 0.025), 'DIMY': (0, 0.025)}
        corner_urdf = self.fill_template(corner_template, replace)
        corner_size = (box_size[0], box_size[1], 0)
        corner_pose = self.get_random_pose(env, corner_size)
        env.add_object(corner_urdf, corner_pose, 'fixed')
        os.remove(corner_urdf)

        theta = utils.quatXYZW_to_eulerXYZ(corner_pose[1])[2]
        fip_rot = utils.eulerXYZ_to_quatXYZW((0, 0, theta + np.pi))
        pose1 = (corner_pose[0], fip_rot)
        alt_x = (box_size[0] / 2) - (box_size[1] / 2)
        alt_y = (box_size[1] / 2) - (box_size[0] / 2)
        alt_pos = (alt_x, alt_y, 0)
        alt_rot0 = utils.eulerXYZ_to_quatXYZW((0, 0, np.pi / 2))
        alt_rot1 = utils.eulerXYZ_to_quatXYZW((0, 0, 3 * np.pi / 2))
        pose2 = utils.multiply(corner_pose, (alt_pos, alt_rot0))
        pose3 = utils.multiply(corner_pose, (alt_pos, alt_rot1))

        box_template ="convenience/block.urdf"
        box_urdf = self.fill_template(box_template, {'DIM': box_size})
        box_pose = self.get_random_pose(env, box_size)
        box_id = env.add_object(box_urdf, box_pose)
        os.remove(box_urdf)
        self.color_random_brown(box_id)

        # Goal: sandwich is aligned with corner (1 of 4 possible poses).
        self.goals.append(([(box_id, (2 * np.pi, None))], np.int32([[1, 1, 1, 1]]),
                           [corner_pose, pose1, pose2, pose3],
                           False, True, 'pose', None, 1))
