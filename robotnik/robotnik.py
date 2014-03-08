#!/usr/bin/python
# coding: utf-8

import sys, os
from world.world import World
from utils import const
import ui.icons

# Handle Ctrl-C
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

from PyQt4 import QtGui, QtCore, uic

class Robotnik(QtGui.QMainWindow):
    """ The Robotnik class is the main container for the simulator.
    """

    # Step duration of 20ms
    const.stepDuration = 20*1e-3 # in s

    def __init__(self, ):
        # Call parent constructor
        super(Robotnik, self).__init__()

        # Load window design
        uic.loadUi('ui/mainwindow.ui', self)

        # Set window title
        self.setWindowTitle("Robotnik Simulator")

        # Create a timer to handle time
        self.timer = QtCore.QTimer(self)

        # Default file name
        self._filename = 'templates/labyrinth_small.xml'

        # Configure
        # Status bar
        self.configureStatusLabel()
        self.setStatusTips() # (Missing in QtCreator)
        # Menu bar
        self.configureMenuBar()
        # Tool bar
        self.configureToolBar()
        # World
        self.configureWorld()
        # World view
        self.configureView()
        # Simu
        self.configureSimu()
        # Window
        self.configureWindow()
        # Slots
        self.connectSlots()

        # Create XML file dialog
        self._worldDialog = QtGui.QFileDialog(self,
                                              "Select World File",
                                              "worlds",
                                              "WorldFile (*.xml)")
        self._worldDialog.setDirectory(QtCore.QDir.currentPath() + os.sep + 'templates')
        self._worldDialog.setAcceptMode(QtGui.QFileDialog.AcceptOpen)
        self._worldDialog.setFileMode(QtGui.QFileDialog.ExistingFile)

    def configureStatusLabel(self, ):
        # By default the status label is empty
        self._statusLabel = QtGui.QLabel("", self.statusBar)
        self._statusLabel.setFrameShape(QtGui.QFrame.NoFrame)
        self.statusBar.addWidget(self._statusLabel)

    def setStatusTips(self, ):
        """Set status tips (missing in QtCreator).
        """
        self.action_Open_World.setStatusTip("Open a new world")
        self.action_Restart.setStatusTip("Restart the simulation")
        self.action_Play_Pause.setStatusTip("Play/pause the simulation")
        self.action_Step.setStatusTip("Execute one step of simulation")
        self.action_Sensors_Robot.setStatusTip("Show/Hide robots sensors")
        self.action_Tracks_Robot.setStatusTip("Show/Hide robots tracks")
        self.action_Ghost_Mode.setStatusTip("Enable/Disable ghost mode")
        self.action_Zoom_World.setStatusTip("Show the entire world")
        self.action_Zoom_Robot.setStatusTip("Follow the master robot")
        self.action_Show_Supervisors.setStatusTip("Show/Hide the supervisors infos")

    def configureMenuBar(self, ):
        """Configure the menubar.
        """
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
        view_menu.addAction(self.action_Show_Supervisors)

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
        self.speed_Slider.setValue(2)
        self.speed_Slider.setEnabled(True)
        self.mainToolBar.addWidget(self.speed_Slider)
        self.speed_Label = QtGui.QLabel(" Speed: 2.0x ",self)
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
        # Add show supervisors infos
        self.mainToolBar.addAction(self.action_Show_Supervisors)

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
        self._world.setCurrentSteps(0)

        self.pause()

    def configureWorld(self, ):
        """Configures the world.
        """
        # Create a new world
        self._world = World(self)

        # Fill the world with data from the configuration file
        self._world.readConfigurationFile(self._filename)

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

        # Connect show supervisors info
        self.action_Show_Supervisors.triggered.connect(self.showSupervisors)

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
        self.speed_Label.setText(" Speed: %.1fx "%(value_))

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

        # Update the status bar
        t = self._world.currentSteps() # (in s)
        minutes = int(t//60)
        self._statusLabel.setText(
            "Simulation running: {:02d}:{:04.1f}".format(minutes,t - minutes*60))

    def pause(self, ):
        """Pause the simulation.
        """
        self._world.setRunning(False)
        # Stop the timer
        self.timer.stop()
        # Change the icon
        self.action_Play_Pause.setIcon(QtGui.QIcon("ui/icons/silk/control_play_blue.png"))

        # Update the status bar
        t = self._world.currentSteps() # (in s)
        minutes = int(t//60)
        self._statusLabel.setText(
            "Simulation paused: {:02d}:{:04.1f}".format(minutes,t - minutes*60))

    def start(self, ):
        """Start the simulation.
        """
        self._world.setRunning(True)
        # The timer class needs a duration in ms
        # -> Convert s into ms
        self.timer.start(const.stepDuration*1e3)
        # Change the icon
        self.action_Play_Pause.setIcon(QtGui.QIcon("ui/icons/silk/control_pause_blue.png"))

    @QtCore.pyqtSlot()
    def startPause(self, ):
        """Starts or pauses the simulation.
        """
        if self._world.isRunning():
            self.pause()
        else:
            self.start()

    @QtCore.pyqtSlot()
    def restart(self, ):
        """Restarts the simulation.
        """
        # Restart the current number of steps
        self._world.setCurrentSteps(0)

        # Pause the world
        self.pause()

        # Tell the world to auto-construct
        self._world.readConfigurationFile(self._filename)

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
        for robot in self._world.robots():
            if robot.isMasterRobot():
                robot.setZoom(zoom)

        self.zoom_Label.setText(" Zoom: %.1fx "%(zoom))

        # Update scale on robot
        self._worldView.scaleOnRobot()

    @QtCore.pyqtSlot()
    def showProxSensors(self, ):
        """Shows the robots proximity sensors.
        """
        # Toggle the robot sensors display
        self._world.toggleRobotSensors()

        # Trigger a view update
        self._worldView.update()

    @QtCore.pyqtSlot()
    def showRobotTracks(self, ):
        """Shows the robots tracks.
        """
        # Toggle the robot tracks display
        self._world.toggleRobotTracks()

        # Trigger an update of the scene
        self._worldView.updateScene([self._worldView.sceneRect()])

    @QtCore.pyqtSlot()
    def enableGhostMode(self, ):
        """Enables the robots ghost mode.
        """
        # Toggle the ghost mode enabling
        self._world.toggleGhostMode()

    @QtCore.pyqtSlot()
    def showSupervisors(self, ):
        """Show the robots supervisors infos.
        """
        # Toggle the supervisors info display
        self._world.toggleShowSupervisors()

        # Trigger a view update
        self._worldView.updateScene([self._world.sceneRect()])

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
        self._filename = filename_
        self._world.readConfigurationFile(self._filename)

if __name__ == '__main__':
    # Create a Qt application
    app = QtGui.QApplication(sys.argv)
    robotnik = Robotnik()
    # Show the view on screen
    robotnik.show()
    # Exit
    sys.exit(app.exec_())
