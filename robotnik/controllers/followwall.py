#!/usr/bin/python
# coding: utf-8

from controllers.pidcontroller import PIDController
import numpy as np
from math import pi

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
        direction = info_.direction

        dirFactor = -1
        if direction is 'left':
            dirFactor = 1

        sensors = [(s, d) for s, d in zip(info_.sensors.insts, info_.sensors.dist)
                   if (0 < (s.angle() * dirFactor) < pi) and (d < info_.sensors.rmax)]

        # Now make sure they are sorted from front to back
        sensors = sorted(sensors, key = lambda (p, d): abs(p.angle()))

        # No wall - drive a bit to the wall
        if len(sensors) == 0:
            return np.array([0.8, dirFactor*0.6, 1])

        # Calculate vectors for each detecting sensors
        vectors = np.array([s.mapToParent(d, 0) for s, d in sensors])

        # Only one sensor detect a wall
        if len(sensors) == 1:
            pass

        # More than one sensor detect the wall
        else:
            # Take the fist and the last
            along_wall_vector = vectors[0] - vectors[-1]
            return along_wall_vector

            # a = self.vectors[-1]
            # b = self.along_wall_vector
            # dot = numpy.dot
            # self.to_wall_vector = a - b*dot(a,b)/dot(b,b)

        return np.array([0, 0, 1])
