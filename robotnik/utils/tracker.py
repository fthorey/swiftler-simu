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

        # Scale position and add it to current track
        self.track = QtGui.QPainterPath(QtCore.QPointF(pos_.x(), pos_.y()))

    def restart(self, pos_):
        """
        """
        self.track = QtGui.QPainterPath(QtCore.QPointF(pos_.x(), pos_.y()))

    def getTrack(self, ):
        """
        """
        return self.track

    def addPosition(self, pos_):
        """
        """
        self.track.lineTo(QtCore.QPointF(pos_.x(), pos_.y()))
