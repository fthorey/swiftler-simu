#!/usr/bin/python
# coding: utf-8

from physics.dynamics.dynamics import DifferentialDrive

class Robot(object):
    """ RobotCtrl class handles a robot controller
    """

    def __init__(self, name_, wheelRadius_, wheelBaseLength_):
        """
        """
        self.name = name_
        self.wheelRadius = wheelRadius_
        self.wheelBaseLength = wheelBaseLength_

        self.dynamics = DifferentialDrive(self.wheelRadius, self.wheelBaseLength)

        self.lefWheelSpeed = 0
        self.rightWheelSpeed = 0

    def getName(self, ):
        """
        """
        return self.name

    def update(self, dt_):
        """
        """
        pass
