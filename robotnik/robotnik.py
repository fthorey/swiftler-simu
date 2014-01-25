#!/usr/bin/python
# coding: utf-8

import sys
from math import pi
from physics.world import World
from robots.woggle import Woggle
from common.shape import *
from common import const
import ui.icons

# Handle Ctrl-C
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

from PyQt4 import QtGui, QtCore, uic

class Robotnik(QtGui.QMainWindow):
    """ Robotnik class is the main container for the simulator
    """

    # Conversion factor between pixels and meters
    const.pix2m = 0.000264583
    const.m2pix = 3779.5276

    # To notify others that the step duration has changed
    stepChanged = QtCore.pyqtSignal(int)

    def __init__(self, stepDuration_):
        """
        """
        # Call parent constructor
        super(Robotnik, self).__init__()

        # Load window design
        uic.loadUi('ui/mainwindow.ui', self)

        # Set step duration (in s)
        self.stepDuration = stepDuration_
        # Must be converted into ms to get into the box
        self.stepDurationBox.setValue(self.stepDuration*1e3)

        # Remove aliasing
        self.graphicsView.setRenderHint(QtGui.QPainter.Antialiasing);
        self.graphicsView.setCacheMode(QtGui.QGraphicsView.CacheBackground);

        # Set scale factor (no unit)
        self.scaleFactor = 0.5
        self.graphicsView.scale(self.scaleFactor, self.scaleFactor)

        # Define world dimensions (in m)
        self.worldLength = 4;
        self.worldHeight = 2;

        # Create a new world
        self.world = World(self, self.stepDuration, self.worldLength, self.worldHeight)

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
        self.stepDurationBox.editingFinished.connect(self.updateStepDuration)
        # Max steps
        self.spinBox_2.editingFinished.connect(self.updateMaxSteps)

        # Create a timer to handle time
        self.timer = QtCore.QTimer(self)

        # Connect timer trigger signal to stop
        # Connect timer trigger signal to world advance
        self.timer.timeout.connect(self.stop)
        self.timer.timeout.connect(self.world.advance)

        self.maxSteps = 500
        # Update maximum steps max value
        self.spinBox_2.setMaximum(1000)
        # Update value in associated spin box
        self.spinBox_2.setValue(self.maxSteps)

        # Current number of steps
        self.currentSteps = 0

    def updateMaxSteps(self, ):
        self.maxSteps = self.spinBox_2.value()

    def updateStepDuration(self, ):
        """
        """
        # Get changed step duration (given in ms in the box)
        # -> Must be converted into s
        self.stepDuration = self.stepDurationBox.value()*1e-3
        # Update world step duration (in s)
        self.world.updateStepDuration(self.stepDuration)
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
        # The timer class needs a duration in ms
        # -> need to convert s into ms
        self.timer.start(self.stepDuration*1e3);

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

    # Create a robotnik simulator with a default step duration of 10ms
    robotnik = Robotnik(10*1e-3)

    # Create a differential drive robot
    # Wheel radius = 2.1cm
    # In-between wheel base length = 8.85cm
    woggle = Woggle("woggle", 0.021, 0.0885)

    shape = Shape("shape")

    # Add the objects to the simulator
    robotnik.addRobot(woggle, QtCore.QPointF(0, 0))

    # robotnik.addFurniture(shape, QtCore.QPointF(-400, 200))

    # Exit
    sys.exit(app.exec_())
