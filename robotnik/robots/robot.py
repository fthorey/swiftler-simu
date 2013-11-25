#!/usr/bin/python
# coding: utf-8

from common.shape import Shape
from PyQt4 import QtGui, QtCore

class Robot(Shape):
    """ Robot class handles a robot
    """

    # Constructor
    def __init__(self, name_, ):
        """
        """
        # Call parent constructor
        super(Robot, self).__init__(name_)

        # Dynamics followed by the robot
        self.dynamics = None

    # Set the dynamics followed by the robot
    def setDynamics(self, dynamics_):
        """
        """
        self.dynamics = dynamics_

    # Action to perform when the scene changes
    def advance(self, step_):
        """
        """
        if (not step_):
            return

        self.dynamics.update(self)
