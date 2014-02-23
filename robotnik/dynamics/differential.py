#!/usr/bin/python
# coding: utf-8

from utils import const
from math import cos, sin, pi, degrees, radians
from PyQt4 import QtGui, QtCore

class DifferentialDrive(object):
    """ The DifferentialDrive class implements a differential drive behavior for
    an unicycle robot.
    """

    def __init__(self, robot_):
        # Robot that uses this differential drive
        self._robot = robot_

    def update(self, dt_):
        """Updates the position of the robot.
        """

        # Make shortcuts for wheel radius and base length (m)
        R = self._robot.wheelRadius()
        L = self._robot.wheelBaseLength()

        # Make shortcuts for wheels velocity (rad/s)
        vel_l = self._robot.getLeftWheelSpeed()
        vel_r = self._robot.getRightWheelSpeed()

        # Convert to robot spped and angular velocity (in m and rad/s)
        v, w = self.diff2Uni(vel_l, vel_r)

        # Current angle of the robot (rad)
        theta = self._robot.getAngle()

        # Position of the robot in the scene referential
        x,y =  self._robot.pos().x(), self._robot.pos().y()

        # Calculate robot's position and angle increment
        if w == 0:
            dtheta = 0
            x += v*cos(theta)*dt_
            y += v*sin(theta)*dt_
        else:
            dtheta = w*dt_
            x += 2*v/w*cos(theta + dtheta/2)*sin(dtheta/2)
            y += 2*v/w*sin(theta + dtheta/2)*sin(dtheta/2)
            theta += dtheta

        l_rev = self._robot.leftRevolutions()
        r_rev = self._robot.rightRevolutions()
        self._robot.setLeftRevolutions(l_rev +  vel_l*dt_/2/pi)
        self._robot.setRightRevolutions(r_rev + vel_r*dt_/2/pi)

        self._robot.setPos(QtCore.QPointF(x, y))
        self._robot.setAngle((theta + pi)%(2*pi) - pi)

        # Add the position to the tracker
        self._robot.tracker().addPosition(QtCore.QPointF(x, y))

    def uni2Diff(self, v, w):
        """Convert heading velocity and angular velocity (in m/s & rad/s)
        to left wheel angular velocity and right wheel angular velocity (in rad/s).
        """
        R = self._robot.wheelRadius() # in m
        L = self._robot.wheelBaseLength() # in m

        summ = 2*v/R
        diff = L*w/R

        vl = (summ-diff)/2
        vr = (summ+diff)/2

        return vl, vr


    def diff2Uni(self, vel_l, vel_r):
        """Convert left wheel angular velocity and right wheel angular velocity to
        heading velocity and angular velocity (in m/s & rad/s).
        """
        R = self._robot.wheelRadius() # in m
        L = self._robot.wheelBaseLength() # in m

        v = R/2*(vel_l+vel_r) # in m/s
        w = R/L*(vel_l-vel_r) # in rad/s

        return v, w
