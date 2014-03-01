#!/usr/bin/python
# coding: utf-8

from math import degrees, sqrt

from PyQt4 import QtCore

class Supervisor(object):
    """The supervisor class oversees the control of a single robot.
    """

    def __init__(self, pos_):
        # Initialize the estimation of the position
        self._posEstimate = pos_

    def posEstimate(self, ):
        """Get the current estimation of the position.
        """
        return self._posEstimate

    def setPosEstimate(self, pos_):
        """Update the current estimation of the position.
        """
        self._posEstimate = pos_

    def execute(self, state_, dt_):
        """Select and execute the current controller.
        """
        raise NotImplementedError("Supervisor.execute")

    def updateStateEstimate(self, ):
        """Update the current estimation of the state of the robot position.
        """
        raise NotImplementedError("Supervisor.updateStateEstimate")

    def controllerState(self, ):
        """Get the parameters that the current controller needs for s.
        """
        raise NotImplementedError('Supervisor.controllerState')
