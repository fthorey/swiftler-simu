#!/usr/bin/python
# coding: utf-8

from math import degrees, sqrt

from PyQt4 import QtCore

class Supervisor(object):
    """The supervisor class oversees the control of a single robot.
    """

    def __init__(self, robot_):
        # Robot supervised
        self._robot = robot_

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

    def stateEstimate(self, ):
        """Return an estimate of the state of the robot (x,y,theta).
        """
        return self._stateEstimate

    def setStateEstimate(self, x, y, theta):
        """Set the current estimate of the state of the robot.
        """
        # Current estimation of the robot position (in m) and angle (in rad)
        # in the scene referential
        self._stateEstimate = {'x': x, 'y': y, 'theta': theta, }

    def execute(self, ):
        """Select and execute the current controller.
        """
        raise NotImplementedError("Supervisor.execute")

    def updateOdometry(self, ):
        """Update the current estimation of the state of the robot position.
        """
        raise NotImplementedError("Supervisor.updateOdometry")

    def restart(self, ):
        """Restart.
        """
        raise NotImplementedError("Supervisor.restart")

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
