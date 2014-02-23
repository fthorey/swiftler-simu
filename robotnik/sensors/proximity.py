#!/usr/bin/python
# coding: utf-8

from utils.rect import Rect
from utils.simobject import SimObject
from math import pi, tan, degrees, cos, sin, sqrt
from utils import const

from PyQt4 import QtGui, QtCore

class ProximitySensor(SimObject):
    """ ProximitySensor class represents a generic class for proximity sensors
    """

    count = 0

    def __init__(self, pos_, ):
        """
        """
        super(ProximitySensor, self).__init__('sharp' + str(self.count))
        self.count = self.count + 1

        # Location on the parent object (in m)
        self.setPos(pos_[0])

        # angle of the beam (in rad)
        self.setAngle(pos_[1])

        # View angle (in rad)
        self._phi = pi/10

        # Minimum range (in m)
        self._rmin = 0.01

        # Maximum range (in m)
        self._rmax = 0.10

        # Maximum detection distance of the sensor (in m)
        self._maxDist = 65536

        # Current detection ditance of the sensor (in m)
        self._currDist = self._maxDist

        # The current cone of the sensor
        self._pts = self.getCone(self._rmax)

        # Update current bounding rect
        self.__updateBoundingRect()

        # Update current shape
        self.__updateShape()

        # Brush color
        self._brushColor = QtGui.QColor('red')
        self._brushColor.setAlpha(50)
        self._brush = QtGui.QBrush(self._brushColor)

        # Pen color
        self._penColor = QtGui.QColor('red')
        self._penColor.setAlpha(128)
        self._pen = QtGui.QPen(QtCore.Qt.NoPen)

    def __updateBoundingRect(self, ):
        """
        """
        # Current bounding rect
        xmin, ymin, xmax, ymax = self.getBounds()
        self._boundingRect = QtCore.QRectF(QtCore.QPointF(xmin, ymin), QtCore.QPointF(xmax, ymax))

    def __updateShape(self, ):
        # Cache the shape
        points = [QtCore.QPointF(p[0], p[1]) for p in self._pts]
        self._shape = QtGui.QPainterPath()
        self._shape.addPolygon(QtGui.QPolygonF(points))

    def isAtMaxRange(self, ):
        """
        """
        return self._currDist == self._maxDist

    def getCone(self, distance):
        return [(self._rmin*cos(self._phi/2),self._rmin*sin(self._phi/2)),
                (distance*cos(self._phi/2),distance*sin(self._phi/2)),
                (distance,0),
                (distance*cos(self._phi/2),-distance*sin(self._phi/2)),
                (self._rmin*cos(self._phi/2),-self._rmin*sin(self._phi/2))]

    def show(self, show_):
        if show_:
            self._brush = QtGui.QBrush(self._brushColor)
        else:
            self._brush = QtGui.QBrush(QtCore.Qt.NoBrush)

        # Trigger an update of the view
        self.update()

    # Restart the sensor to its initial state
    def restart(self, ):
        """
        """

    def getEnvelope(self):
        """Return the envelope of the sensor"""
        return self._pts

    def boundingRect(self, ):
        """
        """
        return self._boundingRect

    def shape(self, ):
        """
        """
        return self._shape

    # Define how to paint the shape
    def paint(self, painter, option, widget):
        """
        """
        painter.setBrush(self._brush)
        painter.setPen(self._pen)

        points = [QtCore.QPointF(p[0], p[1]) for p in self._pts]
        painter.drawPolygon(QtGui.QPolygonF(points))

    def updateDistance(self, simObject = None):
        """updates all the distances from the reading"""
        if simObject is None:
            # reset distance to max
            self.__distance = 65536
            self._pts = self.getCone(self._rmax)
            return True
        else:
            distance2obj = self.getDistanceTo(simObject)
            if distance2obj:
                if self.__distance > distance2obj:
                    self._pts = self.getCone(distance2obj)
                    self.__distance = distance2obj
                    return True
        return False

    def getDistanceTo(self, simObject):
        """Gets the distance to another simobject
        returns distance in meters or None if not in contact"""
        ox, oy = self.pos().x(), self.pos().y()
        minDist = None
        for px, py in self.getContactPoints(simObject):
            distance = sqrt((px-ox)*(px-ox)+(py-oy)*(py-oy))
            if minDist is not None:
                if distance < minDist:
                    minDist = distance
            else: minDist = distance
        return minDist
