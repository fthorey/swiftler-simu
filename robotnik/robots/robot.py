#!/usr/bin/python
# coding: utf-8

from physics.dynamics import DifferentialDrive
from PyQt4 import QtGui, QtCore

class Robot(QtGui.QGraphicsItem):
    """ Robot class handles a robot
    """

    # Constructor
    def __init__(self, name_, wheelRadius_, wheelBaseLength_):
        """
        """
        # Call parent constructor
        super(Robot, self).__init__()

        # Name of the robot
        self.name = name_

        # Radius of the wheels
        self.wheelRadius = wheelRadius_

        # Length between each wheel
        self.wheelBaseLength = wheelBaseLength_

        # Robot follow the differential drive dynamic
        self.dynamics = DifferentialDrive(self.wheelRadius, self.wheelBaseLength)

        # Current position of the robot in its own referential
        self.pos = QtCore.QPointF(0, 0)

        # Current angle of the robot in its own referential
        self.theta = 0
        self.setRotation(self.theta);

        # Current speed of the left wheel in its own referential
        self.leftWheelSpeed = 100

        # Current speed of the right wheel in its own referential
        self.rightWheelSpeed = 0

        # Current color of the robot
        self.color = QtGui.QColor(200, 0, 0)

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

    def getPos(self, ):
        """
        """
        return self.pos

    # Return the current theta angle
    def getTheta(self, ):
        """
        """
        return self.theta

    # Return an estimate of the area painted by the item (must be overloaded)
    def boundingRect(self, ):
        """
        """
        adjust = 0.5;
        return QtCore.QRectF(-18 - adjust, -22 - adjust,
                             36 + adjust, 60 + adjust)

    # Define the accurate shape of the item
    def shape(self, ):
        """
        """
        path = QtGui.QPainterPath()
        path.addRect(0, 0, 50, 50);
        return path;

    # Define how to paint the shape (must be overloaded)
    def paint(self, painter, option, widget):
        """
        """
        painter.setBrush(self.color);
        painter.drawEllipse(0, 0, 100, 100);

    # Return the name of the robot
    def getName(self, ):
        """
        """
        return self.name

    # Return the current coordinates of the robot
    def getPos(self, ):
        """
        """
        return self.pos

    # Action to perform when the scene changes
    def advance(self, step_):
        """
        """
        if (not step_):
            return

        self.dynamics.update(self)
