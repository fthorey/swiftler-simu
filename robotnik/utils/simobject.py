#!/usr/bin/python
# coding: utf-8

from PyQt4 import QtGui, QtCore
from math import degrees
from utils import pylygon

class SimObject(QtGui.QGraphicsItem):
    """ SimObject class is the basic class for all objects in the simulator
    """

    def __init__(self, name_, parent=None):
        """
        """
        # Call parent constructor
        super(SimObject, self).__init__(parent)

        # Name of the simObject
        self._name = name_

        # Cached envelope (in its own coordinates system)
        self._envelope = None

        # Cached world envelope (in the scene coordinates system)
        self._worldEnvelope = None

    def setName(self, name_):
        """Set the name of the simObject
        """
        self._name = name_

    def getName(self, ):
        """Return the name of the simObject
        """
        return self._name

    def getAngle(self, ):
        """Return the current angle of the simObject in its own referential (in rad)
        """
        return self._angle

    def setAngle(self, angle_):
        """Set the current angle of the simObject in its own referential (in rad)
        """
        self._angle = angle_
        self.setRotation(degrees(self._angle))

    def getEnvelope(self, ):
        """Get the envelope of the object in object's local coordinates.

        The envelope is a list of *xy* pairs, describing the shape of the
        bounding polygon.
        """
        raise NotImplementedError("SimObject.getEnvelope")

    def getWorldEnvelope(self, recalculate=False):
        """Get the envelope of the object in world coordinates.
        Used for checking collision.

        The envelope is cached, and will be recalculated if *recalculate*
        is `True`.
        """

        if self._worldEnvelope is None or recalculate:
            temp = [self.mapToScene(p[0], p[1]) for p in self.getEnvelope()]
            self._worldEnvelope = [[p.x(), p.y()] for p in temp]

        return self._worldEnvelope

    def getBounds(self):
        """Get the smallest rectangle that contains the object in the object coordinates
           as a tuple (xmin, ymin, xmax, ymax)"""
        xs, ys = zip(*self.getEnvelope())
        return (min(xs), min(ys), max(xs), max(ys))

    def boundingRect(self, ):
        """Inherited from QGraphicsItem.

        Returns an estimate of the area painted by the item
        """
        raise NotImplementedError("SimObject.boundingRect")

    def shape(self, ):
        """Inherited from QGraphicsItem.

        Returns the exact shape of the item
        """
        raise NotImplementedError("SimObject.shape")

    def getContactPoints(self, other):
         """Get a list of contact points with other object.
         """
         self_poly = pylygon.Polygon(self.getWorldEnvelope())
         other_poly = pylygon.Polygon(other.getWorldEnvelope())
         return self_poly.intersection_points(other_poly)

    def paint(self, painter, option, widget):
        """Inherited from QGraphicsItem.

        Defines how to paint the shape
        """
        raise NotImplementedError("SimObject.paint")
