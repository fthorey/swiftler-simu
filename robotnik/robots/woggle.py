#!/usr/bin/python
# coding: utf-8

from math import pi, degrees, radians
from common import const
from robots.robot import Robot
from sensors.proximity import ProximitySensor
from controllers.supervisor import WoggleSupervisor
from physics.dynamics import DifferentialDrive
from PyQt4 import QtGui, QtCore

class Woggle(Robot):
    """ Woggle class handles a Woggle robot
    """

    def __init__(self, name_, wheelRadius_, wheelBaseLength_):
        """
        """
        # Call parent constructor
        super(Woggle, self).__init__(name_)

        # Radius of the wheels (m)
        self.wheelRadius = wheelRadius_ * const.scaleFactor

        # Length between each wheel (m)
        self.wheelBaseLength = wheelBaseLength_ * const.scaleFactor

        # The Woggle robot follow the differential drive dynamic
        self.setDynamics(DifferentialDrive(self))

        # A supervisor is attached to the Woggle robot
        self.setSupervisor(WoggleSupervisor(self))

        # Current speed of the left wheel in its own referential (rad/s)
        self.leftWheelSpeed = 0

        # Current speed of the right wheel in its own referential (rad/s)
        self.rightWheelSpeed = 0

        # List of all proximity sensors of the robot
        self.proxSensors = list()

        # Add a sharp sensor
        sharp1Pos = QtCore.QPointF((self.wheelBaseLength/2) * const.m2pix, 0)
        sharp1 = ProximitySensor("sharp1", self, sharp1Pos, 0)
        self.proxSensors.append(sharp1)

    # Return the list of all proximity sensors
    def getProxSensors(self, ):
        """
        """
        return self.proxSensors

    # Get the wheel radius
    def getWheelRadius(self, ):
        """
        """
        return self.wheelRadius

    # Get the wheel base length
    def getWheelBaseLength(self, ):
        """
        """
        return self.wheelBaseLength

    # Set the current left wheel speed
    def setLeftWheelSpeed(self, speed_):
        """
        """
        self.leftWheelSpeed = speed_

    # Set the current right wheel speed
    def setRightWheelSpeed(self, speed_):
        """
        """
        self.rightWheelSpeed = speed_

    # Return the current left wheel speed
    def getLeftWheelSpeed(self, ):
        """
        """
        return self.leftWheelSpeed

    # Set the speed of both wheels
    def setWheelSpeeds(self, vel_l, vel_r):
        """
        """
        self.leftWheelSpeed = vel_l
        self.rightWheelSpeed = vel_r

    # Return the current left wheel speed
    def getRightWheelSpeed(self, ):
        """
        """
        return self.rightWheelSpeed

    # Return an estimate of the area painted by the item
    def boundingRect(self, ):
        """
        """
        bodyX = (-self.wheelBaseLength/2) * const.m2pix
        bodyY = (-self.wheelBaseLength/2) * const.m2pix
        bodyW = self.wheelBaseLength * const.m2pix
        bodyH = self.wheelBaseLength * const.m2pix
        return QtCore.QRectF(bodyX, bodyY, bodyW, bodyH)

    # Define the accurate shape of the item
    def shape(self, ):
        """
        """
        path = QtGui.QPainterPath()
        bodyX = (-self.wheelBaseLength/2) * const.m2pix
        bodyY = (-self.wheelBaseLength/2) * const.m2pix
        bodyW = self.wheelBaseLength * const.m2pix
        bodyH = self.wheelBaseLength * const.m2pix
        path.addRect(bodyX, bodyY, bodyW, bodyH);
        return path;

    # Define how to paint the robot
    def paint(self, painter, option, widget):
        """
        """
        # Body
        painter.setBrush(QtGui.QColor("light grey"))
        bodyX = (-self.wheelBaseLength/2) * const.m2pix
        bodyY = (-self.wheelBaseLength/2) * const.m2pix
        bodyW = self.wheelBaseLength * const.m2pix
        bodyH = self.wheelBaseLength * const.m2pix
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

        # Ultrasound sensor
        baseW = bodyW * 0.08
        baseH = bodyW * 0.24
        baseX = bodyW/2 - 2*baseW
        baseY = -baseH/2
        soundW = bodyW * 0.06
        soundH = bodyW * 0.06
        soundX = baseX + soundW
        sound1Y = baseY + (baseH - 2*soundW) / 3
        sound2Y = sound1Y + soundW + (baseH - 2*soundW) / 3
        painter.drawRect(baseX, baseY, baseW, baseH)
        painter.drawRect(soundX, sound1Y, soundW, soundH)
        painter.drawRect(soundX, sound2Y, soundW, soundH)
