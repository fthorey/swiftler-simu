#!/usr/bin/python
# coding: utf-8

import sys
from math import pi
from world.world import World
from robots.woggle import Woggle
from shape.shape import Shape
from utils import const
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

    def __init__(self, ):
        """
        """
        # Call parent constructor
        super(Robotnik, self).__init__()

        # Load window design
        uic.loadUi('ui/mainwindow.ui', self)

        # Create a timer to handle time
        self.timer = QtCore.QTimer(self)

        # Configure
        self.configureSimu()
        self.configureView()
        self.configureWorld()
        self.configureWindow()
        self.connectSlots()

    def configureWorld(self, ):
        """
        """
        # Define world dimensions (in m)
        self.worldSize = 4; # in m
        # Create a new world
        self.world = World(self, self.stepDuration, self.worldSize)
        # Attach the world to the current view
        self.graphicsView.setScene(self.world)
        # Tell the world to auto-construct
        self.world.autoConstruct()

    def configureView(self, ):
        """
        """
        # Remove aliasing
        self.graphicsView.setRenderHints(QtGui.QPainter.Antialiasing |
                                        QtGui.QPainter.SmoothPixmapTransform);
        self.graphicsView.setDragMode(QtGui.QGraphicsView.ScrollHandDrag);

        # Set default scale factor
        scaleFactor = 0.2
        self.graphicsView.scale(scaleFactor, scaleFactor)

    def configureWindow(self, ):
        """
        """
        # Center the main window
        self.center()
        # Show the view on screen
        self.show()

    def configureSimu(self, ):
        """
        """
        # The default step duration is set to 10ms
        self.stepDuration = 10*1e-3
        # Must be converted into ms to get into the box
        self.stepDurationBox.setValue(self.stepDuration*1e3)

        self.maxSteps = 500
        # Update maximum steps max value
        self.stepsNumberBox.setMaximum(1000)
        # Update value in associated spin box
        self.stepsNumberBox.setValue(self.maxSteps)

        # Current number of steps
        self.currentSteps = 0

    def connectSlots(self, ):
        """
        """
        # Play
        self.action_Play.triggered.connect(self.start)
        # Pause
        self.action_Pause.triggered.connect(self.pause)
        # Restart
        self.action_Restart.triggered.connect(self.restart)
        # Step duration
        self.stepDurationBox.editingFinished.connect(self.updateStepDuration)
        # Max steps
        self.stepsNumberBox.editingFinished.connect(self.updateMaxSteps)

        # Connect timer trigger signal to stop function
        # Connect timer trigger signal to world advance function
        self.timer.timeout.connect(self.stop)
        self.timer.timeout.connect(self.world.advance)

    def updateMaxSteps(self, ):
        self.maxSteps = self.stepsNumberBox.value()

    def updateStepDuration(self, ):
        """
        """
        # Get changed step duration (given in ms in the box)
        # -> Must be converted into s
        self.stepDuration = self.stepDurationBox.value()*1e-3
        # Update world step duration (in s)
        self.world.updateStepDuration(self.stepDuration)

    def restart(self, ):
        """
        """
        # Stop the timer
        self.currentSteps = 0
        self.timer.stop()

        # Put robots at there initial position
        for robot in self.world.getRobots():
            robot.restart()

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
        # -> Convert s into ms
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

if __name__ == '__main__':
    # Create a Qt application
    app = QtGui.QApplication([])
    robotnik = Robotnik()
    # Exit
    sys.exit(app.exec_())
