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

        # Rename scene to world
        self.world = self.scene

    def focusOnWorld(self, ):
        """Scale the view to include all of the world (including robots)"""
        # Unset the zoom on robot parameter
        self.world().setZoomOnRobot(False)
        # Set scene bounding rectangle (in pixel)
        self.world().setSceneRect(self.world().itemsBoundingRect())
        # Update the view
        self.fitInView(self.world().sceneRect(), QtCore.Qt.KeepAspectRatio)

    def focusOnRobot(self, ):
        """
        """
        # Set the zoom on robot parameter
        self.world().setZoomOnRobot(True)
        # Search for the master robot
        for robot in self.world().getRobots():
            if robot.isMasterRobot():
                # Update view
                self.fitInView(robot.mapRectToParent(robot.boundingRect()), QtCore.Qt.KeepAspectRatio)
                break

    def wheelEvent(self, event):
        """
        """
        # self.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse);
        scaleFactor = 1.15
        if event.delta() > 0:
            self.scale(scaleFactor, scaleFactor)
        else:
            self.scale(1.0 / scaleFactor, 1.0 / scaleFactor)

    def resizeEvent(self, event):
        """
        """
        if self.world().isZoomOnRobot():
            self.focusOnRobot()
        else:
            self.focusOnWorld()
