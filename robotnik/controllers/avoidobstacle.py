#!/usr/bin/python
# coding: utf-8

from math import atan2, fabs, log, sin, cos, degrees, pi
from controllers.pidcontroller import PIDController

class AvoidObstacle(PIDController):
    """The AvoidObstacles class steers the robot to a direction calculated with
    the weighted sum of direction of obstacles detected by each sensors
    """

    def __init__(self, proxSensors_):

        # PID gains
        coeff = {'Kp': 0.8,
                 'Ki': 0.1,
                 'Kd': 0.01}

        self._proxSensors = proxSensors_

        # Call PIDController constructor
        super(AvoidObstacle, self).__init__(coeff)

    def getHeadingAngle(self, state_, goal_):
        """Get the direction in which the controller wants to move the robot.
        """
        return 0
