#!/usr/bin/python
# coding: utf-8

from common.position import Pos2D
from physics.dynamics.dynamics import DifferentialDrive

class Robot(object):
    """ Robot class handles a robot controller
    """

    def __init__(self, name_, wheelRadius_, wheelBaseLength_):
        """
        """
        self.name = name_
        self.wheelRadius = wheelRadius_
        self.wheelBaseLength = wheelBaseLength_

        self.dynamics = DifferentialDrive(self.wheelRadius, self.wheelBaseLength)

        self.pos = Pos2D(0, 0, 0)

        self.leftWheelSpeed = 0
        self.rightWheelSpeed = 0

    def getName(self, ):
        """
        """
        return self.name

    def getPos(self, ):
        """
        """
        return self.pos

    def update(self, dt_):
        """
        """
        self.dynamics.apply(self.pos, dt_, self.leftWheelSpeed, self.rightWheelSpeed)
