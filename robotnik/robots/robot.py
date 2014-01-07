#!/usr/bin/python
# coding: utf-8

from common import const
from common.shape import Shape
from PyQt4 import QtGui, QtCore

class Robot(Shape):
    """ Robot class handles a robot
    """

    # Constructor
    def __init__(self, name_):
        """
        """
        # Call parent constructor
        super(Robot, self).__init__(name_)

        # Dynamics followed by the robot
        self.dynamics = None

        # Supervisor to run the robot
        self.supervisor = None

        # Is the robot stopped
        self.stopped = False

        # Initial position
        self.initPos = QtCore.QPointF(0, 0)

        # Initial theta angle
        self.initTheta = 0

        # Duration of a step
        self.stepDuration = 0

    # Update the step duration
    def updateStepDuration(self, duration_):
        """
        """
        self.stepDuration = duration_

    # Set the initial position of the robot
    def setInitialPos(self, pos_, theta_):
        """
        """
        self.initPos = pos_
        self.initTheta = theta_

        self.setPos(pos_)
        self.setTheta(theta_)

    # Get the initial position of the robot
    def getInitialPos(self, ):
        """
        """
        return self.initPos, self.initTheta

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

    # Get current speed
    def getSpeed(self, ):
        """
        """
        v, w = self.dynamics.diff2Uni(self.leftWheelSpeed, self.rightWheelSpeed)
        return v

    # Stop the robot
    def stop(self, ):
        """
        """
        self.stopped = True

    # Check if the robot is stopped
    def isStopped(self, ):
        """
        """
        return self.stopped

    # Action to perform when the scene changes
    def advance(self, step_):
        """
        """
        if (not step_):
            return

        # Execute the supervisor
        self.supervisor.execute(self.stepDuration)

        # Update the robot dynamics
        self.dynamics.update(self.stepDuration)
