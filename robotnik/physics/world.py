#!/usr/bin/python
# coding: utf-8

from common import const
from PyQt4 import QtGui, QtCore
from physics import Physics
from math import pi

class World(QtGui.QGraphicsScene):
    """ World class provides access to all objects within the simulated environment
    """

    def __init__(self, parent_, stepDuration_, length_, height_):
        """
        """
        # Call parent constructor
        super(World, self).__init__(parent_)

        # Physics that rules the world
        self.physics = Physics(self, stepDuration_)

        # List of robots currently in the world
        self.robots = list()

        # List of furniture currently in the world
        self.furnitures = list()

        # Duration of a step (in s)
        self.stepDuration = stepDuration_

        # Define world dimension (in m)
        self.length = length_
        self.height = height_

        # Set scene bounding rectangle
        # setSceneRect takes parameters expressed in pixel
        # -> Value in m are converted to pixel
        self.setSceneRect(-(self.length/2)*const.m2pix, -(self.height/2)*const.m2pix,
                          (self.length)*const.m2pix, (self.height)*const.m2pix);

    # Update the step duration (in s)
    def updateStepDuration(self, duration_):
        """
        """
        self.stepDuration = duration_
        self.physics.updateStepDuration(self.stepDuration)

    # Set the physics that rules the world
    def setPhysics(self, physics_):
        """
        """
        self.physics = physics_

    # Add a furniture to the world
    # the position is given in m
    def addFurniture(self, furniture_, position_):
        """
        """
        furniture_.setPos(position_)
        self.addItem(furniture_)
        self.furnitures.append(furniture_)

    # Add a robot to the world
    # The position is given in m
    def addRobot(self, robot_, position_, duration_):
        """
        """
        robot_.setInitialPos(position_, pi)
        self.addItem(robot_)
        self.robots.append(robot_)
        robot_.updateStepDuration(duration_)

    # Return the current physics of the world
    def getPhysics(self, ):
        """
        """
        return self.physics

    # Return a list of all robots in the world
    def getRobots(self, ):
        """
        """
        return self.robots

    # Return a list of all furnitures in the wolrd
    def getFurnitures(self, ):
        """
        """
        return self.furnitures

    # Action to perform when the scene changes
    def advance(self, ):
        """
        """
        # Call parent advance method
        super(World, self).advance()

        # Apply physics
        self.physics.apply()
