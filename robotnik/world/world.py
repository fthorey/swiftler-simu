#!/usr/bin/python
# coding: utf-8

from utils.polygon import Polygon
from PyQt4 import QtGui, QtCore
from physics import Physics
from math import pi, degrees
from utils.xmlreader import XMLReader
from utils import helpers

class World(QtGui.QGraphicsScene):
    """ World class provides access to all objects within the simulated environment.
    """

    def __init__(self, parent_):

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
        self._zoomOnRobot = True

        # Store if the robots sensors are displayed
        self._showRobotSensors = True

        # Store if path drawing is needed
        self._showTracks = True

        # Stores if the ghost mode is activated or not
        self._isGhostMode = True

        # Stores the running state of the world
        self._isRunning = False

        # World speed factor
        self._speedFactor = 1

    def setSpeedFactor(self, factor_):
        """Set the world speed factor.
        """
        self._speedFactor = factor_

    def setRunning(self, isRunning_):
        """Set the running state of the world.
        """
        self._isRunning = isRunning_

    def toggleRunning(self, ):
        """Toggles the running state of the world.
        """
        self._isRunning = not self._isRunning

    def isRunning(self, ):
        """Checks if the world is running or not.
        """
        return self._isRunning

    def getRobots(self, ):
        """Get a list of all robots currently in the world.
        """
        return self._robots

    def isGhostModeActivated(self, ):
        """Checks if the ghost mode is activated.
        """
        return self._isGhostMode

    def toggleGhostMode(self, ):
        """Toggle the ghost mode.
        """
        self._isGhostMode = not self._isGhostMode

    def toggleRobotTracks(self, ):
        """Toggle the robot tracks display.
        """
        self._showTracks = not self._showTracks

    def toggleRobotSensors(self, ):
        """Toggles the robots sensors display.
        """
        self._showRobotSensors = not self._showRobotSensors

        for robot in self._robots:
            robot.showProxSensors(self._showRobotSensors)

    def setZoomOnRobot(self, zoom_):
        """Toggles the current state of the zoom.
        """
        self._zoomOnRobot = zoom_

    def isZoomOnRobot(self, ):
        """Checks if the zoom is currently on the master robot.
        """
        return self._zoomOnRobot

    # Construct the world
    def autoConstruct(self, ):
        """ Autoconstructs the world from informations provided into the xml
        template files.
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

    def addRobot(self, robot_, position_, angle_):
        """Adds a robot to the world
        The position is given in m.
        """
        robot_.setInitialPos(position_, angle_)
        self.addItem(robot_)
        self._robots.append(robot_)

    def setPhysics(self, physics_):
        """Sets the physics that rules the world.
        """
        self._physics = physics_

    def getPhysics(self, ):
        """Returns the current physics of the world.
        """
        return self._physics

    # Return a list of all obstacles in the wolrd
    def getObstacles(self, ):
        """Return a list of all obstacles in the world.
        """
        return self._obstacles

    def update(self, ):
        """Update the world. Call the advance method a certain number
        of times according to the current value of the speed factor.
        """
        for step in range(int(self._speedFactor)):
            self.advance()

    def advance(self, ):
        """Perform actions when the world advance.
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
        """Sets the grid size.
        """
        self._gridSize = size_

    def drawBackground(self, painter, rect):
        """Draw the background.
        """
        painter.setPen(self._gridPen)
        painter.setWorldMatrixEnabled(True);

        # Draw robots tracks
        if self._showTracks:
            for robot in self._robots:
                painter.setPen(QtGui.QColor(robot.brush()))
                painter.drawPath(robot.tracker().getTrack())
