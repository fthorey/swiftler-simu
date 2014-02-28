#!/usr/bin/python
# coding: utf-8

from PyQt4 import QtCore, QtGui

class WorldView(QtGui.QGraphicsView):
    """ The WorldView class displays the embedded world to real world.
    """

    def __init__(self, parent_=None):
        """
        """
        # Call parent constructor
        super(WorldView, self).__init__(parent_)

    def focusOnWorld(self, ):
        """Scale the view to include all of the world (including robots).
        """
        # Set scene bounding rectangle (in pixel)
        self.scene().setSceneRect(self.scene().itemsBoundingRect())
        # Update the view
        self.fitInView(self.scene().sceneRect(), QtCore.Qt.KeepAspectRatio)

    def scaleOnRobot(self, ):
        """Scale the view on the robot.
        """
        for robot in self.scene().getRobots():
            if robot.isMasterRobot():
                # Update bounding rect
                self._boundingRect = robot.mapRectToParent(robot.enlargedBoundingRect())
                # Update view
                self.fitInView(self._boundingRect, QtCore.Qt.KeepAspectRatio)
                break

    def focusOnRobot(self, ):
        """Scale the view to focus only on the robot.
        """
        # Set the zoom on robot parameter
        for robot in self.scene().getRobots():
            if robot.isMasterRobot():
                # Update view
                self.fitInView(self._boundingRect, QtCore.Qt.KeepAspectRatio)
                # Center on master robot
                self.centerOn(robot.pos())
                break

    def resizeEvent(self, event):
        """Check if the current zoom is on the robot on resize events.
        """
        if self.scene().isZoomOnRobot():
            self.focusOnRobot()
        else:
            self.focusOnWorld()
