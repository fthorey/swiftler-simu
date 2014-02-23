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

class World(QtGui.QGraphicsScene):
    """ World class provides access to all objects within the simulated environment
    """

    def __init__(self, parent_):
        """
        """
        # Call parent constructor
        super(World, self).__init__(parent_)

        # Physics that rules the world
        self._physics = Physics(self)

        # Create a xml reader object to parse world files
        self._xmlReader = XMLReader('templates/labyrinth_small.xml')

        # Define a grid size of 10cm
        self._gridSize = 0.1

        # Type of the grid pen
        self._gridPen = QtGui.QPen(QtGui.QColor(0x808080))

        # List of robots currently in the world
        self._robots = list()

        # List of obstacle currently in the world
        self._obstacles = list()

        # Store the current state of the zoom (robot or world)
        self._zoomOnRobot = False

        # Store if the robots sensors are displayed
        self._showRobotSensors = True

        # Store if path drawing is needed
        self._showTracks = True

        # store of the ghost mode is activated or not
        self._isGhostMode = True

    def getRobots(self, ):
        """
        """
        return self._robots

    def isZoomOnRobot(self, ):
        """
        """
        return self._zoomOnRObot

    def isGhostModeActivated(self, ):
        """
        """
        return self._isGhostMode

    def toggleGhostMode(self, ):
        """
        """
        self._isGhostMode = not self._isGhostMode

    def toggleRobotTracks(self, ):
        """
        """
        self._showTracks = not self._showTracks

    def toggleRobotSensors(self, ):
        self._showRobotSensors = not self._showRobotSensors

        for robot in self._robots:
            robot.showProxSensors(self._showRobotSensors)

    # Toggle the current state of the zoom
    def setZoomOnRobot(self, zoom_):
        """
        """
        self._zoomOnRobot = zoom_

    # Get the current state of the zoom
    def isZoomOnRobot(self, ):
        """
        """
        return self._zoomOnRobot

    # Construct the world
    def autoConstruct(self, ):
        """
        """

        # Get all objects from xml
        objects = self._xmlReader.parseConfiguration()

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
                    name = "Robot_{}:_{}".format(len(self._robots), sup_class.__name__)
                    brush = QtGui.QBrush(QtGui.QColor(robot_color))
                    pen = QtGui.QPen(QtCore.Qt.NoPen)
                    robot = robot_class(name, wR, wBL, brush, pen)
                    # Set the 1st robot encountered the master robot
                    if not masterRobotSet:
                        robot.setMasterRobot()
                        masterRobotSet = True
                    # Add the robot to the wo
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
                brush = QtGui.QBrush(QtGui.QColor(obstacle_color))
                pen = QtGui.QPen(QtCore.Qt.NoPen)
                obstacle = Polygon(obstacle_coords, brush, pen)
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
                self._obstacles.append(obstacle)
            else:
                print "{world.autConstruct] Can't recognized the item!"
                raise

    # Set the physics that rules the world
    def setPhysics(self, physics_):
        """
        """
        self._physics = physics_

    # Add a robot to the world
    # The position is given in m
    def addRobot(self, robot_, position_, angle_):
        """
        """
        robot_.setInitialPos(position_, angle_)
        self.addItem(robot_)
        self._robots.append(robot_)

    # Return the current physics of the world
    def getPhysics(self, ):
        """
        """
        return self._physics

    # Return a list of all robots in the world
    def getRobots(self, ):
        """
        """
        return self._robots

    # Return a list of all obstacles in the wolrd
    def getObstacles(self, ):
        """
        """
        return self._obstacles

    # Action to perform when the scene changes
    def advance(self, ):
        """
        """
        # Call parent advance method
        # -> Call all items currently in the world advance method
        super(World, self).advance()

        # Update the view on the robot if necessary
        if self._zoomOnRobot:
            try:
                self.views()[0].focusOnRobot()
            except:
                pass

        # Apply physics
        self._physics.apply()

    def setGridSize(self, size_):
        """
        """
        self._gridSize = size_

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

        if self._showTracks:
            for robot in self._robots:
                painter.drawPath(robot.getTrack())
