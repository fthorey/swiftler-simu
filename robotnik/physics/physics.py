#!/usr/bin/python
# coding: utf-8

from common import const
from math import cos
from PyQt4 import QtGui, QtCore

class Physics(object):
    """ Physics that rules a world
    """

    def __init__(self, world_):
        """
        """
        # Set the world on which the physics apply
        self.world = world_

    # Apply physics at each step
    def apply(self, ):
        """
        """
        # Detect bodies collision
        self.detectBodyCollision()

        # Proximity sensors detection
        self.proximitySensorDetection()

    # Detect body collision
    def detectBodyCollision(self, ):
        """
        """

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
                if self.world.collidingItems(sensor):
                    # Reduce the beam of the sensor
                    # sensor.reduceBeamRange(robot.getSpeed() * const.stepDuration * 1e-3)
                    # Check if the sensor has reached its min beam range
                    if sensor.isMinRangeReached():
                        print 'stop'
                        robot.stop()
