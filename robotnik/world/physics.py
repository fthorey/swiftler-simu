#!/usr/bin/python
# coding: utf-8

from math import cos
from PyQt4 import QtGui, QtCore

class Physics(QtCore.QObject):
    """ The class Physics control the way the world is ruled.
    """

    def __init__(self, world_):

        # Set the world on which the physics apply
        self._world = world_

    def apply(self, ):
        """Applies physics at each time steps.
        """
        # Proximity sensors detection
        self.proximitySensorDetection()

    def __isSensorColliding(self, sensor_, collItems_):
        """Checks if its necessary to process the collision between the sensor
        and an item from the provided list of items.
        """
        def isARobot(item):
            """Checks if the item is the robot to which belong the sensor.
            """
            for robot in self._world.robots():
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

    def proximitySensorDetection(self, ):
        """Checks for collisions and update items if necessary.
        """
        # Check all sensors of all robots currently in the scene
        # Loop over robots
        for robot in self._world.robots():
            # Loop over robot sensors
            for sensor in robot.proxSensors():
                # Get all items in collision with the sensor
                collItems = self._world.collidingItems(sensor)
                # Recalculate the envelope of the sensor in the world
                sensor.getWorldEnvelope(True)
                # Check for a collision
                if self.__isSensorColliding(sensor, collItems):
                    # Update the sensor distance
                    for item in collItems:
                        sensor.updateDistance(item)
                else:
                    # Reset the sensor to its maximum range if not already
                    # if not sensor.isAtMaxRange():
                    sensor.updateDistance()

                # Stop the robot if the minimum range has been reached
                if sensor.isMinRangeReached():
                    robot.stop()
