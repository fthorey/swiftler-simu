#!/usr/bin/python
# coding: utf-8

from PyQt4 import QtCore, QtGui

class WorldView(QtGui.QGraphicsView):
    """ WorldView class displays the embedded world to the real world
    """

    def __init__(self, parent_=None):
        """
        """
        # Call parent constructor
        super(WorldView, self).__init__(parent_)


    def focusOnWorld(self):
        """Scale the view to include all of the world (including robots)"""
        # Set scene bounding rectangle (in pixel)
        self.scene().setSceneRect(self.scene().itemsBoundingRect())
        return self.scene().itemsBoundingRect().getCoords()

    def wheelEvent(self, event):
        """
        """
        # self.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse);
        scaleFactor = 1.15
        if event.delta() > 0:
            self.scale(scaleFactor, scaleFactor)
        else:
            self.scale(1.0 / scaleFactor, 1.0 / scaleFactor)
