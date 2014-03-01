#!/usr/bin/python
# coding: utf-8

from math import atan2, fabs, log, sin, cos, degrees, pi
from controllers.pidcontroller import PIDController

class GoToGoal(PIDController):
    """ The GoToGoal class steers the robot towards a goal with a certain linear velocity using PID
    """

    def __init__(self, ):

        # PID gains
        coeff = {'Kp': 0.8,
                 'Ki': 0.1,
                 'Kd': 0.01}

        # Call PIDController constructor
        super(GoToGoal, self).__init__(coeff)

        self._goal = (1, -10)

    def getHeadingAngle(self, state_):
        """Get the direction in which the controller wants to move the robot
        """
        # Retrieve the goal location (in m)
        x_g, y_g = self._goal

        # Get an estimate of the current pos (in m and rad)
        x, y, theta = state_

        # 1. Calculate the heading (angle) to the goal

        # Distance between goal and robot in x-direction (in m)
        u_x = x_g - x

        # Distance between goal and robot in y-direction (in m)
        u_y = y_g - y

        # Angle from robot to goal. Use ATAN2 (in rad)
        theta_g = atan2(u_y, u_x)

        # 2. Calculate the heading error

        # Error between the goal angle and robot's angle
        # Use ATAN2 to make sure this stays in [-pi,pi]
        e_k = theta_g - theta
        return atan2(sin(e_k), cos(e_k))
