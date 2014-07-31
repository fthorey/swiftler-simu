#!/usr/bin/python
# coding: utf-8

from math import pi, degrees, radians, cos, sin
from robots.robot import Robot
from sensors.irsensor import IRSensor
from sensors.wheelencoder import WheelEncoder
from supervisors.unicyclesupervisor import UnicycleSupervisor
from dynamics.differential import DifferentialDrive
from utils import helpers
from PyQt4 import QtGui, QtCore

class Unicycle(Robot):
    """ The Unicycle class handles a unicycle robot called Unicycle
    """

    def __init__(self, name_, brush_, infoFile_):
        # Call parent constructor
        super(Unicycle, self).__init__(name_=name_, brush_=brush_, infoFile_=infoFile_)

        # Add an encoder to each wheel
        self._leftWheelEncoder = WheelEncoder(self._info["encoders"]["ticksPerRev"])
        self._rightWheelEncoder = WheelEncoder(self._info["encoders"]["ticksPerRev"])

        # Add sharp sensors on the robot
        for p in self._info["sensors"]["ir"]["positions"]:
            self.addProxSensor(IRSensor(p, self._info["sensors"]["ir"]["rmin"],
                                        self._info["sensors"]["ir"]["rmax"],
                                        self._info["sensors"]["ir"]["phi"]))

        # The unicycle robot follows the differential drive dynamic
        self.setDynamics(DifferentialDrive(self))

        # Retrieve info about supervisor and planner
        supervisor_type = self._info['supervisor']["type"]
        planner_type = self._info['planner']["type"]
        sup_class = helpers.load_by_name(str(supervisor_type),'supervisors')
        # Get supervisor configuration file
        sup_conf = self._info["supervisor"]["conf-file"]
        # Get robot planner class
        plan_class = helpers.load_by_name(str(planner_type),'planners')
        # Get planner configuration file
        plan_conf = self._info["planner"]["conf-file"]

        # The supervisor is attached to the robot
        self.setSupervisor(sup_class(infoFile_, sup_conf, plan_class, plan_conf))

    def info(self):
        """Return the robot information structure.
        """
        # Update readings from sensors
        self._info["sensors"]["ir"]["readings"] = [s.reading() for s in self._proxSensors]
        return self._info

    def leftRevolutions(self, ):
        """Return the number of revolutions of the left wheel.
        """
        return self.info()["wheels"]["left"]["rev"]

    def rightRevolutions(self, ):
        """Return the number of revolutions of the right wheel.
        """
        return self.info()["wheels"]["right"]["rev"]

    def setLeftRevolutions(self, rev_):
        """Set the number of revolutions of the left wheel.
        """
        self.info()["wheels"]["left"]["rev"] = rev_

    def setRightRevolutions(self, rev_):
        """Set the number of revolutions of the right wheel.
        """
        self.info()["wheels"]["right"]["rev"] = rev_

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
        self.info()["wheels"]["left"]["speed"] = speed_

    def setRightWheelSpeed(self, speed_):
        """Set the current right wheel speed (in m/s).
        """
        self.info()["wheels"]["right"]["speed"] = speed_

    def getLeftWheelSpeed(self, ):
        """Return the current left wheel speed (in m/s).
        """
        return self.info()["wheels"]["left"]["speed"]

    def getRightWheelSpeed(self, ):
        """Return the current right wheel speed (in m/s).
        """
        return self.info()["wheels"]["right"]["speed"]

    def setWheelSpeeds(self, vel_l, vel_r):
        """Set the speed of both wheels (in m/s).
        """
        self.info()["wheels"]["left"]["speed"] = vel_l
        self.info()["wheels"]["right"]["speed"] = vel_r

    def getSpeed(self, ):
        """Get current speed (in m/s).
        """
        v, w = self.dynamics.diff2Uni(self.info()["wheels"]["left"]["speed"],
                                      self.info()["wheels"]["right"]["speed"])
        return v

    def paint(self, painter, option, widget):
        """Paint the robot on screen
        """
        # Paint body (always grey)
        painter.setBrush(QtGui.QColor("light grey"))
        painter.setPen(QtCore.Qt.SolidLine)
        points = [QtCore.QPointF(p[0], p[1]) for p in self._envelope]
        painter.drawPolygon(QtGui.QPolygonF(points))

        bodyX = (-self.info()["wheels"]["baseLength"]/2)
        bodyY = (-self.info()["wheels"]["baseLength"]/2)
        bodyW = self.info()["wheels"]["baseLength"]
        bodyH = self.info()["wheels"]["baseLength"]

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
