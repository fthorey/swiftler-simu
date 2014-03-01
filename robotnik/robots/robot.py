#!/usr/bin/python
# coding: utf-8

from utils.simobject import SimObject
from PyQt4 import QtGui, QtCore
from utils import const
from utils.tracker import Tracker

class Robot(SimObject):
    """ The Robot class represents a generic class for robots.
    """

    def __init__(self, name_, pos_, brush_):

        # Call parent constructor
        super(Robot, self).__init__(name_, pos_, brush_)

        # Is the robot stopped
        self._stopped = False

        # Is the robot master
        self._isMaster = False

        # Current zoom level
        self._zoom = 1.0

        # Store all items which belong to the robot
        self._items = [self, ]

        # Associate a tracker to store the path (in m)
        # Tracker only manipulates (x,y)
        self._tracker = Tracker(pos_[:2])

    def info(self):
        """Return the robot information structure.
        """
        raise NotImplementedError("Robot.info")

    def tracker(self, ):
        """Return the tracker of the robot.
        """
        return self._tracker

    def addItem(self, item):
        """Add an item to the robot's item list.
        """
        self._items.append(item)
        item.setParentItem(self)

    def getAllItems(self, ):
        """Return the robot's item list.
        """
        return self._items

    def showProxSensors(self, show_):
        """Select to show or not the proximity sensors.
        """
        for sensor in self._proxSensors:
            sensor.show(show_)

    def proxSensors(self, ):
        """Return the list of proximity sensors of the robot.
        """
        return self._proxSensors

    def addProxSensor(self, sensor):
        """Add a sensors to the prox sensors list.
        """
        try:
            self._proxSensors.append(sensor)
        except AttributeError:
            self._proxSensors = list()
            self._proxSensors.append(sensor)

        # Add to list of all items
        self.addItem(sensor)

    def setZoom(self, zoom_):
        """Set the current zoom level of the robot.
        """
        self._zoom = zoom_

    def isMasterRobot(self, ):
        """Check if the robot is currently the master.
        """
        return self._isMaster

    def setMasterRobot(self, ):
        """Set this robot the master robot.
        """
        self._isMaster = True

    def setDynamics(self, dynamics_):
        """Set the dynamics followed by the robot.
        """
        self._dynamics = dynamics_

    def dynamics(self, ):
        """Get the dynamic of the robot.
        """
        return self._dynamics

    def setSupervisor(self, supervisor_):
        """Set the supervisor that run the robot.
        """
        self._supervisor = supervisor_

    def supervisor(self, ):
        """Get the supervisor of the robot.
        """
        return self._supervisor

    def stop(self, ):
        """Stop the robot.
        """
        self._stopped = True

    def isStopped(self, ):
        """Check if the robot is stopped.
        """
        return self._stopped

    def enlargedBoundingRect(self):
        """Return the bounding rect of the robot and all its sensors
        by a zoom factor.
        The zoom factor must be between 0% and 100%.
        """
        zoom = 1.0 / self._zoom
        rect = self.boundingRect() | self.childrenBoundingRect()
        dx1 = -rect.width() * zoom
        dy1 = -rect.height() * zoom
        dx2 = -dx1
        dy2 = -dy1
        rect.adjust(dx1, dy1, dx2, dy2)
        return rect

    def advance(self, step_):
        """Action to perform when the scene changes.
        """
        # -> Do nothing on the 1st phase but move on 2nd phase
        if (step_ == 0):
            return

        # 1 -> Execute the supervisor to obtain unicycle command (v,w) to apply
        v, w = self._supervisor.execute(self.info(), const.stepDuration)
        vel_l, vel_r = self.dynamics().uni2Diff(v, w)

        # 2 -> Apply current speed to wheels
        self.setWheelSpeeds(vel_l, vel_r)

        # 3 -> Update the robot position using dynamic and current command
        self._dynamics.update(const.stepDuration)

        # 4 -> Add the new position to the tracker
        self.tracker().addPosition((self.pos().x(), self.pos().y()))
