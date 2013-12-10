#!/usr/bin/python
# coding: utf-8

import sys
from math import pi
from physics.world import World
from robots.woggle import Woggle
from common.shape import *
from common import const

from PyQt4 import QtGui, QtCore

class Robotnik(QtGui.QMainWindow):
    """ Robotnik class is the main container for the simulator
    """

    # Conversion factor between pixels and meters
    const.pix2m = 0.0002645833333333
    const.m2pix = 3779.527559055

    # Distance scale factor
    const.scaleFactor = 1.0/2.5

    def __init__(self, stepDuration_):
        """
        """
        # Call parent constructor
        super(Robotnik, self).__init__()

        # Set main window object name
        self.setObjectName("Robotnik");

        # Set window title
        self.setWindowTitle("Robotnik");

        # Set step duration
        const.stepDuration = stepDuration_

        # Create a new world
        self.world = World(self)
        self.world.setSceneRect(-300, -300, 600, 600);

        # Create a view to vizualize the graphic scene
        view = QtGui.QGraphicsView(self.world);

        # Remove aliasing
        view.setRenderHint(QtGui.QPainter.Antialiasing);
        view.setCacheMode(QtGui.QGraphicsView.CacheBackground);

        # Place the view of the graphic scene in the center
        self.setCentralWidget(view);

        # Set the main window size
        self.resize(1*const.m2pix*const.scaleFactor, 0.5*const.m2pix*const.scaleFactor)

        # Center the main window
        self.center()

        # Get screen geometry
        screen = QtGui.QDesktopWidget().screenGeometry()

        # Save screen width and height
        const.screenWidth = screen.width() * const.pix2m
        const.screenHeight = screen.height() * const.pix2m

        # Show the view on screen
        self.show()

        # Current number of steps
        self.steps = 0
        self.maxsteps = 0

        # Set a timer to handle time
        self.timer = QtCore.QTimer(self)

        # Connect timer trigger signal to world advance method
        self.timer.timeout.connect(self.world.advance)
        # COnnect timer to step method to check end of time steps
        self.timer.timeout.connect(self.stop)

    def stop(self, ):
        """
        """
        self.steps = self.steps + 1

        if self.steps == self.maxsteps:
            self.timer.stop()

    def step(self, steps_):
        """
        """
        self.timer.start(const.stepDuration);
        self.steps = 0
        self.maxsteps = steps_

    # Center the main window
    def center(self, ):
        """
        """
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # Add an object
    def addObject(self, object_, position_):
        """
        """
        self.world.addObject(object_, position_)

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
    robotnik.addObject(woggle, QtCore.QPointF(0, 0))

    # Random shape
    shape = Shape("shape")
    robotnik.addObject(shape, QtCore.QPointF(-200, -150))

    # Advance the simulation for some steps (1000 * 10ms = 10s)
    robotnik.step(1000)

    # Exit
    sys.exit(app.exec_())
