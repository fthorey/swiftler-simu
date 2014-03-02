#!/usr/bin/python
# coding: utf-8

from math import atan2, fabs, log, sin, cos, degrees, pi, log1p
from controllers.pidcontroller import PIDController
import numpy as np
from PyQt4 import QtGui, QtCore

class AvoidObstacle(PIDController):
    """The AvoidObstacles class steers the robot to a direction calculated with
    the weighted sum of direction of obstacles detected by each sensors
    """

    def __init__(self, info_):

        # Call PIDController constructor
        super(AvoidObstacle, self).__init__(info_)

    def getHeading(self, info_):
        """Get the direction in which the controller wants to move the robot
        as a vector.

        return a numpy array [x, y, z] with z = 1.
        """
        # Map the sensors distance to the robot's frame of reference
        end_w = [s.mapToParent(QtCore.QPointF(d, 0)) for s, d in zip(info_.sensors.insts,
                                                                     info_.sensors.dist)]

        # Return the y-axis (Qt works with a strange frame of reference)
        end_w = np.array([(end.x(), -end.y(), 1) for end in end_w])

        # Get the resulting vector in the robot's frame of reference
        sum_w = np.sum(end_w, axis=0)
        return sum_w
