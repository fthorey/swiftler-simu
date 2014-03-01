#!/usr/bin/python
# coding: utf-8

from PyQt4 import QtGui, QtCore

class Tracker(QtCore.QObject):
    """
    """
    def __init__(self, pos_, parent=None):
        """
        """
        # Call parent constructor
        super(Tracker, self).__init__(parent)

        x, y, theta = pos_
        self.track = QtGui.QPainterPath(QtCore.QPointF(x, y))

    def restart(self, pos_):
        """Restart the tracker.
        """
        x, y, theta = pos_
        self.track = QtGui.QPainterPath(QtCore.QPointF(x, y))

    def getTrack(self, ):
        """Get the current track.
        """
        return self.track

    def addPosition(self, pos_):
        """Add a position to the current track.
        """
        x, y, theta = pos_
        self.track.lineTo(QtCore.QPointF(x, y))
