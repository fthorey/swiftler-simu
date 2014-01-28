#!/usr/bin/python
# coding: utf-8

from utils import const
from PyQt4 import QtCore, QtGui

class WorldRenderer(QtGui.QGraphicsScene):
    """ WorldRenderer class renders the embedded world
    """

    def __init__(self, parent_, size_):
        """
        """
        # Call parent constructor
        super(WorldRenderer, self).__init__(parent_)

        # Define a grid size of 10cm
        self.gridSize = 0.1*const.m2pix

        self.gridPen = QtGui.QPen(QtGui.QColor(0x808080))
        # self.gridPen.setStyle(QtCore.Qt.DotLine)

        # Define world dimension (in m)
        self.size = size_

        # Set scene bounding rectangle
        # setSceneRect takes parameters expressed in pixel
        # -> Value in m are converted to pixel
        self.setSceneRect(-(self.size/2)*const.m2pix, -(self.size/2)*const.m2pix,
                          (self.size)*const.m2pix, (self.size)*const.m2pix);

    def wheelEvent(self, event):
        """
        """
        self.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse);
        scaleFactor = 1.15
        if event.delta() > 0:
            self.scale(scaleFactor, scaleFactor)
        else:
            self.scale(1.0 / scaleFactor, 1.0 / scaleFactor)

    def drawBackground(self, painter, rect):
        painter.setPen(self.gridPen)
        painter.setWorldMatrixEnabled(True);

        left = int(rect.left()) - (int(rect.left()) % self.gridSize);
        top = int(rect.top()) - (int(rect.top()) % self.gridSize);

        lines = list()
        x = left
        while x < rect.right():
            lines.append(QtCore.QLineF(x, rect.top(), x, rect.bottom()))
            x += self.gridSize
        y = top
        while y < rect.bottom():
            lines.append(QtCore.QLineF(rect.left(), y, rect.right(), y))
            y += self.gridSize

        painter.drawLines(lines)
