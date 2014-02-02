#!/usr/bin/python
# coding: utf-8

from shape.shape import Shape
from PyQt4 import QtGui, QtCore
from utils import const

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

        # List of all proximity sensors of the robot
        self.proxSensors = list()

        # Is the robot master
        self.isMaster = False

    # Check if the robot is currently the master
    def isMasterRobot(self, ):
        return self.isMaster

    # Set master
    def setMasterRobot(self, ):
        self.isMaster = True

    # Set a goal
    def setGoal(self, goal_):
        """
        """
        self.supervisor.setGoal(goal_)

    # Get a goal
    def getGoal(self, ):
        """
        """
        return self.supervisor.getGoal()

    # Restart from the robot to its initial state
    def restart(self, ):
        """
        """
        # Set the initial postion (in m)
        self.setPos(self.initPos)
        # Set the initial heading angle (in rad)
        self.setTheta(self.initTheta)
        self.stopped = False
        # Restart all sensors
        for sensor in self.proxSensors:
            sensor.restart()

    # Set the initial position of the robot (in m & rad)
    def setInitialPos(self, pos_, theta_):
        """
        """
        # in m
        self.initPos = pos_
        # in rad
        self.initTheta = theta_

        # setPos and setTheta are in charge of converting m to pixel
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

        # Execute the supervisor
        self.supervisor.execute()

        # Update the robot dynamics
        self.dynamics.update()
