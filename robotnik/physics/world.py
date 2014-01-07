#!/usr/bin/python
# coding: utf-8

from common import const
from PyQt4 import QtGui, QtCore
from physics import Physics
from math import pi

class World(QtGui.QGraphicsScene):
    """ World class provides access to all objects within the simulated environment
    """

    def __init__(self, parent):
        """
        """
        # Call parent constructor
        super(World, self).__init__(parent)

        # Physics that rules the world
        self.physics = Physics(self)

        # List of robots currently in the world
        self.robots = list()

        # List of furniture currently in the world
        self.furnitures = list()

    # Set the physics that rules the world
    def setPhysics(self, physics_):
        """
        """
        self.physics = physics_

    # Add a furniture to the world
    def addFurniture(self, furniture_, position_):
        """
        """
        furniture_.setPos(position_)
        self.addItem(furniture_)
        self.furnitures.append(furniture_)

    # Add a robot to the world
    def addRobot(self, robot_, position_, duration_):
        """
        """
        robot_.setInitialPos(position_, pi)
        self.addItem(robot_)
        self.robots.append(robot_)
        robot_.updateStepDuration(duration_)

    # Return a list of all robots in the wolrd
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
