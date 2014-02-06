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
        R = self.robot.wheelRadius()
        L = self.robot.wheelBaseLength()

        # Make shortcuts for wheels velocity (rad/s)
        vel_l = self.robot.getLeftWheelSpeed()
        vel_r = self.robot.getRightWheelSpeed()

        # Convert to robot spped and angular velocity (in m and rad/s)
        v, w = self.diff2Uni(vel_l, vel_r)

        # Current angle of the robot (rad)
        theta = self.robot.getTheta()

        # Position of the robot in the scene referential
        x,y =  self.robot.pos().x(), self.robot.pos().y()

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

        print 'real pos:', x, y, theta

        l_rev = self.robot.leftRevolutions()
        r_rev = self.robot.rightRevolutions()
        self.robot.setLeftRevolutions(l_rev +  vel_l*dt_/2/pi)
        self.robot.setRightRevolutions(r_rev + vel_r*dt_/2/pi)

        print 'rev:', l_rev +  vel_l*dt_/2/pi, r_rev + vel_r*dt_/2/pi

        self.robot.setPos(QtCore.QPointF(x, y))
        self.robot.setTheta((theta + pi)%(2*pi) - pi)

        # Add the position to the tracker
        self.robot.tracker().addPosition(QtCore.QPointF(x, y))

    # Convert heading velocity and angular velocity (in m/s & rad/s)
    # To left wheel angular velocity and right wheel angular velocity (in rad/s)
    def uni2Diff(self, v, w):
        """
        """
        R = self.robot.wheelRadius() # in m
        L = self.robot.wheelBaseLength() # in m

        summ = 2*v/R
        diff = L*w/R

        vl = (summ-diff)/2
        vr = (summ+diff)/2

        return vl, vr

    # Convert left wheel angular velocity and right wheel angular velocity to
    # heading velocity and angular velocity (in m/s & rad/s)
    def diff2Uni(self, vel_l, vel_r):
        """
        """
        R = self.robot.wheelRadius() # in m
        L = self.robot.wheelBaseLength() # in m

        v = R/2*(vel_l+vel_r) # in m/s
        w = R/L*(vel_l-vel_r) # in rad/s

        return v, w
