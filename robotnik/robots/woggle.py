#!/usr/bin/python
# coding: utf-8

from math import pi, degrees, radians, cos, sin
from robots.robot import Robot
from sensors.proximity import ProximitySensor
from sensors.wheelencoder import WheelEncoder
from supervisors.wogglesupervisor import WoggleSupervisor
from dynamics.differential import DifferentialDrive
from PyQt4 import QtGui, QtCore

class Woggle(Robot):
    """ The Woggle class handles a unicycle robot called Woggle
    """

    def __init__(self, name_, wheelRadius_, wheelBaseLength_, brush_, color_):
        # Call parent constructor
        super(Woggle, self).__init__(name_, brush_, color_)

        # Radius of the wheels (m)
        self._wheelRadius = wheelRadius_

        # Length between each wheel (m)
        self._wheelBaseLength = wheelBaseLength_

        # The Woggle robot follows the differential drive dynamic
        self.setDynamics(DifferentialDrive(self))

        # A supervisor is attached to the Woggle robot
        self.setSupervisor(WoggleSupervisor(self))

        # Current speed of the left wheel (rad/s)
        self._leftWheelSpeed = 0

        # Current speed of the right wheel (rad/s)
        self._rightWheelSpeed = 0

        # Current number of revolution of each wheel
        self._leftRevolutions = 0
        self._rightRevolutions = 0

        # Add a wheel encoder to each wheel
        self._leftWheelEncoder = WheelEncoder(2764.8, self._wheelRadius)

        # Add a wheel encoder to each wheel
        self._rightWheelEncoder = WheelEncoder(2764.8, self._wheelRadius)

        # Cache the envelope
        bl = self._wheelBaseLength/2
        self._envelope = [[bl * cos(pi/2 + pi/12), bl * sin(pi/2 + pi/12)],
                          [bl * cos(pi/2 - pi/12), bl * sin(pi/2 - pi/12)],
                          [bl * cos(pi/3), bl * sin(pi/3)],
                          [bl * cos(pi/4), bl * sin(pi/4)],
                          [bl * cos(pi/5), bl * sin(pi/5)],
                          [bl * cos(pi/12), bl * sin(pi/12)],
                          [bl * cos(-pi/12), bl * sin(-pi/12)],
                          [bl * cos(-pi/5), bl * sin(-pi/5)],
                          [bl * cos(-pi/4), bl * sin(-pi/4)],
                          [bl * cos(-pi/3), bl * sin(-pi/3)],
                          [bl * cos(-pi/2 + pi/12), bl * sin(-pi/2 + pi/12)],
                          [bl * cos(-pi/2 - pi/12), bl * sin(-pi/2 - pi/12)],
                          [bl * cos(pi + pi/3), bl * sin(pi + pi/3)],
                          [bl * cos(pi + pi/4), bl * sin(pi + pi/4)],
                          [bl * cos(pi + pi/5), bl * sin(pi + pi/5)],
                          [bl * cos(pi + pi/12), bl * sin(pi + pi/12)],
                          [bl * cos(pi - pi/12), bl * sin(pi - pi/12)],
                          [bl * cos(pi - pi/5), bl * sin(pi - pi/5)],
                          [bl * cos(pi - pi/4), bl * sin(pi - pi/4)],
                          [bl * cos(pi - pi/3), bl * sin(pi - pi/3)]]

        # Cache the bounding rect
        xmin, ymin, xmax, ymax = self.getBounds()
        self._boundingRect = QtCore.QRectF(QtCore.QPointF(xmin, ymin), QtCore.QPointF(xmax, ymax))

        # Cache the shape
        points = [QtCore.QPointF(p[0], p[1]) for p in self._envelope]
        self._shape = QtGui.QPainterPath()
        self._shape.addPolygon(QtGui.QPolygonF(points))

        # Position of the sharp sensors
        bl = self._wheelBaseLength/2 + 0.01
        self._proxSensorsPos = [
            [QtCore.QPointF(bl*cos(0), sin(0)), 0],
            [QtCore.QPointF(bl*cos(17*pi/120), bl*sin(17*pi/120)), 17*pi/120],
            [QtCore.QPointF(bl*cos(-17*pi/120), bl*sin(-17*pi/120)), -17*pi/120],
            [QtCore.QPointF(bl*cos(-9*pi/24), bl*sin(-9*pi/24)), -9*pi/24],
            [QtCore.QPointF(bl*cos(9*pi/24), bl*sin(9*pi/24)), 9*pi/24],
            [QtCore.QPointF(bl*cos(-pi/2-7*pi/24), bl*sin(-pi/2-7*pi/24)), -pi/2-7*pi/24],
            [QtCore.QPointF(bl*cos(pi/2+7*pi/24), bl*sin(pi/2+7*pi/24)), pi/2+7*pi/24],
            [QtCore.QPointF(bl*cos(pi), bl*sin(pi)), pi]]

        # Add the sensors to the robot
        for pos in self._proxSensorsPos:
            sensor = ProximitySensor(pos)
            # Add the sensor to the list of sensors
            self.proxSensors().append(sensor)
            # Add the sensor to the general list of items of the robot
            self.addItem(sensor)

    def restart(self, ):
        """Restart.
        """
        # Call robot restart
        super(Woggle, self).restart()

        # Set wheel speeds to 0
        self._leftWheelSpeed = 0
        self._rightWheelSpeed = 0

        # Set current number of revolutions to 0
        self._leftRevolutions = 0
        self._rightRevolutions = 0

    def leftRevolutions(self, ):
        """Return the number of revolutions of the left wheel.
        """
        return self._leftRevolutions

    def rightRevolutions(self, ):
        """Return the number of revolutions of the right wheel.
        """
        return self._rightRevolutions

    def setLeftRevolutions(self, rev_):
        """Set the number of revolutions of the left wheel.
        """
        self._leftRevolutions = rev_

    def setRightRevolutions(self, rev_):
        """Set the number of revolutions of the right wheel.
        """
        self._rightRevolutions = rev_

    def leftWheelEncoder(self, ):
        """Return the left wheel encoder.
        """
        return self._leftWheelEncoder

    def rightWheelEncoder(self, ):
        """Return the right wheel encoder.
        """
        return self._rightWheelEncoder

    def wheelRadius(self, ):
        """Return the wheel radius (in m).
        """
        return self._wheelRadius

    def wheelBaseLength(self, ):
        """Return the wheel base length (in m).
        """
        return self._wheelBaseLength

    def setLeftWheelSpeed(self, speed_):
        """Set the current left wheel speed (in m/s).
        """
        self._leftWheelSpeed = speed_

    def setRightWheelSpeed(self, speed_):
        """Set the current right wheel speed (in m/s).
        """
        self._rightWheelSpeed = speed_

    def getLeftWheelSpeed(self, ):
        """Return the current left wheel speed (in m/s).
        """
        return self._leftWheelSpeed

    def getRightWheelSpeed(self, ):
        """Return the current right wheel speed (in m/s).
        """
        return self._rightWheelSpeed

    def setWheelSpeeds(self, vel_l, vel_r):
        """Set the speed of both wheels (in m/s).
        """
        self._leftWheelSpeed = vel_l
        self._rightWheelSpeed = vel_r

    def getSpeed(self, ):
        """Get current speed (in m/s).
        """
        v, w = self.dynamics.diff2Uni(self._leftWheelSpeed, self._rightWheelSpeed)
        return v

    def getEnvelope(self, ):
        """Return the envelope of the robot.
        """
        return self._envelope

    def boundingRect(self, ):
        """Return the bounding rect of the robot.
        """
        return self._boundingRect

    def shape(self, ):
        """Return the shape of the robot.
        """
        return self._shape

    def paint(self, painter, option, widget):
        """Paint the robot on screen
        """
        # Paint body (always grey)
        painter.setBrush(QtGui.QColor("light grey"))
        painter.setPen(QtCore.Qt.SolidLine)
        points = [QtCore.QPointF(p[0], p[1]) for p in self._envelope]
        painter.drawPolygon(QtGui.QPolygonF(points))

        bodyX = (-self._wheelBaseLength/2)
        bodyY = (-self._wheelBaseLength/2)
        bodyW = self._wheelBaseLength
        bodyH = self._wheelBaseLength

        # Paint identifier
        painter.setBrush(self.brush())
        painter.setPen(self.pen())
        rect = QtCore.QRectF(-bodyW/8, -bodyH/8, bodyW/4, bodyH/4)
        painter.drawEllipse(rect)

        # Paint left wheel
        wheelW = bodyW / 3
        wheelH = bodyH / 6
        lwheelX = -wheelW/2
        lwheelY = -bodyH/2 + wheelH/2
        rect = QtCore.QRectF(lwheelX, lwheelY, wheelW, wheelH)
        painter.setBrush(QtGui.QColor("black"))
        painter.drawRect(rect)

        # Paint right wheel
        rwheelX = -wheelW/2
        rwheelY = bodyH/2 - wheelH - wheelH/2
        rect = QtCore.QRectF(rwheelX, rwheelY, wheelW, wheelH)
        painter.drawRect(rect)
