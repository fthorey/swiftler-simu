#!/usr/bin/python
# coding: utf-8

from utils import const
from PyQt4 import QtGui, QtCore
from physics import Physics
from math import pi
from ui.worldrenderer import WorldRenderer

class World(WorldRenderer):
    """ World class provides access to all objects within the simulated environment
    """

    def __init__(self, parent_, stepDuration_, size_):
        """
        """
        # Call parent constructor
        super(World, self).__init__(parent_, size_)

        # Physics that rules the world
        self.physics = Physics(self, stepDuration_)

        # List of robots currently in the world
        self.robots = list()

        # List of obstacle currently in the world
        self.obstacles = list()

        # Duration of a step (in s)
        self.stepDuration = stepDuration_

    # Update the step duration (in s)
    def updateStepDuration(self, duration_):
        """
        """
        # Update step duration (in s)
        self.stepDuration = duration_
        # Update physics step duration (in s)
        self.physics.updateStepDuration(self.stepDuration)
        # Update robots step duration (in s)
        for robot in self.robots:
            robot.updateStepDuration(self.stepDuration)

    # Set the physics that rules the world
    def setPhysics(self, physics_):
        """
        """
        self.physics = physics_

    # Add a obstacle to the world
    # the position is given in m
    def addObstacle(self, obstacle_, position_, theta_):
        """
        """
        obstacle_.setPos(position_)
        obstacle_.setTheta(theta_)
        self.addItem(obstacle_)
        self.obstacles.append(obstacle_)

    # Add a robot to the world
    # The position is given in m
    def addRobot(self, robot_, position_, theta_, duration_):
        """
        """
        robot_.setInitialPos(position_, theta_)
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

    # Return a list of all obstacles in the wolrd
    def getObstacles(self, ):
        """
        """
        return self.obstacles

    # Action to perform when the scene changes
    def advance(self, ):
        """
        """
        # Call parent advance method
        super(World, self).advance()

        # Apply physics
        self.physics.apply()
