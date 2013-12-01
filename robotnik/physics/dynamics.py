#!/usr/bin/python
# coding: utf-8

from common import const
from math import cos, sin, pi, degrees, radians

class DifferentialDrive(object):
    """ DifferentialDrive class implements a differential drive behavior
    """

    def __init__(self, robot_):
        """
        """

        # Robot that uses the differential drive
        self.robot = robot_

    def update(self, stepDuration_):
        """
        """

        # Make shortcuts for wheel radius and base length (m)
        R = self.robot.getWheelRadius()
        L = self.robot.getWheelBaseLength()

        # Make shortcuts for wheels velocity (rad/s)
        vel_l = self.robot.getLeftWheelSpeed()
        vel_r = self.robot.getRightWheelSpeed()

        # Velocity of the robot (m/s)
        v = R/2*(vel_l+vel_r)

        # Angular velocity of the robot (rad/s)
        w = R/L*(vel_l-vel_r)

        # Delta integration time (s)
        dt = stepDuration_

        # Current angle of the robot (rad)
        theta_k = self.robot.getTheta()

        # Position of the robot in the scene referential
        pos_k =  self.robot.pos()

        # Calculate robot's position and angle increment
        dx = v*cos(theta_k)*dt
        dy = v*sin(theta_k)*dt
        dtheta = (dt*w) % 2*pi

        # Apply new position of the robot
        self.robot.setPos(pos_k.x() + dx, pos_k.y() + dy)
        self.robot.setTheta(theta_k + dtheta)
        self.robot.setRotation(degrees(theta_k + dtheta))

    def uni2Diff(self, v, w):
        """
        """
        R = self.robot.getWheelRadius()
        L = self.robot.getWheelBaseLength()

        vel_l = v/R-(w*L)/(2*R);
        vel_r = v/R+(w*L)/(2*R);

        return vel_l, vel_r
