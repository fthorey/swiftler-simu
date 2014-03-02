#!/usr/bin/python
# coding: utf-8

from utils.polygon import Polygon
from utils import const
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

    def readConfigurationFile(self, filename_):
        """Check the existence of the configuration file
        and create a specific XML reader to parse it. then call autoConstruct
        """
        try:
            self._xmlReader = XMLReader(filename_)
        except Exception, e:
            raise Exception('[World.checkConfigurationFile] Failed to parse ' + filename \
                + ': ' + str(e))
        else:
            self.autoConstruct()

        # Update the views on the robot
        for view in self.views():
                if self._zoomOnRobot:
                    view.focusOnRobot()
                else:
                    view.focusOnWorld()

    def autoConstruct(self, ):
        """ Autoconstructs the world from informations provided into the xml
        template files.
        """
        # Start by erasing all current objects in the world
        self.clear()

        # Get all objects from xml
        objects = self._xmlReader.parseConfiguration()

        # To check if a master robot has been defined
        masterRobotSet = False
        for objs in objects:
            objsType = objs[0]
            if objsType is 'robot':
                # Get robot parameters
                robot_type, supervisor_type, robot_pos, robot_color = objs[1:5]
                try:
                    # Get robot class
                    robot_class = helpers.load_by_name(robot_type,'robots')
                    # Get robot supervisor class
                    sup_class = helpers.load_by_name(supervisor_type,'supervisors')
                    # Generate a robot name
                    name = "{}{}".format(robot_class.__name__,
                                              len(self._robots))
                    brush = QtGui.QBrush(QtGui.QColor(robot_color))
                    robot = robot_class(name, sup_class, robot_pos, brush)
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
            elif objsType is 'obstacle':
                # Get obstacle parameters
                # Position are in m and rad
                obstacle_pos, obstacle_coords, obstacle_color = objs[1:4]
                # Set a default color
                if obstacle_color is None:
                    obstacle_color = 0xFF0000
                # Get obstacle attribute
                brush = QtGui.QBrush(QtGui.QColor(obstacle_color))
                obstacle = Polygon(obstacle_pos, obstacle_coords, brush)
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
        super(World, self).advance()

        # Apply physics
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
