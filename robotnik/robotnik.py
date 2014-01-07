#!/usr/bin/python
# coding: utf-8

import sys
from math import pi
from physics.world import World
from robots.woggle import Woggle
from common.shape import *
from common import const
import ui.icons

from PyQt4 import QtGui, QtCore, uic

class Robotnik(QtGui.QMainWindow):
    """ Robotnik class is the main container for the simulator
    """

    # Conversion factor between pixels and meters
    const.pix2m = 0.0002645833333333
    const.m2pix = 3779.527559055

    # Scale factor
    const.scaleFactor = 1.0/2.5

    # To notify others that the step duration has changed
    stepChanged = QtCore.pyqtSignal(int)

    def __init__(self, stepDuration_):
        """
        """
        # Call parent constructor
        super(Robotnik, self).__init__()

        # Load window design
        uic.loadUi('ui/mainwindow.ui', self)

        # Set step duration
        self.stepDuration = stepDuration_
        self.spinBox.setValue(self.stepDuration)

        # Remove aliasing
        self.graphicsView.setRenderHint(QtGui.QPainter.Antialiasing);
        self.graphicsView.setCacheMode(QtGui.QGraphicsView.CacheBackground);

        # Create a new world
        self.world = World(self)
        self.world.setSceneRect(-300, -300, 600, 600);

        # Attach the world to the view
        self.graphicsView.setScene(self.world)

        # Center the main window
        self.center()

        # Show the view on screen
        self.show()

        # Connect slots
        # Play
        self.action_Play.triggered.connect(self.start)
        # Pause
        self.action_Pause.triggered.connect(self.pause)
        # Restart
        self.action_Restart.triggered.connect(self.restart)
        # Step duration
        self.spinBox.editingFinished.connect(self.updateStepDuration)
        # Max steps
        self.spinBox_2.editingFinished.connect(self.updateMaxSteps)

        # Create a timer to handle time
        self.timer = QtCore.QTimer(self)

        # Connect timer trigger signal to stop
        # Connect timer trigger signal to world advance
        self.timer.timeout.connect(self.stop)
        self.timer.timeout.connect(self.world.advance)

        self.maxSteps = 50
        # Update value in associated spin box
        self.spinBox_2.setValue(self.maxSteps)
        # Update maximum steps max value
        self.spinBox_2.setMaximum(1000)

        # Current number of steps
        self.currentSteps = 0

    def updateMaxSteps(self, ):
        self.maxSteps = self.spinBox_2.value()

    def updateStepDuration(self, ):
        """
        """
        # Get changed step duration
        self.stepDuration = self.spinBox.value()
        # Notify other users that the step duration has changed
        self.stepChanged.emit(self.stepDuration)

    def restart(self, ):
        """
        """
        # Stop the timer
        self.currentSteps = 0
        self.timer.stop()

        # Put robots at there initial position
        for robot in self.world.getRobots():
            pos, theta = robot.getInitialPos()
            robot.setPos(pos)
            robot.setTheta(theta)

    def stop(self, ):
        """
        """
        self.currentSteps = self.currentSteps + 1

        if self.currentSteps == self.maxSteps:
            self.timer.stop()
            self.currentSteps = 0

    def start(self, ):
        """
        """
        self.timer.start(self.stepDuration);

    def pause(self, ):
        """
        """
        self.timer.stop()

    # Center the main window
    def center(self, ):
        """
        """
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # Add a furniture in the world
    def addFurniture(self, furniture_, position_):
        """
        """
        self.world.addFurniture(furniture_, position_)

    # Add a robot in the world
    def addRobot(self, robot_, position_):
        """
        """
        self.world.addRobot(robot_, position_, self.stepDuration)
        self.stepChanged.connect(robot_.updateStepDuration)

if __name__ == '__main__':
    # Create a Qt application
    app = QtGui.QApplication([])

    # Create a robotnik simulator with a step duration of 10ms
    robotnik = Robotnik(10)

    # Create a differential drive robot
    # Wheel radius = 2.1cm
    # In-between wheel base length = 8.85cm
    woggle = Woggle("woggle", 0.021, 0.0885)

    # Add the objects to the simulator
    robotnik.addRobot(woggle, QtCore.QPointF(0, 0))

    # Advance the simulation for some steps (1000 * 10ms = 10s)
    # robotnik.step(1000)

    # Exit
    sys.exit(app.exec_())
