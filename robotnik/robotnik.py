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

    def __init__(self, stepDuration_):
        """
        """
        # Call parent constructor
        super(Robotnik, self).__init__()

        # Load window design
        uic.loadUi('ui/mainwindow.ui', self)

        # Set step duration
        const.stepDuration = stepDuration_

        # Get the view
        view = self.centralWidget.findChild(QtGui.QGraphicsView, 'graphicsView')

        # Remove aliasing
        view.setRenderHint(QtGui.QPainter.Antialiasing);
        view.setCacheMode(QtGui.QGraphicsView.CacheBackground);

        # Create a new world
        self.world = World(self)
        self.world.setSceneRect(-300, -300, 600, 600);

        # Attach the world to the view
        view.setScene(self.world)

        # Center the main window
        self.center()

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

    # Add a furniture in the world
    def addFurniture(self, furniture_, position_):
        """
        """
        self.world.addFurniture(furniture_, position_)

    # Add a robot in the world
    def addRobot(self, robot_, position_):
        """
        """
        self.world.addRobot(robot_, position_)

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

    # Random shape
    shape = Shape("shape")
    robotnik.addFurniture(shape, QtCore.QPointF(-200, -150))

    # Advance the simulation for some steps (1000 * 10ms = 10s)
    robotnik.step(1000)

    # Exit
    sys.exit(app.exec_())
