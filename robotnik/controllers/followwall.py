#!/usr/bin/python
# coding: utf-8

from controllers.pidcontroller import PIDController
import numpy as np

class FollowWall(PIDController):
    """The FollowWall class steers the robot to a direction that is a linear combination
    of a vector tangential and a vector normal to a wall
    """

    def __init__(self, info_):

        # Call PIDController constructor
        super(FollowWall, self).__init__(info_)

    def getHeading(self, info_):
        """Get the direction in which the controller wants to move the robot
        as a vector.
        """
        return np.array([0, 0, 1])
