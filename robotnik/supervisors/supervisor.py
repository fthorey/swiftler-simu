#!/usr/bin/python
# coding: utf-8

from math import degrees, sqrt
from utils.struct import Struct
from utils import helpers

from PyQt4 import QtCore

class Supervisor(object):
    """The supervisor class oversees the control of a single robot.
    """

    def __init__(self, pos_, robotInfo_):
        # Store information about the robot
        self._info = Struct()
        self._info.pos = pos_

        # Current controller
        self._current = None

        # Dict controller -> (function, controller)
        self._states = {}

    def processStateInfo(self, ):
        """Process the current estimation of the state of the robot position.
        """
        raise NotImplementedError("Supervisor.processStateInfo")

    def info(self, ):
        """Get the parameters that the current controller needs for s.
        """
        return self._info

    def createController(self, moduleString_, info_):
        """Create and return a controller instance for a given controller class.
        """
        controllerClass = helpers.load_by_name(moduleString_, 'controllers')
        return controllerClass(info_)

    def addController(self, controller_, *args):
        """Add a transition table for a state with controller.
        """
        self._states[controller_] = args

    def execute(self, robotInfo_, dt_):
        # Process state info
        self.processStateInfo(robotInfo_)

        # Switch:
        if self._current in self._states:
            for f, c in self._states[self._current]:
                if f():
                    c.restart()
                    self._current = c
                    print "Switched to {}".format(c.__class__.__name__)
                    break

        #execute the current controller
        return self._current.execute(self.info(), dt_)
