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
        self._gridSize = 0.1*const.m2pix

        self._gridPen = QtGui.QPen(QtGui.QColor(0x808080))
        self._gridPen.setStyle(QtCore.Qt.DotLine)

    def setGridSize(self, size_):
        """
        """
        self._gridSize = size_

    def drawBackground(self, painter, rect):
        """
        """
        # painter.setPen(self._gridPen)
        # painter.setWorldMatrixEnabled(True);

        # left = int(rect.left()) - (int(rect.left()) % self._gridSize);
        # top = int(rect.top()) - (int(rect.top()) % self._gridSize);

        # lines = list()
        # x = left
        # while x < rect.right():
        #     lines.append(QtCore.QLineF(x, rect.top(), x, rect.bottom()))
        #     x += self._gridSize
        # y = top
        # while y < rect.bottom():
        #     lines.append(QtCore.QLineF(rect.left(), y, rect.right(), y))
        #     y += self._gridSize

        # painter.drawLines(lines)
