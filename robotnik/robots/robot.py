#!/usr/bin/python
# coding: utf-8

from common.shape import Shape
from PyQt4 import QtGui, QtCore
from common import const

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

        # Initial position (in m)
        self.initPos = QtCore.QPointF(0, 0)

        # Initial heading angle (in rad)
        self.initTheta = 0

        # Duration of a step (in s)
        self.stepDuration = 0

        # List of all proximity sensors of the robot
        self.proxSensors = list()

    # Update the step duration (in s)
    def updateStepDuration(self, duration_):
        """
        """
        # The step duration is updated in s
        self.stepDuration = duration_

    # Set the initial position of the robot (in m & rad)
    def setInitialPos(self, pos_, theta_):
        """
        """
        # in m
        self.initPos = pos_
        # in rad
        self.initTheta = theta_

        # setPos and setTheta are in charge
        # of converting m to pixel
        self.setPos(pos_)
        self.setTheta(theta_)

    # Get the initial position of the robot (in m & rad)
    def getInitialPos(self, ):
        """
        """
        return self.initPos, self.initTheta

    # Set the dynamics followed by the robot
    def setDynamics(self, dynamics_):
        """
        """
        self.dynamics = dynamics_

    # Get the dynamic of the robot
    def getDynamics(self, ):
        """
        """
        return self.dynamics

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
        # Called twice by QGraphicsScene::advance() First, with step_ == 0: about to advance,
        # and then called with phase == 1, advance effectively
        # -> Do nothing on the 1st phase but move on 2nd phase
        if (step_ == 0):
            return

        # Execute the supervisor (duration in s)
        self.supervisor.execute(self.stepDuration)

        # Update the robot dynamics (duration in s)
        self.dynamics.update(self.stepDuration)
