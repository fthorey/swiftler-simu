#!/usr/bin/python
# coding: utf-8

from utils import const
from utils.polygon import Polygon
from PyQt4 import QtGui, QtCore
from physics import Physics
from math import pi, degrees
from ui.worldrenderer import WorldRenderer
from utils.xmlreader import XMLReader
from utils import helpers

class World(WorldRenderer):
    """ World class provides access to all objects within the simulated environment
    """

    def __init__(self, parent_):
        """
        """
        # Call parent constructor
        super(World, self).__init__(parent_)

        # Physics that rules the world
        self.physics = Physics(self)

        # Create a xml reader object to parse world files
        self.xmlReader = XMLReader('templates/labyrinth_small.xml')

        # List of robots currently in the world
        self.robots = list()

        # List of obstacle currently in the world
        self.obstacles = list()

        # Store the current state of the zoom (robot or world)
        self.zoomOnRobot = False

        # Store if the robots sensors are displayed
        self.showRobotSensors = True

        # Store if path drawing is needed
        self.showTracks = True

        # store of the ghost mode is activated or not
        self.isGhostMode = True

    def isGhostModeActivated(self, ):
        """
        """
        return self.isGhostMode

    def toggleGhostMode(self, ):
        """
        """
        self.isGhostMode = not self.isGhostMode

    def toggleRobotTracks(self, ):
        """
        """
        self.showTracks = not self.showTracks

    def toggleRobotSensors(self, ):
        self.showRobotSensors = not self.showRobotSensors

        for robot in self.robots:
            robot.showProxSensors(self.showRobotSensors)

    # Toggle the current state of the zoom
    def setZoomOnRobot(self, zoom_):
        """
        """
        self.zoomOnRobot = zoom_

    # Get the current state of the zoom
    def isZoomOnRobot(self, ):
        """
        """
        return self.zoomOnRobot

    # Construct the world
    def autoConstruct(self, ):
        """
        """

        # Get all objects from xml
        objects = self.xmlReader.parseConfiguration()

        # To check if a master robot has been defined
        masterRobotSet = False
        for objs in objects:
            objsType = objs[0]
            if objsType is 'robot':
                # Get robot parameters
                robot_type, supervisor_type, robot_pos, robot_color, robot_dim = objs[1:6]
                # Get robot position (in m and rad)
                x, y, theta = robot_pos
                wR, wBL = robot_dim
                try:
                    # Get robot class
                    robot_class = helpers.load_by_name(robot_type,'robots')
                    # Get robot supervisor class
                    sup_class = helpers.load_by_name(supervisor_type,'supervisors')
                    # Generate a robot name
                    name = "Robot_{}:_{}".format(len(self.robots), sup_class.__name__)
                    robot = robot_class(name, wR, wBL)
                    # Set the 1st robot encountered the master robot
                    if not masterRobotSet:
                        robot.setMasterRobot()
                        masterRobotSet = True
                    # Add the robot to the obstacle list
                    self.addRobot(robot, QtCore.QPointF(x, y), theta)
                except:
                    print "[world.autoConstruct] Robot creation failed!"
                    raise
            elif objsType is 'obstacle':
                # Get obstacle parameters
                # Position are in m and rad
                obstacle_pos, obstacle_coords, obstacle_color = objs[1:4]
                # Set a default color
                if obstacle_color is None:
                    obstacle_color = 0xFF0000
                # Get obstacle attribute
                brush_ = QtGui.QBrush(QtGui.QColor(obstacle_color))
                pen_ = QtGui.QPen(QtCore.Qt.NoPen)
                obstacle = Polygon(obstacle_coords, brush_, pen_)
                # Add the obstacle to the world
                self.addItem(obstacle)
                # Get obstacle position (in m)
                x = obstacle_pos[0]
                y = obstacle_pos[1]
                theta = obstacle_pos[2]
                # Position the obstacle
                obstacle.setPos(QtCore.QPointF(x, y))
                obstacle.rotate(degrees(theta))
                # Add the obstacle to obstacles list
                self.obstacles.append(obstacle)
            else:
                print "{world.autConstruct] Can't recognized the item!"
                raise

    # Set the physics that rules the world
    def setPhysics(self, physics_):
        """
        """
        self.physics = physics_

    # Add a obstacle to the world
    # the position is given in m
    def addObstacle(self, obstacle_, position_, angle_):
        """
        """
        obstacle_.setPos(position_)
        obstacle_.setAngle(angle_)
        self.addItem(obstacle_)
        self.obstacles.append(obstacle_)

    # Add a robot to the world
    # The position is given in m
    def addRobot(self, robot_, position_, angle_):
        """
        """
        robot_.setInitialPos(position_, angle_)
        self.addItem(robot_)
        self.robots.append(robot_)

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
        # -> Call all items currently in the world advance method
        super(World, self).advance()

        # Update the view on the robot if necessary
        if self.zoomOnRobot:
            try:
                self.views()[0].focusOnRobot()
            except:
                pass

        # Apply physics
        self.physics.apply()

    def drawBackground(self, painter, rect):
        """
        """
        painter.setPen(self._gridPen)
        painter.setWorldMatrixEnabled(True);

        # left = int(rect.left()) - (int(rect.left()) % self._gridSize);
        # top = int(rect.top()) - (int(rect.top()) % self._gridSize);

        # lines = list()
        # x = left
        # while x < rect.right():
        #     lines.append(QtCore.QLineF(x, rect.top(), x, rect.bottom()))
        #     x += self._gridSize
        # y = top
        # while y < rect.bottom():
        #     lines.append(QtCore.QLineF(rect.left(), y, rect.right(), y))
        #     y += self._gridSize

        # painter.drawLines(lines)

        if self.showTracks:
            for robot in self.robots:
                painter.drawPath(robot.getTrack())
