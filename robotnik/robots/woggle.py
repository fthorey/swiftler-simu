#!/usr/bin/python
# coding: utf-8

from robots.robot import Robot
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

        # Radius of the wheels
        self.wheelRadius = wheelRadius_

        # Length between each wheel
        self.wheelBaseLength = wheelBaseLength_

        # The Woggle robot follow the differential drive dynamic
        self.setDynamics(DifferentialDrive(self.wheelRadius, self.wheelBaseLength))

        # Current speed of the left wheel in its own referential
        self.leftWheelSpeed = 0

        # Current speed of the right wheel in its own referential
        self.rightWheelSpeed = 0

    # Return the current left wheel speed
    def getLeftWheelSpeed(self, ):
        """
        """
        return self.leftWheelSpeed

    # Return the current left wheel speed
    def getRightWheelSpeed(self, ):
        """
        """
        return self.rightWheelSpeed


    # Return an estimate of the area painted by the item
    def boundingRect(self, ):
        """
        """
        return QtCore.QRectF(0, 0, 110, 110)

    # Define how to paint the robot
    def paint(self, painter, option, widget):
        """
        """
        # Body
        painter.setBrush(QtGui.QColor("light grey"))
        painter.drawEllipse(-50, -50, 100, 100)

        # Left wheel
        painter.setBrush(QtGui.QColor("black"))
        painter.drawRect(-20, -55, 40, 20)

        # Right wheel
        painter.drawRect(-20, 35, 40, 20)

        # Ultrasound sensor
        painter.drawRect(40, -15, 10, 30)
        painter.drawRect(50, -10, 8, 8)
        painter.drawRect(50, 2, 8, 8)
