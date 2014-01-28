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

    # Constructor
    # Get wheel radius (in m)
    # Get in-between wheels distance (in m)
    def __init__(self, name_, wheelRadius_, wheelBaseLength_):
        """
        """
        # Call parent constructor
        super(Woggle, self).__init__(name_)

        # Radius of the wheels (m)
        self.wheelRadius = wheelRadius_

        # Length between each wheel (m)
        self.wheelBaseLength = wheelBaseLength_

        # The Woggle robot follow the differential drive dynamic
        self.setDynamics(DifferentialDrive(self))

        # A supervisor is attached to the Woggle robot
        self.setSupervisor(WoggleSupervisor(self))

        # Current speed of the left wheel (rad/s)
        self.leftWheelSpeed = 0

        # Current speed of the right wheel (rad/s)
        self.rightWheelSpeed = 0

        # Set default heading angle (in rad)
        self.setTheta(0)

        # Add a sharp sensor
        # Set where to place this sensor (in m)
        sharp1Pos = QtCore.QPointF((self.wheelBaseLength/2), 0)
        # Create the sensor
        sharp1 = ProximitySensor("sharp1", self, sharp1Pos, 0)
        # And append it to the list of embedded proximity sensors
        self.proxSensors.append(sharp1)

    # Return the list of all proximity sensors
    def getProxSensors(self, ):
        """
        """
        return self.proxSensors

    # Get the wheel radius (in m)
    def getWheelRadius(self, ):
        """
        """
        return self.wheelRadius

    # Get the wheel base length (in m)
    def getWheelBaseLength(self, ):
        """
        """
        return self.wheelBaseLength

    # Set the current left wheel speed (in m/s)
    def setLeftWheelSpeed(self, speed_):
        """
        """
        self.leftWheelSpeed = speed_

    # Set the current right wheel speed (in m/s)
    def setRightWheelSpeed(self, speed_):
        """
        """
        self.rightWheelSpeed = speed_

    # Return the current left wheel speed (in m/s)
    def getLeftWheelSpeed(self, ):
        """
        """
        return self.leftWheelSpeed

    # Set the speed of both wheels (in m/s)
    def setWheelSpeeds(self, vel_l, vel_r):
        """
        """
        self.leftWheelSpeed = vel_l
        self.rightWheelSpeed = vel_r

    # Get current speed (in m/s)
    def getSpeed(self, ):
        """
        """
        v, w = self.dynamics.diff2Uni(self.leftWheelSpeed, self.rightWheelSpeed)
        return v

    # Return the current left wheel speed (in m/s)
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
        path.addEllipse(bodyX, bodyY, bodyW, bodyH);
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
