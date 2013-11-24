#!/usr/bin/python
# coding: utf-8

import sys
from physics.world import World
from robots.robot import Robot
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
        view.resize(400, 300);

        # Place the view of the graphic scene in the center
        self.setCentralWidget(view);

        # Set the main window size
        self.setGeometry(300, 300, 250, 250)

        # Center the main window
        self.center()

        # Show the view on screen
        self.show()

        # Set a timer to handle time
        timer = QtCore.QTimer(self)

        # Connect timer trigger signal to world advance method
        timer.timeout.connect(self.world.advance)

        # Get a frame rate of ~30fps
        timer.start(1000 / 33);

    # Center the main window
    def center(self, ):
        """
        """
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # Add a robot
    def addRobot(self, robot_):
        """
        """
        self.world.addRobot(robot_)

if __name__ == '__main__':
    # Create a Qt application
    app = QtGui.QApplication([])

    # Create a robotnik simulator with a step duration of 1s
    robotnik = Robotnik(1)

    # Create a differential drive robot
    robot = Robot("Robot1", 0.021, 0.0885)

    # Add the robot to the simulator
    robotnik.addRobot(robot)

    # Exit
    sys.exit(app.exec_())
