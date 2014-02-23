#!/usr/bin/python
# coding: utf-8

import sys
from math import pi
from world.world import World
from robots.woggle import Woggle
from utils import const
import ui.icons

# Handle Ctrl-C
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

from PyQt4 import QtGui, QtCore, uic

class Robotnik(QtGui.QMainWindow):
    """ The Robotnik class is the main container for the simulator.
    """

    # Step duration of 10ms (min possible for Qt framework)
    const.stepDuration = 10*1e-3 # in s

    def __init__(self, ):
        # Call parent constructor
        super(Robotnik, self).__init__()

        # Load window design
        uic.loadUi('ui/mainwindow.ui', self)

        # Create a timer to handle time
        self.timer = QtCore.QTimer(self)

        # Configure
        self.configureToolBar()
        self.configureSimu()
        self.configureWorld()
        self.configureView()
        self.configureWindow()
        self.connectSlots()

    def configureToolBar(self, ):
        """Configures the toolbar.
        """
        # Add robot zoom slider
        self.zoom_Slider = QtGui.QSlider(QtCore.Qt.Horizontal,self)
        self.zoom_Slider.setTickPosition(QtGui.QSlider.NoTicks)
        self.zoom_Slider.setToolTip("Adjust zoom")
        self.zoom_Slider.setStatusTip("Zoom in/out on robot")
        self.zoom_Slider.setMaximumWidth(150)
        self.zoom_Slider.setRange(-150,100)
        self.zoom_Slider.setValue(0)
        self.zoom_Slider.setEnabled(False)
        self.mainToolBar.addWidget(self.zoom_Slider)
        self.zoom_Label = QtGui.QLabel(" Zoom: 1.0x ",self)
        self.zoom_Label.setToolTip("Current zoom factor")
        self.mainToolBar.addWidget(self.zoom_Label)

    def configureSimu(self, ):
        """Configures the simulation.
        """
        # Max steps number
        self.maxSteps = 1000
        # Current number of steps
        self.currentSteps = 0

    def configureWorld(self, ):
        """Configures the world.
        """
        # Create a new world
        self.world = World(self)
        # Tell the world to auto-construct
        self.world.autoConstruct()

    def configureView(self, ):
        """Configures the view slot.
        """
        # Remove aliasing and smooth transformations
        self.worldView.setRenderHints(QtGui.QPainter.Antialiasing |
                                        QtGui.QPainter.SmoothPixmapTransform);
        # Enable drag mode on mouse click
        self.worldView.setDragMode(QtGui.QGraphicsView.ScrollHandDrag);

        # Attach the world to the current view
        self.worldView.setScene(self.world)

        # Focus on the world by default
        self.worldView.focusOnWorld()

    def configureWindow(self, ):
        """Configures the window.
        """
        # Center the main window
        self.center()
        # Show the view on screen
        self.show()

    def connectSlots(self, ):
        """Connects all slots.
        """
        # Play
        self.action_Play.triggered.connect(self.start)
        # Pause
        self.action_Pause.triggered.connect(self.pause)
        # Restart
        self.action_Restart.triggered.connect(self.restart)

        # Connect timer trigger signal to stop function
        self.timer.timeout.connect(self.stop)
        # Connect timer trigger signal to world advance function
        self.timer.timeout.connect(self.world.advance)

        # Connect zoom world
        self.action_Zoom_World.triggered.connect(self.zoomWorld)

        # Connect zoom robot
        self.action_Zoom_Robot.triggered.connect(self.zoomRobot)

        # Connect robot zoom level slider
        self.zoom_Slider.valueChanged[int].connect(self.setRobotZoomLevel)

        # Connect show sensors robots
        self.action_Sensors_Robot.triggered.connect(self.showProxSensors)

        # Connect show tracks robots
        self.action_Tracks_Robot.triggered.connect(self.showRobotTracks)

        # Connect ghost mode enabling
        self.action_Ghost_Mode.triggered.connect(self.enableGhostMode)

    @QtCore.pyqtSlot()
    def pause(self, ):
        """Pauses the simulation.
        """
        self.timer.stop()

    @QtCore.pyqtSlot()
    def stop(self, ):
        """Stops the simulation.
        """
        self.currentSteps = self.currentSteps + 1

        if self.currentSteps == self.maxSteps:
            self.timer.stop()
            self.currentSteps = 0

    @QtCore.pyqtSlot()
    def start(self, ):
        """Starts the simulation.
        """
        # The timer class needs a duration in ms
        # -> Convert s into ms
        self.timer.start(const.stepDuration*1e3);

    @QtCore.pyqtSlot()
    def restart(self, ):
        """Restarts the simulation.
        """
        # Stop the timer
        self.currentSteps = 0
        self.timer.stop()

        # Put robots at there initial position
        for robot in self.world.getRobots():
            robot.restart()

        # Refocus the view on the master robot
        if self.world.isZoomOnRobot():
            self.worldView.focusOnRobot()

    @QtCore.pyqtSlot()
    def zoomWorld(self, ):
        """Zooms on the world.
        """
        # Toggle zoom icons
        self.action_Zoom_World.setChecked(True)
        self.action_Zoom_Robot.setChecked(False)

        # Disable robot zoom slider
        self.zoom_Slider.setEnabled(False)

        # Set focus on world
        self.worldView.focusOnWorld()

    @QtCore.pyqtSlot()
    def zoomRobot(self, ):
        """Zooms on the master robot.
        """
        # Toggle zoom icons
        self.action_Zoom_World.setChecked(False)
        self.action_Zoom_Robot.setChecked(True)

        # Enable robot zoom slider
        self.zoom_Slider.setEnabled(True)

        # Set focus on robot
        self.worldView.focusOnRobot()

    @QtCore.pyqtSlot(int)
    def setRobotZoomLevel(self, value_):
        """Sets the master robot zoom level.
        """
        zoom = 5.0**(value_/100.0)
        for robot in self.world.getRobots():
            if robot.isMasterRobot():
                robot.setZoom(zoom)

        self.zoom_Label.setText(" Zoom: %.1fx "%(zoom))

        # Update focus on robot
        self.worldView.focusOnRobot()

    @QtCore.pyqtSlot()
    def showProxSensors(self, ):
        """Shows the robots proximity sensors
        """
        # Toggle the robot sensors display
        self.world.toggleRobotSensors()

        # Trigger a view update
        self.worldView.update()

    @QtCore.pyqtSlot()
    def showRobotTracks(self, ):
        """Shows the robots tracks
        """
        # Toggle the robot tracks display
        self.world.toggleRobotTracks()

        # Trigger a view update
        self.worldView.update()

    @QtCore.pyqtSlot()
    def enableGhostMode(self, ):
        """Enables the robots ghost mode.
        """
        # Toggle the ghost mode enabling
        self.world.toggleGhostMode()

    # Center the main window
    def center(self, ):
        """Centers the window on screen.
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
