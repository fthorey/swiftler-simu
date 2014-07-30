#!/usr/bin/python
# coding: utf-8

from utils.polygon import Polygon
from utils import const
from physics import Physics
from math import pi, degrees
from utils import helpers
import json

from PyQt4 import QtGui, QtCore

class World(QtGui.QGraphicsScene):
    """ World class provides access to all objects within the simulated environment.
    """

    def __init__(self, parent_):

        # Call parent constructor
        super(World, self).__init__(parent_)

        # Physics that rules the world
        self._physics = Physics(self)

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
        self._speedFactor = 2

    def toggleShowSupervisors(self, ):
        """Toggle the display of supervisors infos.
        """
        for robot in self._robots:
            robot.toggleShowSupervisors()

    def setCurrentSteps(self, steps_):
        """Set the current number of steps.
        """
        self._currentSteps = steps_

    def currentSteps(self, ):
        """Get the current number of steps.
        """
        return self._currentSteps

    def clear(self, ):
        """Clear the world
        """
        # Call parent clear
        super(World, self).clear()

        # Clear all robots and obstacles
        self._robots = list()
        self._obstacles = list()

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

    def robots(self, ):
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

    def parseColor(self, color):
        """
        Convert a color attribute value to int
        None will yield None, '#FFACDD' will yield 0xFFACDD
        """
        if color is None:
            return color
        if color[0] == "#":
            return int(color[1:],16)
        color = color.lower()
        if color == 'black':
            return 0x000000
        if color == 'red':
            return 0xFF0000
        if color == 'green':
            return 0x00FF00
        if color == 'blue':
            return 0x0000FF
        raise Exception('[world.parseColor] Bad color value in XML!')

    def readConfigurationFile(self, filename_):
        """Check the existence of the configuration file
        and create a specific XML reader to parse it. then call autoConstruct
        """
        # Autoconstruct the world
        self.autoConstruct(filename_)

        # Update the views on the robot
        for view in self.views():
                if self._zoomOnRobot:
                    view.focusOnRobot()
                else:
                    view.focusOnWorld()

    def autoConstruct(self, filename_):
        """ Autoconstructs the world from informations provided into the json
        template files.
        """
        # Start by erasing all current objects in the world
        self.clear()

        # Load the properties of the robot from file
        try:
            objects = json.loads(open(filename_, 'r').read())
        except ValueError:
            objects = {}

        masterRobotSet = False
        for key, value in objects["simulation"].items():
            if key == 'robot':
                robot_name = value['name']
                robot_type = value['type']
                try:
                    robot_color = self.parseColor(value['color'])
                except KeyError:
                    robot_color = self.parseColor(None)
                supervisor_type = value['supervisor']["type"]
                try:
                    # Get robot class
                    robot_class = helpers.load_by_name(str(robot_type), 'robots')
                    # Get robot supervisor class
                    sup_class = helpers.load_by_name(str(supervisor_type),'supervisors')
                    # Generate a robot name
                    brush = QtGui.QBrush(QtGui.QColor(str(robot_color)))
                    robot = robot_class(robot_name, sup_class, brush,
                                        './robots/resources/woggle-robot.json')
                    # Set the 1st robot encountered the master robot
                    if not masterRobotSet:
                        robot.setMasterRobot()
                        masterRobotSet = True
                    # Add the robot to the world
                    self.addItem(robot)
                    # Add the robot to the robots list
                    self._robots.append(robot)
                except:
                    print "[world.autoConstruct] Robot creation failed!"
                    raise
            elif key == 'obstacle':
                # Get obstacle parameters
                # Position are in m and rad
                for obstacle in value:
                    obstacle_pos = (float(obstacle['pose']['x']),
                                    float(obstacle['pose']['y']),
                                    float(obstacle['pose']['theta']))
                    points = []
                    for point in obstacle['geometry']['point']:
                        points.append((float(point['x']), float(point['y'])))
                    try:
                        obstacle_color = self.parseColor(obstacle['color'])
                    except KeyError:
                        obstacle_color = self.parseColor(None)
                    # Get obstacle attribute
                    brush = QtGui.QBrush(QtGui.QColor(obstacle_color))
                    obstacle = Polygon(obstacle_pos, points, brush)
                    # Add the obstacle to the world
                    self.addItem(obstacle)
                    # Add the obstacle to obstacles list
                    self._obstacles.append(obstacle)
            else:
                print "{world.autConstruct] Can't recognized the item!"
                raise

    def setPhysics(self, physics_):
        """Sets the physics that rules the world.
        """
        self._physics = physics_

    def physics(self, ):
        """Returns the current physics of the world.
        """
        return self._physics

    # Return a list of all obstacles in the wolrd
    def obstacles(self, ):
        """Return a list of all obstacles in the world.
        """
        return self._obstacles

    def update(self, ):
        """Update the world. Call the advance method a certain number
        of times according to the current value of the speed factor.
        """
        for step in range(int(self._speedFactor)):
            self._currentSteps = self._currentSteps + const.stepDuration
            self.advance()

    def advance(self, ):
        """Perform actions when the world advance.
        """

        # Call parent advance method
        # -> Call all items currently in the world advance method
        for robot in self.robots():
            robot.advance()

        # Apply physics (collisions detection)
        self._physics.apply()

        # Update the views on the robot if necessary
        if self._zoomOnRobot:
            for view in self.views():
                view.focusOnRobot()

    def drawBackground(self, painter, rect):
        """Draw the background.
        """
        # Draw robots tracks
        if self._showTracks:
            for robot in self._robots:
                painter.setPen(QtGui.QColor(robot.brush()))
                painter.drawPath(robot.tracker().getTrack())
