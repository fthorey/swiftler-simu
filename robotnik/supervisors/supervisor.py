#!/usr/bin/python
# coding: utf-8

from math import degrees, sqrt
from robots.robot import Robot
from controllers.controller import GoToGoal, Rotate
from utils import const

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
        self.controller = Rotate()

        # Current estimation of the robot position (in m) and angle (in rad)
        # in the scene referential
        self.stateEstimate = [self.robot.pos(), self.robot.getTheta()]

        # Goal expressed in the scene referential (in m)
        self.goal = QtCore.QPointF(0, 0)

        # Distance from the goal to which the robot stop (in m)
        self.stopDist          = 0.05

    # Get goal
    def getGoal(self, ):
        """
        """
        return self.goal

    # Set a goal
    def setGoal(self, goal_):
        """
        """
        self.goal = goal_

    # Select and execute the current controller
    def execute(self, ):
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
