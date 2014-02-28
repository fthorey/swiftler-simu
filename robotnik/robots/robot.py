#!/usr/bin/python
# coding: utf-8

from utils.simobject import SimObject
from PyQt4 import QtGui, QtCore
from utils import const
from utils.tracker import Tracker

class Robot(SimObject):
    """ The Robot class represents a generic class for robots.
    """

    def __init__(self, name_, brush_, color_):

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

        # Current zoom level
        self._zoom = 1.0

        # Store all items which belong to the robot
        self._items = [self, ]

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

    def setGoal(self, goal_):
        """Set a heading goal to the robot.
        """
        self._supervisor.setGoal(goal_)

    def getGoal(self, ):
        """Get the heading goal of the robot.
        """
        return self._supervisor.getGoal()

    def restart(self, ):
        """Restart from the robot to its initial state.
        """
        # Set the initial postion (in m)
        self.setPos(self._initPos)
        # Set the initial heading angle (in rad)
        self.setAngle(self._initAngle)
        # Set the initial state estimate of the supervisor
        self._supervisor.setStateEstimate(self._initPos.x(),
                                          self._initPos.y(),
                                          self._initAngle)

        # The robot is not stopped anymore
        self._stopped = False

        # Actions below must be performed after the position
        # of the robot has been restarted

        # Restart all sensors
        for sensor in self._proxSensors:
            sensor.restart()

        # Restar the supervisor
        self._supervisor.restart()

        # Restart the tracker
        self._tracker.restart(self._initPos)

    def setInitialPos(self, pos_, angle_):
        """Set the initial position of the robot (in m & rad).
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

    def getInitialPos(self, ):
        """Get the initial position of the robot (in m & rad).
        """
        return self._initPos, self._initAngle

    def setDynamics(self, dynamics_):
        """Set the dynamics followed by the robot.
        """
        self._dynamics = dynamics_

    def getDynamics(self, ):
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
        # Called twice by QGraphicsScene::advance() First, with step_ == 0: about to advance,
        # and then called with phase == 1, advance effectively
        # -> Do nothing on the 1st phase but move on 2nd phase
        if (step_ == 0):
            return

        # 1 -> Execute the supervisor to obtain new command to apply to the robot
        # according to the new state
        self._supervisor.execute(const.stepDuration)

        # 2 -> Update the robot position using dynamic and current command
        self._dynamics.update(const.stepDuration)

        # 3 -> Add the position to the tracker
        self.tracker().addPosition(self.pos())
