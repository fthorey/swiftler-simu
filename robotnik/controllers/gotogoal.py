#!/usr/bin/python
# coding: utf-8

from math import atan2, fabs, log, sin, cos, degrees, pi
from controllers.pidcontroller import PIDController

class GoToGoal(PIDController):
    """ The GoToGoal class steers the robot towards a goal with a certain linear velocity using PID
    """

    def __init__(self, info__):

        # Call PIDController constructor
        super(GoToGoal, self).__init__(info__)

    # Let's overwrite this way:
    def getHeadingAngle(self, info_):
        """Get the direction from the robot to the goal as a vector.
        """
        # The goal:
        x_g, y_g = info_.goal.x, info_.goal.y

        # The robot:
        x_r, y_r, theta = info_.pos

        # Heading angle:
        heading_angle = atan2(y_g - y_r, x_g - x_r) - theta

        # Avoid weird oscilations pi -> -pi -> pi -> ...
        # Return the goal in the robot's frame of reference?
        return (heading_angle + pi)%(2*pi) - pi
