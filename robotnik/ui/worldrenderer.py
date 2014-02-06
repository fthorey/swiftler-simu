#!/usr/bin/python
# coding: utf-8

from utils import const
from PyQt4 import QtCore, QtGui

class WorldRenderer(QtGui.QGraphicsScene):
    """ WorldRenderer class renders the embedded world
    """

    def __init__(self, parent_):
        """
        """
        # Call parent constructor
        super(WorldRenderer, self).__init__(parent_)

        # Define a grid size of 10cm
        self._gridSize = 0.1

        self._gridPen = QtGui.QPen(QtGui.QColor(0x808080))
        self._gridPen.setStyle(QtCore.Qt.DotLine)

    def setGridSize(self, size_):
        """
        """
        self._gridSize = size_
