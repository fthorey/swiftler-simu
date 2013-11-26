#!/usr/bin/python
# coding: utf-8

from PyQt4 import QtGui, QtCore

class Shape(QtGui.QGraphicsItem):
    """ Shape class is the basic class for all objects in the simulator
    """

    def __init__(self, name_):
        """
        """
        # Call parent constructor
        super(Shape, self).__init__()

        # Name of the shape
        self.name = name_

        # Angle of the shape in its parent referential
        self.theta = 0

        # Main color of the shape
        self.color = QtGui.QColor(0, 0, 0)

    # Return the name of the shape
    def getName(self, ):
        """
        """
        return self.name

    # Return the current theta angle
    def getTheta(self, ):
        """
        """
        return self.theta

    # Set the position of the shape
    def setTheta(self, theta_):
        """
        """
        self.theta = theta_

    # Return an estimate of the area painted by the item
    def boundingRect(self, ):
        """
        """
        return QtCore.QRectF(-50, -50, 100, 100)

    # Define the accurate shape of the item
    def shape(self, ):
        """
        """
        path = QtGui.QPainterPath()
        path.addRect(-50, -50, 100, 100);
        return path;

    # Define how to paint the shape
    def paint(self, painter, option, widget):
        """
        """
        painter.setBrush(self.color);
        painter.drawRect(-50, -50, 100, 100)
