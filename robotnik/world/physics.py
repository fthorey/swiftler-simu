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
        # Set the world on which the physics apply
        self.world = world_

    # Apply physics at each step
    def apply(self, ):
        """
        """
        # Proximity sensors detection
        self.proximitySensorDetection()

    def isSensorColliding(self, sensor):
        colItems = self.world.collidingItems(sensor)

        for item in colItems:
            robot = sensor.parentItem()
            if item is robot:
                continue
            elif item in robot.getProxSensors():
                continue
            elif item is self.world.getRobotTrack(robot):
                continue
            else:
                return True

        return False

    # Proximity sensors collision
    def proximitySensorDetection(self, ):
        """
        """
        # Check all sensors of all robots currently in the scene
        # Loop over robots
        for robot in self.world.getRobots():
            # Loop over sensors
            for sensor in robot.getProxSensors():

                # Get all sensors that detect an obstacle
                if self.isSensorColliding(sensor):
                    while self.isSensorColliding(sensor):
                        # Reduce the beam of this sensor of 1 pixel
                        sensor.reduceBeamRange(const.pix2m)
                        # Check if the sensor has reached its min beam range
                    if sensor.isMinRangeReached():
                        robot.stop()

                # Otherwise check if they are at their max range or not
                else:
                    # sensor.setBeamRange(sensor.getMaxBeamRange())
                    if sensor.getBeamRange() < sensor.getMaxBeamRange():
                        while not self.isSensorColliding(sensor):
                            if not sensor.isMaxRangeReached():
                                # Increase the beam of this sensor of 1 pixel
                                sensor.increaseBeamRange(const.pix2m)
                            else:
                                break
