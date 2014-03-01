#!/usr/bin/python
# coding: utf-8

import sys, os
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

    # Step duration of 20ms (min possible for Qt framework)
    const.stepDuration = 20*1e-3 # in s

    def __init__(self, ):
        # Call parent constructor
        super(Robotnik, self).__init__()

        # Load window design
        uic.loadUi('ui/mainwindow.ui', self)

        # Create a timer to handle time
        self.timer = QtCore.QTimer(self)

        # Configure
        self.configureMenuBar()
        self.configureToolBar()
        self.configureSimu()
        self.configureWorld()
        self.configureView()
        self.configureWindow()
        self.connectSlots()

        # Create XML file dialog
        self._worldDialog = QtGui.QFileDialog(self,
                                "Select World File",
                                "worlds",
                                "WorldFile (*.xml)")
        self._worldDialog.setDirectory(QtCore.QDir.currentPath() + os.sep + 'templates')
        self._worldDialog.setAcceptMode(QtGui.QFileDialog.AcceptOpen)
        self._worldDialog.setFileMode(QtGui.QFileDialog.ExistingFile)

    def configureMenuBar(self, ):
        """Configure the menubar.
        """
        self.setMenuBar(self.menuBar)

        # File
        file_menu = self.menuBar.addMenu("&File")
        file_menu.addAction(self.action_Open_World)
        file_menu.addSeparator()
        file_menu.addAction(self.action_Exit)

        # View
        view_menu = self.menuBar.addMenu("&View")
        view_menu.addAction(self.action_Zoom_World)
        view_menu.addAction(self.action_Zoom_Robot)
        view_menu.addSeparator()
        view_menu.addAction(self.action_Sensors_Robot)
        view_menu.addAction(self.action_Tracks_Robot)
        view_menu.addAction(self.action_Ghost_Mode)

        # Simu
        run_menu = self.menuBar.addMenu("&Simu")
        run_menu.addAction(self.action_Restart)
        run_menu.addAction(self.action_Play_Pause)
        run_menu.addAction(self.action_Step)

        help_menu = self.menuBar.addMenu("&Help")
        help_menu.addAction(self.action_About)

    def configureToolBar(self, ):
        """Configure the toolbar.
        """

        # Add open world action
        self.mainToolBar.addAction(self.action_Open_World)

        # Add separator
        self.mainToolBar.addSeparator()

        # Add restart action
        self.mainToolBar.addAction(self.action_Restart)
        # Add play action
        self.mainToolBar.addAction(self.action_Play_Pause)
        # Add step action
        self.mainToolBar.addAction(self.action_Step)

        # Add simulation speed toolbar
        self.speed_Slider = QtGui.QSlider(QtCore.Qt.Horizontal,self)
        self.speed_Slider.setTickPosition(QtGui.QSlider.NoTicks)
        self.speed_Slider.setToolTip("Adjust simulation speed factor")
        self.speed_Slider.setStatusTip("Adjust simulation speed factor")
        self.speed_Slider.setMaximumWidth(100)
        self.speed_Slider.setRange(1,5)
        self.speed_Slider.setValue(1)
        self.speed_Slider.setEnabled(True)
        self.mainToolBar.addWidget(self.speed_Slider)
        self.speed_Label = QtGui.QLabel(" Speed: 1.0x ",self)
        self.speed_Label.setToolTip("Current Speed factor")
        self.mainToolBar.addWidget(self.speed_Label)

        # Add separator
        self.mainToolBar.addSeparator()

        # Add show robots sensors
        self.mainToolBar.addAction(self.action_Sensors_Robot)
        # Add show robots tracks
        self.mainToolBar.addAction(self.action_Tracks_Robot)
        # Add ghost mode
        self.mainToolBar.addAction(self.action_Ghost_Mode)

        # Add separator
        self.mainToolBar.addSeparator()

        # Add zoom world
        self.mainToolBar.addAction(self.action_Zoom_World)
        # Add zoom master robot
        self.mainToolBar.addAction(self.action_Zoom_Robot)
        # Add robot zoom slider
        self.zoom_Slider = QtGui.QSlider(QtCore.Qt.Horizontal,self)
        self.zoom_Slider.setTickPosition(QtGui.QSlider.NoTicks)
        self.zoom_Slider.setToolTip("Adjust zoom")
        self.zoom_Slider.setStatusTip("Zoom in/out on robot")
        self.zoom_Slider.setMaximumWidth(150)
        self.zoom_Slider.setRange(-150,100)
        self.zoom_Slider.setValue(0)
        self.zoom_Slider.setEnabled(True)
        self.mainToolBar.addWidget(self.zoom_Slider)
        self.zoom_Label = QtGui.QLabel(" Zoom: 1.0x ",self)
        self.zoom_Label.setToolTip("Current zoom factor")
        self.mainToolBar.addWidget(self.zoom_Label)

    def configureSimu(self, ):
        """Configures the simulation.
        """
        self._currentSteps = 0

    def configureWorld(self, ):
        """Configures the world.
        """
        # Create a new world
        self._world = World(self)
        # Tell the world to auto-construct
        self._world.readConfigurationFile('templates/labyrinth_small.xml')

    def configureView(self, ):
        """Configures the view slot.
        """
        # Remove aliasing and smooth transformations
        self._worldView.setRenderHints(QtGui.QPainter.Antialiasing |
                                        QtGui.QPainter.SmoothPixmapTransform);
        # Enable drag mode on mouse click
        self._worldView.setDragMode(QtGui.QGraphicsView.ScrollHandDrag);

        # Attach the world to the current view
        self._worldView.setScene(self._world)

        # Focus on the robot by default
        self._worldView.scaleOnRobot()

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

        # Open World
        self.action_Open_World.triggered.connect(self.onOpenWorld)

        # Play/Pause
        self.action_Play_Pause.triggered.connect(self.startPause)
        # Restart
        self.action_Restart.triggered.connect(self.restart)
        # Step
        self.action_Step.triggered.connect(self.step)

        # Connect simulation speed factor slider
        self.speed_Slider.valueChanged[int].connect(self.setSpeedFactor)

        # Connect timer trigger signal to world update method
        self.timer.timeout.connect(self._world.update)
        self.timer.timeout.connect(self.updateTime)

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

        # Connect exit
        self.action_Exit.triggered.connect(self.close)

        # About
        self.action_About.triggered.connect(self.about)

    @QtCore.pyqtSlot()
    def about(self):
        QtGui.QMessageBox.about(self,"About Robotnik",
        """<b>Robotnik (Qt)</b><br>
        Robot simulator<br>
        &copy; Robotnik Team
        """)

    @QtCore.pyqtSlot()
    def onOpenWorld(self, ):
        """Action to perform when the XML world file dialog is invocated.
        """
        # First, if the simulation is running, stop it
        if self._world.isRunning():
            self.startPause()

        # Then load the world from the configuration file
        if self._worldDialog.exec_():
            self.loadWorld(self._worldDialog.selectedFiles()[0])

    @QtCore.pyqtSlot(int)
    def setSpeedFactor(self, value_):
        """Sets the simulation speed factor
        """
        # Update slider label
        self.speed_Label.setText(" speed: %.1fx "%(value_))

        # Update world speed factor
        self._world.setSpeedFactor(value_)

    @QtCore.pyqtSlot()
    def step(self, ):
        """Step the simulation.
        """
        # The timer class needs a duration in ms
        # -> Convert s into ms
        self.timer.singleShot(const.stepDuration*1e3, self._world.advance)

    @QtCore.pyqtSlot()
    def updateTime(self, ):
        """Update the current time.
        """
        self._currentSteps = self._currentSteps + const.stepDuration

    @QtCore.pyqtSlot()
    def startPause(self, ):
        """Starts or pauses the simulation.
        """
        if self._world.isRunning():
            # Stop the timer
            self.timer.stop()
            # Change the icon
            self.action_Play_Pause.setIcon(QtGui.QIcon("ui/icons/silk/control_play_blue.png"))
        else:
            # The timer class needs a duration in ms
            # -> Convert s into ms
            self.timer.start(const.stepDuration*1e3)
            # Change the icon
            self.action_Play_Pause.setIcon(QtGui.QIcon("ui/icons/silk/control_pause_blue.png"))

        self._world.toggleRunning()

    @QtCore.pyqtSlot()
    def restart(self, ):
        """Restarts the simulation.
        """
        # Restart the current number of steps
        self._currentSteps = 0
        # Stop the timer
        self.timer.stop()

        # Put robots at there initial position
        for robot in self._world.getRobots():
            robot.restart()

        # Refocus the view on the master robot
        if self._world.isZoomOnRobot():
            self._worldView.focusOnRobot()

        # Change the play/pause icon
        self.action_Play_Pause.setIcon(QtGui.QIcon("ui/icons/silk/control_play_blue.png"))
        # Set the world to the not running state
        self._world.setRunning(False)

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
        self._world.setZoomOnRobot(False)
        self._worldView.focusOnWorld()

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
        self._world.setZoomOnRobot(True)
        self._worldView.scaleOnRobot()

    @QtCore.pyqtSlot(int)
    def setRobotZoomLevel(self, value_):
        """Sets the master robot zoom level.
        """
        zoom = 5.0**(value_/100.0)
        for robot in self._world.getRobots():
            if robot.isMasterRobot():
                robot.setZoom(zoom)

        self.zoom_Label.setText(" Zoom: %.1fx "%(zoom))

        # Update scale on robot
        self._worldView.scaleOnRobot()

    @QtCore.pyqtSlot()
    def showProxSensors(self, ):
        """Shows the robots proximity sensors
        """
        # Toggle the robot sensors display
        self._world.toggleRobotSensors()

        # Trigger a view update
        self._worldView.update()

    @QtCore.pyqtSlot()
    def showRobotTracks(self, ):
        """Shows the robots tracks
        """
        # Toggle the robot tracks display
        self._world.toggleRobotTracks()

        # Trigger a view update
        self._worldView.update()

    @QtCore.pyqtSlot()
    def enableGhostMode(self, ):
        """Enables the robots ghost mode.
        """
        # Toggle the ghost mode enabling
        self._world.toggleGhostMode()

    def center(self, ):
        """Centers the window on screen.
        """
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def loadWorld(self,filename_):
        """Load a new world according to an existing XML file.
        """
        # Check the existence of the file
        if not os.path.exists(filename_):
            print "Cannot open file {}".format(filename_)
            return

        # Check the configuration file
        self._world.readConfigurationFile(filename_)

if __name__ == '__main__':
    # Create a Qt application
    app = QtGui.QApplication(sys.argv)
    robotnik = Robotnik()
    # Exit
    sys.exit(app.exec_())
