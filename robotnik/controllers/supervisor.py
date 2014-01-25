#!/usr/bin/python
# coding: utf-8

from math import degrees, sqrt
from robots.robot import Robot
from controller import GoToGoal
from common import const

from PyQt4 import QtCore

class Supervisor(object):
    """ Supervisor class provides a way to control a robot
    """

    def __init__(self, robot_):
        """
        """
        # Robot supervised
        self.robot = robot_

        # Current controller
        self.controller = GoToGoal()

        # Current estimation of the robot position (in m) and angle (in rad)
        # in the scene referential
        self.stateEstimate = [self.robot.pos(), self.robot.getTheta()]

        # Goal expressed in the scene referential (in m)
        self.goal = QtCore.QPointF(1, 1)

        # Distance from the goal to which the robot stop (in m)
        self.stopDist          = 0.05

    # Select and execute the current controller
    def execute(self, stepDuration_):
        """
        """

    # Update the current estimation of the state of the robot position
    def updateOdometry(self, ):
        """
        """

    # Check if the robot is nearby enough its goal
    def isAtGoal(self, ):
        """
        """
        # Get goal coordinates (in m)
        xg = self.goal.x()
        yg = self.goal.y()

        # Get current robot position coordinates (in m)
        x = self.robot.pos().x()
        y = self.robot.pos().y()
        cDist = sqrt((x-xg)*(x-xg) + (y-yg)*(y-yg)) # (in m)

        return  cDist < self.stopDist

class WoggleSupervisor(Supervisor):
    """ WoggleSupervisor is a class that provides a way to control a Woggle robot
    """

    def __init__(self, robot_):
        """
        """
        # Call parent constructor
        super(WoggleSupervisor, self,).__init__(robot_);

    # Select and execute the current controller
    # The step duration is in seconds
    def execute(self, stepDuration_):
        """
        """

        if self.isAtGoal() or self.robot.isStopped():
            self.robot.setWheelSpeeds(0, 0)
            return

        # Execute the controller to obtain parameters to apply to the robot
        v, w = self.controller.execute(self.stateEstimate, self.goal, stepDuration_)

        # Convert speed (in m/s) and angular rotation (in rad/s) to
        # angular speed to apply to each robot wheels (in rad/s)
        vel_l, vel_r = self.robot.getDynamics().uni2Diff(v, w)

        # Apply current speed to wheels
        self.robot.setWheelSpeeds(vel_l, vel_r)

        # Update the estimate of the robot position
        self.updateOdometry()

    def updateOdometry(self, ):
        """
        """
        # For now, get exact robot position (in m) and angle (in rad)
        self.stateEstimate = [self.robot.pos(), self.robot.getTheta()]
