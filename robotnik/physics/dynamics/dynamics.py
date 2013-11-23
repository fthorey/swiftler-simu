#!/usr/bin/python
# coding: utf-8

from scipy.integrate import ode

from common.position import Pos2D

from math import cos, sin

class DifferentialDrive(object):
    """ DifferentialDrive class implements a differential drive behavior
    """

    def __init__(self, wheelRadius_, wheelBaseLength_):
        """
        """
        self.wheelRadius = wheelRadius_
        self.wheelBaseLength = wheelBaseLength_

    def apply(self, pos_t, dt, vel_r, vel_l):
        """
        """
        R = self.wheelRadius
        L = self.wheelBaseLength

        v = R/2*(vel_r+vel_l)
        w = R/L*(vel_r+vel_l)

        x_k, y_k, theta_k = pos_t.unPack()

        pos_t.setX(x_k + dt*(v*cos(theta_k)))
        pos_t.setY(y_k + dt*(v*sin(theta_k)))
        pos_t.setTheta(theta_k + dt*w)
