#!/usr/bin/python
# coding: utf-8

from shape.shape import Shape
from PyQt4 import QtGui, QtCore
from utils import const
from utils.tracker import Tracker

class Robot(Shape):
    """ Robot class handles a robot
    """

    # Constructor
    def __init__(self, name_):
        """
        """
        # Call parent constructor
        super(Robot, self).__init__(name_)

        # Dynamics followed by the robot
        self.dynamics = None

        # Supervisor to run the robot
        self.supervisor = None

        # Is the robot stopped
        self.stopped = False

        # Initial position (in m)
        self.initPos = QtCore.QPointF(0, 0)

        # Initial heading angle (in rad)
        self.initTheta = 0

        # List of all proximity sensors of the robot
        self.proxSensors = list()

        # Is the robot master
        self.isMaster = False

        # Keep the current zoom
        self.zoom = 1

        # Store track item into the current view
        self.trackItem = None

        # Store all items which belong to the robot
        self.items = [self, ]

    def addItem(self, item):
        """
        """
        self.items.append(item)

    def getAllItems(self, ):
        """
        """
        return self.items

    def getTrack(self, ):
        """
        """
        return self.tracker.getTrack()

    def setTrackItem(self, trackItem_):
        """
        """
        self.trackItem = trackItem_

        # Add the track item to the robot list of items
        self.items.append(trackItem_)

    def getTrackItem(self, ):
        """
        """
        return self.trackItem

    def removeTrackItem(self, ):
        """
        """
        # Remove the track item from the robot list of items
        self.items.remove(self.trackItem)
        self.trackItem = None

    def showProxSensors(self, show_):
        for sensor in self.proxSensors:
            sensor.show(show_)

    def getProxSensors(self, ):
        """
        """
        return self.proxSensors

    def setZoom(self, zoom_):
        """
        """
        self.zoom = zoom_

    # Check if the robot is currently the master
    def isMasterRobot(self, ):
        """
        """
        return self.isMaster

    # Set master
    def setMasterRobot(self, ):
        """
        """
        self.isMaster = True

    # Set a goal
    def setGoal(self, goal_):
        """
        """
        self.supervisor.setGoal(goal_)

    # Get a goal
    def getGoal(self, ):
        """
        """
        return self.supervisor.getGoal()

    # Restart from the robot to its initial state
    def restart(self, ):
        """
        """
        # Set the initial postion (in m)
        self.setPos(self.initPos)
        # Set the initial heading angle (in rad)
        self.setTheta(self.initTheta)
        self.stopped = False
        # Restart all sensors
        for sensor in self.proxSensors:
            sensor.restart()

        # Restart the tracker
        self.tracker.restart(self.initPos)

    # Set the initial position of the robot (in m & rad)
    def setInitialPos(self, pos_, theta_):
        """
        """
        # in m
        self.initPos = pos_
        # in rad
        self.initTheta = theta_

        # setPos and setTheta are in charge of converting m to pixel
        self.setPos(pos_)
        self.setTheta(theta_)

        # Associate a tracker to store the path (in m)
        self.tracker = Tracker(pos_)

    # Get the initial position of the robot (in m & rad)
    def getInitialPos(self, ):
        """
        """
        return self.initPos, self.initTheta

    # Set the dynamics followed by the robot
    def setDynamics(self, dynamics_):
        """
        """
        self.dynamics = dynamics_

    # Get the dynamic of the robot
    def getDynamics(self, ):
        """
        """
        return self.dynamics

    # Set the supervisor that run the robot
    def setSupervisor(self, supervisor_):
        """
        """
        self.supervisor = supervisor_

    # Get the supervisor of the robot
    def getSupervisor(self, ):
        """
        """
        return self.supervisor

    # Stop the robot
    def stop(self, ):
        """
        """
        self.stopped = True

    # Check if the robot is stopped
    def isStopped(self, ):
        """
        """
        return self.stopped

    # Return the bounding rect of the robot and all its sensors by a zoom factor
    # The zoom factor must be between 0% and 100%
    def enlargedBoundingRect(self):
        """
        """
        zoom = 1.0 / self.zoom
        rect = self.boundingRect() | self.childrenBoundingRect()
        dx1 = -rect.width() * zoom
        dy1 = -rect.height() * zoom
        dx2 = -dx1
        dy2 = -dy1
        rect.adjust(dx1, dy1, dx2, dy2)
        return rect

    # Action to perform when the scene changes
    def advance(self, step_):
        """
        """
        # Called twice by QGraphicsScene::advance() First, with step_ == 0: about to advance,
        # and then called with phase == 1, advance effectively
        # -> Do nothing on the 1st phase but move on 2nd phase
        if (step_ == 0):
            return

        # Execute the supervisor
        self.supervisor.execute()

        # Update the robot dynamics
        # Get pos (in m), get theta (in rad)
        pos, theta = self.dynamics.update()

        # Add the position to the tracker
        self.tracker.addPosition(pos)

        # Set the new robot position (in pixel)
        self.setPos(pos)
        # Set the new robot theta angle (in rad)
        self.setTheta(theta)
