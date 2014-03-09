#!/usr/bin/python
# coding: utf-8

from utils.struct import Struct
from math import degrees, sqrt, cos, sin, pi, log1p, tan
from robots.robot import Robot
from controllers.gotogoal import GoToGoal
from controllers.avoidobstacle import AvoidObstacle
from controllers.followwall import FollowWall
from controllers.hold import Hold
from supervisors.supervisor import Supervisor
import numpy as np

from PyQt4 import QtCore, QtGui

class WoggleSupervisor(Supervisor):
    """ WoggleSupervisor is a class that provides a way to control a Woggle robot.

    The WoggleSupervisor does not move the robot directly. Instead, the supervisor
    selects a controller to do the work and uses the controller outputs
    to generate the robot inputs.
    """

    def __init__(self, pos_, robotInfo_):
        # Call parent constructor
        super(WoggleSupervisor, self,).__init__(pos_, robotInfo_);

        # Set some extra informations
        # PID parameters
        self.info().gains = Struct()
        self.info().gains.Kp = 1.0
        self.info().gains.Ki = 0.2
        self.info().gains.Kd = 0.01
        # Goal
        self.info().goal = Struct()
        self.info().goal.x = -1
        self.info().goal.y = 1
        # Wheels
        self.info().wheels = Struct()
        self.info().wheels.radius = robotInfo_.wheels.radius
        self.info().wheels.baseLength = robotInfo_.wheels.baseLength
        self.info().wheels.leftTicks = robotInfo_.wheels.leftTicks
        self.info().wheels.rightTicks = robotInfo_.wheels.rightTicks
        # Sensors
        self.info().sensors = Struct()
        self.info().sensors.insts = robotInfo_.sensors.insts
        self.info().sensors.dist = self.getIRDistance(robotInfo_)
        self.info().sensors.rmin = robotInfo_.sensors.rmin
        self.info().sensors.rmax = robotInfo_.sensors.rmax

        # Create:
        # - a go-to-goal controller
        # - an avoid-obstacle controller
        # - a follow-wall controller
        # - a hold controller
        self._controllers = {'gtg': GoToGoal(self.info()),
                             'avd': AvoidObstacle(self.info()),
                             'fow': FollowWall(self.info()),
                             'hld' : Hold(self.info())}

        # Set current controller
        self._currController = self._controllers['gtg']

    def controller(self, ):
        """Return the current controller of the robot.
        """
        return self._currController

    def setController(self, controller_):
        """Set the controller of the robot.
        """
        self._currController = controller_

    def atGoal(self):
        """Check if the distance to goal is small.
        """
        return self._toGoal < self.info().wheels.baseLength/2

    def atObst(self):
        """Check if the distance to obstacle is small.
        """
        return self._toObst < self.info().sensors.rmax/2

    def execute(self, robotInfo_, dt_):
        """Selects and executes a controller.
        """
        # 1 -> Update the estimation of the robot state
        self.updateStateEstimate(robotInfo_)

        if self.atObst():
            self._currController = self._controllers['avd']
        elif self.atGoal():
            self._currController = self._controllers['hld']
        else:
            self._currController = self._controllers['gtg']

        # 2 -> Execute the controller to obtain unicycle command (v, w) to apply
        v, w = self._currController.execute(self.info(), dt_)

        return v, w

    def getIRDistance(self, robotInfo_):
        """Converts the IR distance readings into a distance in meters.
        """
        # Get the current parameters of the sensor
        readings = robotInfo_.sensors.readings
        rmin = robotInfo_.sensors.rmin
        rmax = robotInfo_.sensors.rmax

        # Conver the readings to a distance (in m)
        dists = [max( min( (log1p(3960) - log1p(r))/30 + rmin, rmax), rmin) for r in readings]
        return dists

    def updateStateEstimate(self, robotInfo_):
        """Update the current estimation of the robot state.
        """
        # Get the number of ticks on each wheel since last call
        dtl = robotInfo_.wheels.leftTicks - self.info().wheels.leftTicks
        dtr = robotInfo_.wheels.rightTicks - self.info().wheels.rightTicks

        # Save the wheel encoder ticks for the next estimate
        self.info().wheels.leftTicks += dtl
        self.info().wheels.rightTicks += dtr

        # Get old state estimation (in m and rad)
        x, y, theta = self.info().pos

        # Get robot parameters (in m)
        R = robotInfo_.wheels.radius
        L = robotInfo_.wheels.baseLength
        m_per_tick = (2*pi*R) / robotInfo_.wheels.ticksPerRev

        # distance travelled by left wheel
        dl = dtl*m_per_tick
        # distance travelled by right wheel
        dr = dtr*m_per_tick

        theta_dt = -(dr-dl)/L
        theta_mid = theta + theta_dt/2
        dst = (dr+dl)/2
        x_dt = dst*cos(theta_mid)
        y_dt = dst*sin(theta_mid)

        theta_new = theta + theta_dt
        x_new = x + x_dt
        y_new = y + y_dt

        # Update the state estimation
        self.info().pos = (x_new, y_new, theta_new)

        # Update the sensors readings
        self.info().sensors.dist = self.getIRDistance(robotInfo_)

        # Distance to the goal
        self._toGoal = sqrt((x_new - self.info().goal.x)**2 +
                            (y_new - self.info().goal.y)**2)

        # Distance to the closest obstacle
        self._toObst = min(self.info().sensors.dist)

    def drawHeading(self, painter, option=None, widget=None):
        """Draw the heading direction.
        """
        def drawArrow(painter, color, x1, y1, x2, y2, angle=0.5, ratio=0.02):
            """Draw an arrow.
            """
            line = QtCore.QLineF(x1, y1, x2, y2)
            xe = arrow_l - ratio
            ye = tan(angle) * ratio
            line1 = QtCore.QLineF(x2, y2, xe, ye)
            line2 = QtCore.QLineF(x2, y2, xe, -ye)
            painter.setPen(QtCore.Qt.SolidLine)
            painter.setPen(QtGui.QColor(color))
            painter.drawLine(line)
            painter.drawLine(line1)
            painter.drawLine(line2)

        # Go to Goal heading angle
        gtg_angle = self._controllers['gtg'].getHeadingAngle(self.info())
        avd_angle = self._controllers['avd'].getHeadingAngle(self.info())
        arrow_l = self.info().wheels.baseLength * 2

        # Robot direction
        drawArrow(painter, "green", 0, 0, arrow_l, 0)

        # GoToGoal direction
        painter.rotate(degrees(gtg_angle))
        drawArrow(painter, "blue", 0, 0, arrow_l, 0)
        painter.rotate(-degrees(gtg_angle))

        # AvoidObstacle direction
        painter.rotate(degrees(avd_angle))
        drawArrow(painter, "red", 0, 0, arrow_l, 0)
        painter.rotate(-degrees(avd_angle))
