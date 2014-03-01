#!/usr/bin/python
# coding: utf-8

from PyQt4 import QtGui, QtCore

class Tracker(QtCore.QObject):
    """The Tracker class implements a simple way to store the path followed
    by a robot.
    """
    def __init__(self, pos_, parent=None):
        """
        """
        # Call parent constructor
        super(Tracker, self).__init__(parent)

        x, y = pos_
        self.track = QtGui.QPainterPath(QtCore.QPointF(x, y))

    def getTrack(self, ):
        """Get the current track.
        """
        return self.track

    def addPosition(self, pos_):
        """Add a position to the current track.
        """
        x, y = pos_
        self.track.lineTo(QtCore.QPointF(x, y))
