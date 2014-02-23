#!/usr/bin/python
# coding: utf-8

from utils import const
from math import cos
from PyQt4 import QtGui, QtCore

class Physics(QtCore.QObject):
    """ Physics that rules a world
    """

    # Constructor
    # The step duration is given in s
    def __init__(self, world_):
        """
        """
        super(QtCore.QObject, self).__init__()

        # Set the world on which the physics apply
        self._world = world_

    # Apply physics at each step
    def apply(self, ):
        """
        """
        # Proximity sensors detection
        self.proximitySensorDetection()

    def isSensorColliding(self, sensor_, collItems_):

        def isARobot(item):
            for robot in self._world.getRobots():
                if item in robot.getAllItems():
                    return True
            return False

        for item in collItems_:
            # Check if the item is a robot or affiliated
            if isARobot(item):
                # If ghost mode activated, continue, else return False
                if self._world.isGhostModeActivated():
                    continue
                else:
                    myRobot = sensor_.parentItem()
                    if item in myRobot.getAllItems():
                        continue
                    return True
            # If the item is not a robot (or affiliated) return False
            else:
                return True

        # Return False by default
        return False

    # Proximity sensors collision
    def proximitySensorDetection(self, ):
        """
        """
        # Check all sensors of all robots currently in the scene
        # Loop over robots
        for robot in self._world.getRobots():

            # Don't check for collision if the robot is already stopped
            if robot.isStopped():
                continue

            # Loop over robot sensors
            for sensor in robot.proxSensors():
                # Get all items in collision with the sensor
                collItems = self._world.collidingItems(sensor)
                # Recalculate the envelope of the sensor in the world
                sensor.getWorldEnvelope(True)
                # Check for a collision
                if self.isSensorColliding(sensor, collItems):
                    # Update the sensor distance
                    for item in collItems:
                        sensor.updateDistance(item)
                else:
                    # Reset the sensor to its maximum range if not already
                    if not sensor.isAtMaxRange():
                        sensor.updateDistance()
