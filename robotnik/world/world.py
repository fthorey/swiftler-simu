#!/usr/bin/python
# coding: utf-8

from utils import const
from PyQt4 import QtGui, QtCore
from physics import Physics
from math import pi
from ui.worldrenderer import WorldRenderer
from utils.xmlreader import XMLReader
from utils import helpers

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

        # Create a xml reader object to parse world files
        self.xmlReader = XMLReader('templates/labyrinth_small.xml')

        # List of robots currently in the world
        self.robots = list()

        # List of obstacle currently in the world
        self.obstacles = list()

        # Duration of a step (in s)
        self.stepDuration = stepDuration_

    # Construct the world
    def autoConstruct(self, ):

        # Get all objects from xml
        objects = self.xmlReader.parseConfiguration()

        for objs in objects:
            objsType = objs[0]
            if objsType is 'robot':
                # Get robot parameters
                robot_type, supervisor_type, robot_pos, robot_color = objs[1:5]
                # Get robot position
                x, y, theta = robot_pos
                try:
                    # Get robot class
                    robot_class = helpers.load_by_name(robot_type,'robots')
                    # Get robot supervisor class
                    sup_class = helpers.load_by_name(supervisor_type,'supervisors')
                    # Generate a robot name
                    name = "Robot_{}:_{}".format(len(self.robots), sup_class.__name__)
                    robot = robot_class(name, 0.021, 0.0885)
                    self.addRobot(robot, QtCore.QPointF(x, y), theta)
                except:
                    print "[Simulator.construct_world] Robot creation failed!"
                    raise
            elif objsType is 'obstacle':
                obstacle_pos, obstacle_coords, obstacle_color = objs[1:4]
                if obstacle_color is None:
                    obstacle_color = 0xFF0000
                obstacle_coords = [coord*const.m2pix for coord in obstacle_coords]
                obstacle = self.addPolygon(QtGui.QPolygonF(obstacle_coords))
                x = obstacle_pos[0]*const.m2pix
                y = obstacle_pos[1]*const.m2pix
                obstacle.setPos(QtCore.QPointF(x, y))
                self.obstacles.appends(obstacle)
            else:
                print "{Simulator.construct_world] Can't recognized the item!"
                raise

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
    def addRobot(self, robot_, position_, theta_):
        """
        """
        robot_.setInitialPos(position_, theta_)
        self.addItem(robot_)
        self.robots.append(robot_)
        robot_.updateStepDuration(self.stepDuration)

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
