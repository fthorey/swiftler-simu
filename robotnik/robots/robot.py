#!/usr/bin/python
# coding: utf-8

from common import const
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

        # Supervisor to run the robot
        self.supervisor = None

    # Set the dynamics followed by the robot
    def setDynamics(self, dynamics_):
        """
        """
        self.dynamics = dynamics_

    # Set the supervisor that run the robot
    def setSupervisor(self, supervisor_):
        """
        """
        self.supervisor = supervisor_

    # Get the supervisor of the robot
    def getSupervisor(self, ):
        """
        """
        return self.supervisor

    # Get the dynamic of the robot
    def getDynamics(self, ):
        """
        """
        return self.dynamics

    # Action to perform when the scene changes
    def advance(self, step_):
        """
        """
        if (not step_):
            return

        # Execute the supervisor
        self.supervisor.execute(const.stepDuration)

        # Update the robot dynamics
        self.dynamics.update(const.stepDuration)
