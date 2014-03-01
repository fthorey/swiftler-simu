#!/usr/bin/python
# coding: utf-8

from math import degrees, sqrt

from PyQt4 import QtCore

class Supervisor(object):
    """The supervisor class oversees the control of a single robot.
    """

    def __init__(self, robot_, pos_):
        # Robot supervised
        self._robot = robot_

        # Initialize the estimation of the position
        self._posEstimate = pos_

    def posEstimate(self, ):
        """Get the current estimation of the position.
        """
        return self._posEstimate

    def setPosEstimate(self, pos_):
        """Update the current estimation of the position.
        """
        self._posEstimate = pos_

    def stopDist(self, ):
        """Return the distance from an obstacle to which the robot stops.
        """
        return self._stopDist

    def setStopDist(self, stopDist_):
        """Set the distance from an obstacle to which the robot stops.
        """
        self._stopDist = stopDist_

    def robot(self, ):
        """Return the robot controlled by the supervisor.
        """
        return self._robot

    def setGoal(self, xg_, yg_):
        """Set the goal of the robot.
        """
        self._goal = QtCore.QPointF(xg_, yg_)

    def goal(self, ):
        """Return the goal of the robot.
        """
        return self._goal.x(), self._goal.y()

    def execute(self, ):
        """Select and execute the current controller.
        """
        raise NotImplementedError("Supervisor.execute")

    def updateOdometry(self, ):
        """Update the current estimation of the state of the robot position.
        """
        raise NotImplementedError("Supervisor.updateOdometry")

    def isAtGoal(self, ):
        """Check if the robot is nearby enough its goal.
        """

        # Get goal coordinates (in m)
        xg = self._goal.x()
        yg = self._goal.y()

        # Get current robot position coordinates (in m)
        from robots.robot import Robot
        x = self._robot.pos().x()
        y = self._robot.pos().y()
        cDist = sqrt((x-xg)*(x-xg) + (y-yg)*(y-yg)) # (in m)

        return  cDist < self._stopDist
