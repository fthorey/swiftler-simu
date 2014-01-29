#!/usr/bin/python
# coding: utf-8

from utils import const
from math import cos
from PyQt4 import QtGui, QtCore

class Physics(object):
    """ Physics that rules a world
    """

    # Constructor
    # The step duration is given in s
    def __init__(self, world_, stepDuration_):
        """
        """
        # Set the world on which the physics apply
        self.world = world_

        # Duration of a step (in s)
        self.stepDuration = stepDuration_

    # Update the step duration (in s)
    def updateStepDuration(self, duration_):
        """
        """
        self.stepDuration = duration_

    # Apply physics at each step
    def apply(self, ):
        """
        """
        # Proximity sensors detection
        self.proximitySensorDetection()

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
                    while self.world.collidingItems(sensor):
                        # Reduce the beam of this sensor of 1 pixel
                        sensor.reduceBeamRange(const.pix2m)
                        # Check if the sensor has reached its min beam range
                    if sensor.isMinRangeReached():
                        robot.stop()

                # Otherwise check if they are at their max range or not
                else:
                    # sensor.setBeamRange(sensor.getMaxBeamRange())
                    if sensor.getBeamRange() < sensor.getMaxBeamRange():
                        while not self.world.collidingItems(sensor):
                            if not sensor.isMaxRangeReached():
                                # Increase the beam of this sensor of 1 pixel
                                sensor.increaseBeamRange(const.pix2m)
                            else:
                                break
