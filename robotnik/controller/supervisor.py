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

        # Robot to be supervised
        self.robot = robot_

        # Current controller
        self.controller = GoToGoal()

        # Current estimates of the robot position in the scene referential
        self.stateEstimate = [self.robot.pos(), self.robot.getTheta()]

        # Goal expressed in the scene referential
        self.goal = QtCore.QPointF(-0.25*const.m2pix*const.scaleFactor,
                                   -0.15*const.m2pix*const.scaleFactor)

        # Distance from the goal to which the robot stop
        self.stopDist          = 0.005*const.m2pix*const.scaleFactor

    # Select and execute the current controller
    def execute(self, stepDuration_):
        """
        """

    # Update the current state estimate of the robot position
    def updateOdometry(self, ):
        """
        """

    # Check if the robot is nearby enough its goal
    def isAtGoal(self, ):
        """
        """
        # Get goal coordinates
        xg = self.goal.x()
        yg = self.goal.y()

        # Get current robot position coordinates
        x = self.robot.pos().x()
        y = self.robot.pos().y()
        cDist = sqrt((x-xg)*(x-xg) + (y-yg)*(y-yg))

        return  cDist < self.stopDist


class WoggleSupervisor(Supervisor):
    """ WoggleSupervisor is a class that provides a way to control a Woggle robot
    """

    def __init__(self, robot_):
        """
        """
        # Call parent constructor
        super(WoggleSupervisor, self,).__init__(robot_);

    # select and execute the current controller
    def execute(self, stepDuration_):
        """
        """

        if self.isAtGoal():
            self.robot.setWheelSpeeds(0, 0)
            return

        # Execute the controller to obtain parameters to apply to the robot
        v, w = self.controller.execute(self.stateEstimate, self.goal, stepDuration_)

        # Convert speed and angular rotation to angular speed to apply to each robot wheels
        vel_l, vel_r = self.robot.getDynamics().uni2Diff(v, w)

        # Apply current speed to wheels
        self.robot.setWheelSpeeds(vel_l, vel_r)

        # Update the estimate of the robot position
        self.updateOdometry()

    def updateOdometry(self, ):
        """
        """
        # For now, get exact robot position and angle
        self.stateEstimate = [self.robot.pos(), self.robot.getTheta()]
