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

            # Loop over sensors
            for sensor in robot.proxSensors():
                # Get all sensors that detect an obstacle
                if self.isSensorColliding(sensor):
                    while self.isSensorColliding(sensor):
                        # Reduce the beam of this sensor
                        sensor.reduceBeamRange(self._sensorReduction)
                        # Check if the sensor has reached its min beam range
                    if sensor.isMinRangeReached():
                        robot.stop()

                # Otherwise check if they are at their max range or not
                else:
                    # sensor.setBeamRange(sensor.getMaxBeamRange())
                    if sensor.getBeamRange() < sensor.getMaxBeamRange():
                        while not self.isSensorColliding(sensor):
                            if not sensor.isMaxRangeReached():
                                # Increase the beam of this sensor
                                sensor.increaseBeamRange(self._sensorReduction)
                            else:
                                break
