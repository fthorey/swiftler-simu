#!/usr/bin/python
# coding: utf-8

from common import const
from math import cos, sin

class DifferentialDrive(object):
    """ DifferentialDrive class implements a differential drive behavior
    """

    def __init__(self, wheelRadius_, wheelBaseLength_):
        """
        """
        self.wheelRadius = wheelRadius_
        self.wheelBaseLength = wheelBaseLength_

    def update(self, robot):
        """
        """
        R = self.wheelRadius
        L = self.wheelBaseLength

        vel_l = robot.getLeftWheelSpeed()
        vel_r = robot.getRightWheelSpeed()

        v = R/2*(vel_l+vel_r)
        w = R/L*(vel_l+vel_r)

        dt = const.stepDuration
        theta_k = robot.getTheta()
        pos_k =  robot.getPos()

        dx = dt*(v*cos(theta_k))
        dy = dt*(v*sin(theta_k))

        dtheta = dt*w

        robot.setPos(robot.mapToParent(pos_k.x() + dx, pos_k.y() + dy))
        robot.setRotation(theta_k + dtheta)
