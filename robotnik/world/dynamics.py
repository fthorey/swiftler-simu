#!/usr/bin/python
# coding: utf-8

from utils import const
from math import cos, sin, pi, degrees, radians
from PyQt4 import QtGui, QtCore

class DifferentialDrive(object):
    """ DifferentialDrive class implements a differential drive behavior
    """

    def __init__(self, robot_):
        """
        """

        # Robot that uses the differential drive
        self.robot = robot_

    # The step duration is given in s
    def update(self, dt_):
        """
        """

        # Make shortcuts for wheel radius and base length (m)
        R = self.robot.getWheelRadius()
        L = self.robot.getWheelBaseLength()

        # Make shortcuts for wheels velocity (rad/s)
        vel_l = self.robot.getLeftWheelSpeed()
        vel_r = self.robot.getRightWheelSpeed()

        # Convert to robot spped and angular velocity (in m and rad/s)
        v, w = self.diff2Uni(vel_l, vel_r)

        # Delta integration time (s)
        dt = dt_

        # Current angle of the robot (rad)
        theta_k = self.robot.getTheta()

        # Position of the robot in the scene referential
        pos_k =  self.robot.pos()

        # Calculate robot's position and angle increment
        dx = v*cos(theta_k)*dt # in m
        dy = v*sin(theta_k)*dt # in m
        pos = QtCore.QPointF(pos_k.x() + dx, pos_k.y() + dy)
        dtheta = (dt*w) % 2*pi # in rad

        # Apply new position of the robot (in m & rad)
        self.robot.setPos(pos)
        self.robot.setTheta(theta_k + dtheta)

    # Convert heading velocity and angular velocity (in m/s & rad/s)
    # To left wheel angular velocity and right wheel angular velocity (in rad/s)
    def uni2Diff(self, v, w):
        """
        """
        R = self.robot.getWheelRadius() # in m
        L = self.robot.getWheelBaseLength() # in m

        vel_l = v/R+(w*L)/(2*R); # in rad/s
        vel_r = v/R-(w*L)/(2*R); # in rad/s

        return vel_l, vel_r

    # Convert left wheel angular velocity and right wheel angular velocity to
    # heading velocity and angular velocity (in m/s & rad/s)
    def diff2Uni(self, vel_l, vel_r):
        """
        """
        R = self.robot.getWheelRadius() # in m
        L = self.robot.getWheelBaseLength() # in m

        v = R/2*(vel_l+vel_r) # in m/s
        w = R/L*(vel_l-vel_r) # in rad/s

        return v, w
