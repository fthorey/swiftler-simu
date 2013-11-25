#!/usr/bin/python
# coding: utf-8

import sys
from physics.world import World
from robots.woggle import Woggle
from common.shape import *
from common import const

from PyQt4 import QtGui, QtCore

class Robotnik(QtGui.QMainWindow):
    """ Robotnik class is the main container for the simulator
    """

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

        # Create a view to vizualize the graphic scene
        view = QtGui.QGraphicsView(self.world);

        # Remove aliasing
        view.setRenderHint(QtGui.QPainter.Antialiasing);
        view.setCacheMode(QtGui.QGraphicsView.CacheBackground);

        # Place the view of the graphic scene in the center
        self.setCentralWidget(view);

        # Set the main window size
        self.resize(800, 600)

        # Center the main window
        self.center()

        # Show the view on screen
        self.show()

        # Set a timer to handle time
        timer = QtCore.QTimer(self)

        # Connect timer trigger signal to world advance method
        timer.timeout.connect(self.world.advance)

        # Get a frame rate of ~100fps
        timer.start(const.stepDuration);

    # Center the main window
    def center(self, ):
        """
        """
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # Add an object
    def addObject(self, object_):
        """
        """
        self.world.addObject(object_)

if __name__ == '__main__':
    # Create a Qt application
    app = QtGui.QApplication([])

    # Create a robotnik simulator with a step duration of 10ms
    robotnik = Robotnik(10)

    # Create a differential drive robot
    woggle = Woggle("woggle", 0.021, 0.0885)

    # Add the objects to the simulator
    robotnik.addObject(woggle)

    # Exit
    sys.exit(app.exec_())
