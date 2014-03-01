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

    # Let's overwrite this way:
    def getHeadingAngle(self, state_):
        """Get the direction from the robot to the goal as a vector.
        """
        # The goal:
        x_g, y_g = state_.goal.x, state_.goal.y

        # The robot:
        x_r, y_r, theta = state_.pos

        # Where is the goal in the robot's frame of reference?
        return atan2(y_g - y_r, x_g - x_r) - theta
