#!/usr/bin/python
# coding: utf-8

from math import degrees, sqrt
from utils.struct import Struct

from PyQt4 import QtCore

class Supervisor(object):
    """The supervisor class oversees the control of a single robot.
    """

    def __init__(self, pos_, robotInfo_):
        # Store information about the robot
        self._info = Struct()
        self._info.pos = pos_

    def execute(self, info_, dt_):
        """Select and execute the current controller.
        """
        raise NotImplementedError("Supervisor.execute")

    def updateStateEstimate(self, ):
        """Update the current estimation of the state of the robot position.
        """
        raise NotImplementedError("Supervisor.updateStateEstimate")

    def info(self, ):
        """Get the parameters that the current controller needs for s.
        """
        return self._info
