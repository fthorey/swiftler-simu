#!/usr/bin/python
# coding: utf-8

from common.shape import Shape
from math import pi, tan, degrees
from common import const

from PyQt4 import QtGui, QtCore

class ProximitySensor(Shape):
    """ ProximitySensor class represents a generic class for proximity sensors
    """

    def __init__(self, name_, parent_, location_, beamAngle_):
        """
        """
        super(ProximitySensor, self).__init__(name_, parent_)

        # Location on the parent object
        self.setPos(location_)

        # angle of the beam (rad)
        self.setTheta(beamAngle_)

        # View angle
        self.spread = pi/4

        # Minimum range
        self.minRange = 0.05*const.scaleFactor

        # Maximum range
        self.maxRange = 0.08*const.scaleFactor

        # Current range =
        self.currRange = self.maxRange

    # Check if current range > minrange
    def isMinRangeReached(self, ):
        return self.currRange <= self.minRange

    # Get current beam range
    def getBeamRange(self, ):
        """
        """
        return self.currRange

    # Set current beam range
    def setBeamRange(self, range_):
        """
        """
        self.currRange = range_

    # Reduce beam range
    def reduceBeamRange(self, reduce_):
        """
        """
        self.currRange = self.currRange - reduce_

    # Increase beam range
    def increaseBeamRange(self, increase_):
        """
        """
        self.currRange = self.currRange + increase_

    # Return the left limit of the beam
    def getBeamLeftLimit(self, ):
        """
        """
        return QtCore.QPointF(self.currRange, -self.currRange * tan(self.spread/2))

    # Return the right limit of the beam
    def getBeamRightLimit(self, ):
        """
        """
        return QtCore.QPointF(self.currRange, self.currRange * tan(self.spread/2))

    # Return an estimate of the area painted by the item
    def boundingRect(self, ):
        """
        """
        rectX = 0
        rectY = -self.currRange * tan(self.spread/2) * const.m2pix
        rectW = self.currRange * const.m2pix
        rectH = 2 * self.currRange * tan(self.spread/2) * const.m2pix

        return QtCore.QRectF(rectX, rectY, rectW, rectH)

    # Define the accurate shape of the item
    def shape(self, ):
        """
        """
        path = QtGui.QPainterPath()

        leftLimit = self.getBeamLeftLimit()
        leftLimit = QtCore.QPointF(leftLimit.x() * const.m2pix, leftLimit.y() * const.m2pix)
        rightLimit = self.getBeamRightLimit()
        rightLimit = QtCore.QPointF(rightLimit.x() * const.m2pix, rightLimit.y() * const.m2pix)

        path.addPolygon(QtGui.QPolygonF([QtCore.QPointF(0,0), leftLimit, rightLimit]))

        return path

    # Define how to paint the shape
    def paint(self, painter, option, widget):
        """
        """
        painter.setBrush(QtGui.QColor("red"))

        leftLimit = self.getBeamLeftLimit()
        leftLimit = QtCore.QPointF(leftLimit.x() * const.m2pix, leftLimit.y() * const.m2pix)

        rightLimit = self.getBeamRightLimit()
        rightLimit = QtCore.QPointF(rightLimit.x() * const.m2pix, rightLimit.y() * const.m2pix)

        painter.drawPolygon(QtCore.QPointF(0,0), leftLimit, rightLimit)