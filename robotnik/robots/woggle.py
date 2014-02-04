#!/usr/bin/python
# coding: utf-8

from math import pi, degrees, radians, cos, sin
from utils import const
from robots.robot import Robot
from sensors.proximity import ProximitySensor
from supervisors.wogglesupervisor import WoggleSupervisor
from dynamics.differential import DifferentialDrive
from PyQt4 import QtGui, QtCore

class Woggle(Robot):
    """ Woggle class handles a Woggle robot
    """

    # Constructor
    # Get wheel radius (in m)
    # Get in-between wheels distance (in m)
    def __init__(self, name_, wheelRadius_, wheelBaseLength_):
        """
        """
        # Call parent constructor
        super(Woggle, self).__init__(name_)

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

        # Set default heading angle (in rad)
        self.setTheta(0)

        # Store position for sharps
        self._sharpPos = dict()

        # Add some distance to avoid extra collision detection
        baseLength = self._wheelBaseLength + 0.02
        self._sharpPos['sharp0'] = {'pos': QtCore.QPointF(baseLength/2, 0),
                                   'angle': 0}

        self._sharpPos['sharp1'] = {'pos': QtCore.QPointF(baseLength/2 * cos(pi/3),
                                                             -baseLength/2 * sin(pi/3)),
                                   'angle': -pi/3}

        self._sharpPos['sharp2'] = {'pos': QtCore.QPointF(baseLength/2 * cos(pi/3),
                                                             baseLength/2 * sin(pi/3)),
                                   'angle': +pi/3}

        self._sharpPos['sharp3'] = {'pos': QtCore.QPointF(baseLength/2 * cos(pi/5),
                                                             -baseLength/2 * sin(pi/5)),
                                   'angle': -pi/5}

        self._sharpPos['sharp4'] = {'pos': QtCore.QPointF(baseLength/2 * cos(pi/5),
                                                             baseLength/2 * sin(pi/5)),
                                   'angle': +pi/5}

        self._sharpPos['sharp5'] = {'pos': QtCore.QPointF(baseLength/2 * cos(2*pi/3),
                                                             -baseLength/2 * sin(2*pi/3)),
                                   'angle': -2*pi/3}

        self._sharpPos['sharp6'] = {'pos': QtCore.QPointF(baseLength/2 * cos(2*pi/3),
                                                             baseLength/2 * sin(2*pi/3)),
                                   'angle': 2*pi/3}

        self._sharpPos['sharp7'] = {'pos': QtCore.QPointF(baseLength/2 * cos(pi),
                                                             baseLength/2 * sin(pi)),
                                   'angle': pi}

        # Add sharp sensors
        sharp0 = ProximitySensor('sharp0', self,
                                 self._sharpPos['sharp0']['pos'],
                                 self._sharpPos['sharp0']['angle'])
        sharp1 = ProximitySensor('sharp1', self,
                                 self._sharpPos['sharp1']['pos'],
                                 self._sharpPos['sharp1']['angle'])
        sharp2 = ProximitySensor('sharp2', self,
                                 self._sharpPos['sharp2']['pos'],
                                 self._sharpPos['sharp2']['angle'])
        sharp3 = ProximitySensor('sharp3', self,
                                 self._sharpPos['sharp3']['pos'],
                                 self._sharpPos['sharp3']['angle'])
        sharp4 = ProximitySensor('sharp4', self,
                                 self._sharpPos['sharp4']['pos'],
                                 self._sharpPos['sharp4']['angle'])
        sharp5 = ProximitySensor('sharp5', self,
                                 self._sharpPos['sharp5']['pos'],
                                 self._sharpPos['sharp5']['angle'])
        sharp6 = ProximitySensor('sharp6', self,
                                 self._sharpPos['sharp6']['pos'],
                                 self._sharpPos['sharp6']['angle'])
        sharp7 = ProximitySensor('sharp7', self,
                                 self._sharpPos['sharp7']['pos'],
                                 self._sharpPos['sharp7']['angle'])

        # And append it to the list of embedded proximity sensors
        self.proxSensors().append(sharp0)
        self.proxSensors().append(sharp1)
        self.proxSensors().append(sharp2)
        self.proxSensors().append(sharp3)
        self.proxSensors().append(sharp4)
        self.proxSensors().append(sharp5)
        self.proxSensors().append(sharp6)
        self.proxSensors().append(sharp7)

        # Append all sensors to the robot items list
        for sensor in self.proxSensors():
            self.addItem(sensor)

        # Show proximity sensors by default
        self.showProxSensors(True)

        # Cache the bounding rect
        bodyX = (-self._wheelBaseLength/2) * const.m2pix
        bodyY = (-self._wheelBaseLength/2) * const.m2pix
        bodyW = self._wheelBaseLength * const.m2pix
        bodyH = self._wheelBaseLength * const.m2pix
        self._boundingRect = QtCore.QRectF(bodyX, bodyY, bodyW, bodyH)

        # Cache the shape
        self._shape = QtGui.QPainterPath()
        self._shape.addEllipse(bodyX, bodyY, bodyW, bodyH);

    # Get the wheel radius (in m)
    def getWheelRadius(self, ):
        """
        """
        return self._wheelRadius

    # Get the wheel base length (in m)
    def getWheelBaseLength(self, ):
        """
        """
        return self._wheelBaseLength

    # Set the current left wheel speed (in m/s)
    def setLeftWheelSpeed(self, speed_):
        """
        """
        self._leftWheelSpeed = speed_

    # Set the current right wheel speed (in m/s)
    def setRightWheelSpeed(self, speed_):
        """
        """
        self._rightWheelSpeed = speed_

    # Return the current left wheel speed (in m/s)
    def getLeftWheelSpeed(self, ):
        """
        """
        return self._leftWheelSpeed

    # Set the speed of both wheels (in m/s)
    def setWheelSpeeds(self, vel_l, vel_r):
        """
        """
        self._leftWheelSpeed = vel_l
        self._rightWheelSpeed = vel_r

    # Get current speed (in m/s)
    def getSpeed(self, ):
        """
        """
        v, w = self.dynamics.diff2Uni(self._leftWheelSpeed, self._rightWheelSpeed)
        return v

    # Return the current left wheel speed (in m/s)
    def getRightWheelSpeed(self, ):
        """
        """
        return self._rightWheelSpeed

    # Return an estimate of the area painted by the item
    def boundingRect(self, ):
        """
        """
        return self._boundingRect

    # Define the accurate shape of the item
    def shape(self, ):
        """
        """
        return self._shape

    # Define how to paint the robot
    def paint(self, painter, option, widget):
        """
        """
        # Body
        painter.setBrush(QtGui.QColor("light grey"))
        bodyX = (-self._wheelBaseLength/2) * const.m2pix
        bodyY = (-self._wheelBaseLength/2) * const.m2pix
        bodyW = self._wheelBaseLength * const.m2pix
        bodyH = self._wheelBaseLength * const.m2pix
        painter.drawEllipse(bodyX, bodyY, bodyW, bodyH)

        # Left wheel
        wheelW = bodyW / 3
        wheelH = bodyH / 6
        lwheelX = -wheelW/2
        lwheelY = -bodyH/2 + wheelH/2
        painter.setBrush(QtGui.QColor("black"))
        painter.drawRect(lwheelX, lwheelY, wheelW, wheelH)

        # Right wheel
        rwheelX = -wheelW/2
        rwheelY = bodyH/2 - wheelH - wheelH/2
        painter.drawRect(rwheelX, rwheelY, wheelW, wheelH)
