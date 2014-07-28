#!/usr/bin/python
# coding: utf-8

from math import pi, degrees, radians, cos, sin
from utils.struct import Struct
from robots.robot import Robot
from sensors.woggleirsensor import WoggleIRSensor
from sensors.wheelencoder import WheelEncoder
from supervisors.wogglesupervisor import WoggleSupervisor
from dynamics.differential import DifferentialDrive
from PyQt4 import QtGui, QtCore

class Woggle(Robot):
    """ The Woggle class handles a unicycle robot called Woggle
    """

    def __init__(self, name_, supervisorClass_, pos_, brush_, infoFile_):
        # Call parent constructor
        super(Woggle, self).__init__(name_, pos_, brush_, infoFile_)

        # TODO: REMOVE THIS
        self._info2 = {}
        self._info2.update(self._info)

        # Fill-in the state informations
        self._info = Struct()
        # Wheels
        self._info.wheels = Struct()
        self._info.wheels.radius = self._info2["wheels"]["radius"]
        self._info.wheels.baseLength = self._info2["wheels"]["baseLength"]
        self._info.wheels.ticksPerRev = self._info2["encoders"]["ticksPerRev"]
        self._info.wheels.leftTicks = self._info2["encoders"]["leftTicks"]
        self._info.wheels.rightTicks = self._info2["encoders"]["rightTicks"]
        # Proximity sensors
        self._info.sensors = Struct()
        self._info.sensors.rmin = self._info2["sensors"]["ir"]["rmin"]
        self._info.sensors.rmax = self._info2["sensors"]["ir"]["rmax"]
        self._info.sensors.phi = self._info2["sensors"]["ir"]["phi"]
        self._info.sensors.toCenter = self._info2["wheels"]["baseLength"]/2 + 0.01

        # Current speed of each wheel (rad/s)
        self._leftWheelSpeed = 0
        self._rightWheelSpeed = 0

        # Current number of revolution of each wheel
        self._leftRevolutions = 0
        self._rightRevolutions = 0

        # Add a wheel encoder to each wheel
        self._leftWheelEncoder = WheelEncoder(self._info2["encoders"]["ticksPerRev"])
        self._rightWheelEncoder = WheelEncoder(self._info2["encoders"]["ticksPerRev"])

        # Position of the sharp sensors
        self._proxSensorsPos = self._info2["sensors"]["ir"]["positions"]

        # Add the sensors to the robot
        rmin = self._info2["sensors"]["ir"]["rmin"]
        rmax = self._info2["sensors"]["ir"]["rmax"]
        phi = self._info2["sensors"]["ir"]["phi"]
        for p in self._proxSensorsPos:
            self.addProxSensor(WoggleIRSensor(p, rmin, rmax, phi))

        # Add sensors instance to the information
        # -> Mostly needed to get the correct transformation matrix
        # to world/robot frame.
        self._info2["sensors"]["ir"]["insts"] = self._proxSensors
        self._info.sensors.insts = self._info2["sensors"]["ir"]["insts"]

        # Initialize the IR sensors readings
        self._info2["sensors"]["ir"]["readings"] = [s.reading() for s in self._proxSensors]
        self._info.sensors.readings = self._info2["sensors"]["ir"]["readings"]

        #------------------------------------------------------------------#
        # Dynamics and supervisor must be set after all robot configurations
        # and structures are well known
        #------------------------------------------------------------------#

        # The Woggle robot follows the differential drive dynamic
        self.setDynamics(DifferentialDrive(self))

        # The supervisor is attached to the robot
        self.setSupervisor(supervisorClass_(pos_, self._info))

    def info(self):
        """Return the robot information structure.
        """
        # Measures current reading of the sensors
        self._info2["sensors"]["ir"]["readings"] = [s.reading() for s in self._proxSensors]
        self._info.sensors.readings = self._info2["sensors"]["ir"]["readings"]
        return self._info

    def info2(self):
        """Return the robot information structure.
        """
        self._info2["sensors"]["ir"]["readings"] = [s.reading() for s in self._proxSensors]
        return self._info2

    def leftRevolutions(self, ):
        """Return the number of revolutions of the left wheel.
        """
        return self._leftRevolutions

    def rightRevolutions(self, ):
        """Return the number of revolutions of the right wheel.
        """
        return self._rightRevolutions

    def setLeftRevolutions(self, rev_):
        """Set the number of revolutions of the left wheel.
        """
        self._leftRevolutions = rev_

    def setRightRevolutions(self, rev_):
        """Set the number of revolutions of the right wheel.
        """
        self._rightRevolutions = rev_

    def leftWheelEncoder(self, ):
        """Return the left wheel encoder.
        """
        return self._leftWheelEncoder

    def rightWheelEncoder(self, ):
        """Return the right wheel encoder.
        """
        return self._rightWheelEncoder

    def setLeftWheelSpeed(self, speed_):
        """Set the current left wheel speed (in m/s).
        """
        self._leftWheelSpeed = speed_

    def setRightWheelSpeed(self, speed_):
        """Set the current right wheel speed (in m/s).
        """
        self._rightWheelSpeed = speed_

    def getLeftWheelSpeed(self, ):
        """Return the current left wheel speed (in m/s).
        """
        return self._leftWheelSpeed

    def getRightWheelSpeed(self, ):
        """Return the current right wheel speed (in m/s).
        """
        return self._rightWheelSpeed

    def setWheelSpeeds(self, vel_l, vel_r):
        """Set the speed of both wheels (in m/s).
        """
        self._leftWheelSpeed = vel_l
        self._rightWheelSpeed = vel_r

    def getSpeed(self, ):
        """Get current speed (in m/s).
        """
        v, w = self.dynamics.diff2Uni(self._leftWheelSpeed, self._rightWheelSpeed)
        return v

    def paint(self, painter, option, widget):
        """Paint the robot on screen
        """
        # Paint body (always grey)
        painter.setBrush(QtGui.QColor("light grey"))
        painter.setPen(QtCore.Qt.SolidLine)
        points = [QtCore.QPointF(p[0], p[1]) for p in self._envelope]
        painter.drawPolygon(QtGui.QPolygonF(points))

        bodyX = (-self._info2["wheels"]["baseLength"]/2)
        bodyY = (-self._info2["wheels"]["baseLength"]/2)
        bodyW = self._info2["wheels"]["baseLength"]
        bodyH = self._info2["wheels"]["baseLength"]

        # Paint identifier
        painter.setBrush(self.brush())
        painter.setPen(self.pen())
        rect = QtCore.QRectF(-bodyW/8, -bodyH/8, bodyW/4, bodyH/4)
        painter.drawEllipse(rect)

        # Paint left wheel
        wheelW = bodyW / 3
        wheelH = bodyH / 6
        lwheelX = -wheelW/2
        lwheelY = -bodyH/2 + wheelH/2
        rect = QtCore.QRectF(lwheelX, lwheelY, wheelW, wheelH)
        painter.setBrush(QtGui.QColor("black"))
        painter.drawRect(rect)

        # Paint right wheel
        rwheelX = -wheelW/2
        rwheelY = bodyH/2 - wheelH - wheelH/2
        rect = QtCore.QRectF(rwheelX, rwheelY, wheelW, wheelH)
        painter.drawRect(rect)

        if self.showSupervisors():
            self.supervisor().drawHeading(painter, option, widget)
