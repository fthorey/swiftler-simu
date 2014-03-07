#!/usr/bin/python
# coding: utf-8

from PyQt4 import QtGui, QtCore
from math import degrees
from utils import pylygon

class SimObject(QtGui.QGraphicsItem):
    """ SimObject class is the basic class for all objects in the simulator
    """

    def __init__(self, name_, pos_, brush_, parent=None):
        """
        """
        # Call parent constructor
        super(SimObject, self).__init__(parent)

        # Name of the simObject
        self._name = name_

        # Set the position
        x, y, angle = pos_
        self.setPos(QtCore.QPointF(x,y))
        self.setAngle(angle)

        # Save the brush
        self._brush = brush_
        # Set to NoPen by default
        self._pen = QtCore.Qt.NoPen

        # Cached envelope (in its own coordinates system)
        self._envelope = None

        # Cached world envelope (in the scene coordinates system)
        self._worldEnvelope = None

    def mapToParent(self, *args, **kwargs):
        """
        """
        obj = None
        if (len(args) == 1) and (isinstance(args[0], tuple)):
            point = QtCore.QPointF(args[0][0], args[0][1])
            obj = super(SimObject, self).mapToParent(point)
        else:
            obj = super(SimObject, self).mapToParent(*args, **kwargs)

        if isinstance(obj, QtCore.QPointF):
            return (obj.x(), obj.y())
        else:
            return obj

    def mapToScene(self, *args, **kwargs):
        """
        """
        obj = None
        if (len(args) == 1) and (isinstance(args[0], tuple)):
            point = QtCore.QPointF(args[0][0], args[0][1])
            obj = super(SimObject, self).mapToScene(point)
        else:
            obj = super(SimObject, self).mapToScene(*args, **kwargs)

        if isinstance(obj, QtCore.QPointF):
            return (obj.x(), obj.y())
        else:
            return obj

    def setBrush(self, brush_):
        """Set the brush of the simObject
        """
        self._brush = brush_

    def setPen(self, pen_):
        """Set the pen of the simObject
        """
        self._pen = pen_

    def brush(self, ):
        """Return the brush of the simObject
        """
        return self._brush

    def pen(self, ):
        """Return the pen of the simObject
        """
        return self._pen

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
            self._worldEnvelope = [self.mapToScene(p) for p in self.getEnvelope()]

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
