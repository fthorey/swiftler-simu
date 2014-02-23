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

        # Rename scene to world
        self.world = self.scene

        # Invert the world to get a correct frame to work in
        self.scale(-1, -1)

    def focusOnWorld(self, ):
        """Scale the view to include all of the world (including robots).
        """
        # Unset the zoom on robot parameter
        self.world().setZoomOnRobot(False)
        # Set scene bounding rectangle (in pixel)
        self.world().setSceneRect(self.world().itemsBoundingRect())
        # Update the view
        self.fitInView(self.world().sceneRect(), QtCore.Qt.KeepAspectRatio)

    def focusOnRobot(self, ):
        """Scale the view to focus only on the robot.
        """
        # Set the zoom on robot parameter
        self.world().setZoomOnRobot(True)
        # Search for the master robot
        for robot in self.world().getRobots():
            if robot.isMasterRobot():
                # Update view
                boundingRect = robot.mapRectToParent(robot.enlargedBoundingRect())
                self.fitInView(boundingRect, QtCore.Qt.KeepAspectRatio)
                break

    def resizeEvent(self, event):
        """Check if the current zoom is on the robot on resize events.
        """
        if self.world().isZoomOnRobot():
            self.focusOnRobot()
        else:
            self.focusOnWorld()
