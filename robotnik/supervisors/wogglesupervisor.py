#!/usr/bin/python
# coding: utf-8

from utils.struct import Struct
from math import degrees, sqrt, cos, sin, pi, log1p, tan, atan2
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
        self.info().gains.Kp = 3.0
        self.info().gains.Ki = 0.7
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
        self.info().sensors.toCenter = robotInfo_.sensors.toCenter

        # Follow wall important information
        self.info().direction = 'left'

        # Distance from center of robot to extremity of a sensor beam
        self._distMax = self.info().sensors.toCenter + robotInfo_.sensors.rmax

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

    def isAtWall(self):
        """Check if the distance to obstacle is small.
        """
        # Detect a wall when it is at 80% of the distance
        # from the center of the robot
        return self._toWall < ((self.info().sensors.toCenter + self.info().sensors.rmax) * 0.8)
        return self._toWall < (self._distMax * 0.8)

    def atWall(self, ):
        """Check if the distance to wall is small and decide a direction.
        """
        wall_close = self.isAtWall()

        # Find the closest detected point
        if wall_close:
            dmin = self.info().sensors.toCenter + self.info().sensors.rmax
            dmin = self._distMax
            angle = 0
            for i, d in enumerate(self.info().sensors.dist):
                if d < dmin:
                    dmin = d
                    angle = self.info().sensors.insts[i].angle()

            # Go that way
            if angle > 0:
                self.info().direction = 'left'
            else:
                self.info().direction = 'right'

        return wall_close

    def execute(self, robotInfo_, dt_):
        """Selects and executes a controller.
        """
        # 1 -> Update the estimation of the robot state
        self.updateStateEstimate(robotInfo_)

        if self.atWall():
            self._currController = self._controllers['fow']
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
        self._toWall = self.info().sensors.toCenter + min(self.info().sensors.dist)

    def drawHeading(self, painter, option=None, widget=None):
        """Draw the heading direction.
        """
        def drawArrow(painter, color, x1, y1, x2, y2, angle=0.5, ratio=0.1):
            """Draw an arrow.
            """
            # Save state
            painter.save()

            # Rotate and scale
            painter.rotate(degrees(atan2(y2-y1,x2-x1)))
            factor = sqrt((x1-x2)**2 + (y1-y2)**2)
            painter.scale(factor, factor)

            # Draw the arrow
            line = QtCore.QLineF(0, 0, 1, 0)
            xe = 1 - ratio
            ye = tan(angle) * ratio
            line1 = QtCore.QLineF(1, 0, xe, ye)
            line2 = QtCore.QLineF(1, 0, xe, -ye)
            painter.setPen(QtCore.Qt.SolidLine)
            painter.setPen(QtGui.QColor(color))
            painter.drawLine(line)
            painter.drawLine(line1)
            painter.drawLine(line2)

            # Restore state
            painter.restore()

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

        # FollowWall direction
        along_wall = self._controllers['fow']._along_wall_vector
        to_wall = self._controllers['fow']._to_wall_vector

        if to_wall is not None:
            to_angle = degrees(atan2(to_wall[1], to_wall[0]))
            drawArrow(painter, "green", 0, 0, to_wall[0], to_wall[1])

        if along_wall is not None:
            along_angle = degrees(atan2(along_wall[1], along_wall[0]))
            painter.translate(to_wall[0], to_wall[1])
            drawArrow(painter, "purple", 0, 0, along_wall[0], along_wall[1])
