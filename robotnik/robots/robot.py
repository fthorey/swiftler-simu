#!/usr/bin/python
# coding: utf-8

from utils.simobject import SimObject
from PyQt4 import QtGui, QtCore
from utils import const
from utils.tracker import Tracker

class Robot(SimObject):
    """ Robot class handles a robot
    """

    # Constructor
    def __init__(self, name_, brush_, color_):
        """
        """
        # Call parent constructor
        super(Robot, self).__init__(name_, brush_, color_)

        # Dynamics followed by the robot
        self._dynamics = None

        # Supervisor to run the robot
        from supervisors.supervisor import Supervisor
        self._supervisor = Supervisor(self)

        # Is the robot stopped
        self._stopped = False

        # Initial position (in m)
        self._initPos = QtCore.QPointF(0, 0)

        # Initial heading angle (in rad)
        self._initAngle = 0

        # List of all proximity sensors of the robot
        self._proxSensors = list()

        # Is the robot master
        self._isMaster = False

        # Keep the current zoom
        self._zoom = 1

        # Store track item into the current view
        self._trackItem = None

        # Store all items which belong to the robot
        self._items = [self, ]

    def tracker(self, ):
        """
        """
        return self._tracker

    def addItem(self, item):
        """
        """
        self._items.append(item)

    def getAllItems(self, ):
        """
        """
        return self._items

    def getTrack(self, ):
        """
        """
        return self._tracker.getTrack()

    def showProxSensors(self, show_):
        for sensor in self._proxSensors:
            sensor.show(show_)

    def proxSensors(self, ):
        """
        """
        return self._proxSensors

    def setZoom(self, zoom_):
        """
        """
        self._zoom = zoom_

    # Check if the robot is currently the master
    def isMasterRobot(self, ):
        """
        """
        return self._isMaster

    # Set master
    def setMasterRobot(self, ):
        """
        """
        self._isMaster = True

    # Set a goal
    def setGoal(self, goal_):
        """
        """
        self._supervisor.setGoal(goal_)

    # Get a goal
    def getGoal(self, ):
        """
        """
        return self._supervisor.getGoal()

    # Restart from the robot to its initial state
    def restart(self, ):
        """
        """
        # Set the initial postion (in m)
        self.setPos(self._initPos)
        # Set the initial heading angle (in rad)
        self.setAngle(self._initAngle)
        self._stopped = False
        # Restart all sensors
        for sensor in self._proxSensors:
            sensor.restart()

        # Restart the tracker
        self._tracker.restart(self._initPos)

    # Set the initial position of the robot (in m & rad)
    def setInitialPos(self, pos_, angle_):
        """
        """
        # in m
        self._initPos = pos_
        # in rad
        self._initAngle = angle_

        # setPos and setAngle are in charge of converting m to pixel
        self.setPos(pos_)
        self.setAngle(angle_)

        # Associate a tracker to store the path (in m)
        self._tracker = Tracker(pos_)

        # Set the initial state estimate of the supervisor
        self._supervisor.setStateEstimate(self._initPos.x(),
                                          self._initPos.y(),
                                          self._initAngle)

    # Get the initial position of the robot (in m & rad)
    def getInitialPos(self, ):
        """
        """
        return self._initPos, self._initAngle

    # Set the dynamics followed by the robot
    def setDynamics(self, dynamics_):
        """
        """
        self._dynamics = dynamics_

    # Get the dynamic of the robot
    def getDynamics(self, ):
        """
        """
        return self._dynamics

    # Set the supervisor that run the robot
    def setSupervisor(self, supervisor_):
        """
        """
        self._supervisor = supervisor_

    # Get the supervisor of the robot
    def getSupervisor(self, ):
        """
        """
        return self._supervisor

    # Stop the robot
    def stop(self, ):
        """
        """
        self._stopped = True

    # Check if the robot is stopped
    def isStopped(self, ):
        """
        """
        return self._stopped

    # Return the bounding rect of the robot and all its sensors by a zoom factor
    # The zoom factor must be between 0% and 100%
    def enlargedBoundingRect(self):
        """
        """
        zoom = 1.0 / self._zoom
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

        # Update the robot position using dynamic and current command
        self._dynamics.update(const.stepDuration)

        # Execute the supervisor
        self._supervisor.execute()
