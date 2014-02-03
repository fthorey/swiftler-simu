#!/usr/bin/python
# coding: utf-8

from PyQt4 import QtGui, QtCore
from utils import const

class Tracker(QtCore.QObject):
    """
    """
    def __init__(self, pos_, parent=None):
        """
        """
        # Call parent constructor
        super(Tracker, self).__init__(parent)

        # Scale position and add it to current track
        self.track = QtGui.QPainterPath(self.scalePosition(pos_))

    def restart(self, pos_):
        """
        """
        self.track = QtGui.QPainterPath(self.scalePosition(pos_))

    def getTrack(self, ):
        """
        """
        return self.track

    def scalePosition(self, pos_):
        return QtCore.QPointF(pos_.x()*const.m2pix, pos_.y()*const.m2pix)

    def addPosition(self, pos_):
        """
        """
        self.track.lineTo(self.scalePosition(pos_))
