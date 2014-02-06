#!/usr/bin/python
# coding: utf-8


from math import degrees, sqrt, cos, sin, pi
from robots.robot import Robot
from controllers.controller import GoToGoal, Rotate
from utils import const
from supervisors.supervisor import Supervisor
from utils import const

from PyQt4 import QtCore

class WoggleSupervisor(Supervisor):
    """ WoggleSupervisor is a class that provides a way to control a Woggle robot
    """

    def __init__(self, robot_):
        """
        """
        # Call parent constructor
        super(WoggleSupervisor, self,).__init__(robot_);

        # Store old value of wheel encoder ticks
        self.prevLeftTicks = 0
        self.prevRightTicks = 0

    # Select and execute the current controller
    # The step duration is in seconds
    def execute(self, ):
        """
        """

        if self.isAtGoal() or self.robot.isStopped():
            self.robot.setWheelSpeeds(0, 0)
            return

        # Update the estimate of the robot position
        self.updateOdometry()

        # Execute the controller to obtain parameters to apply to the robot
        v, w = self.controller.execute(self._stateEstimate, self.goal, const.stepDuration)

        # Convert speed (in m/s) and angular rotation (in rad/s) to
        # angular speed to apply to each robot wheels (in rad/s)
        vel_l, vel_r = self.robot.getDynamics().uni2Diff(v, w)

        # Apply current speed to wheels
        self.robot.setWheelSpeeds(vel_l, vel_r)

        # Update the estimate of the robot position
        self.updateOdometry()

    def updateOdometry(self, ):
        """
        """
        ticks_per_rev = self.robot.leftWheelEncoder().ticksPerRev()
        left_ticks = int(self.robot.leftRevolutions()*ticks_per_rev)
        right_ticks = int(self.robot.rightRevolutions()*ticks_per_rev)

        dtl = left_ticks - self.prevLeftTicks
        dtr = right_ticks - self.prevRightTicks

        # Save the wheel encoder ticks for the next estimate
        self.prevLeftTicks += dtl
        self.prevRightTicks += dtr

        # Get old state estimation (in m and rad)
        x, y  = self._stateEstimate['x'], self._stateEstimate['y']
        theta =self._stateEstimate['theta']

        # Get robot parameters (in m)
        R = self.robot.wheelRadius()
        L = self.robot.wheelBaseLength()
        m_per_tick = (2*pi*R) / ticks_per_rev

        # distance travelled by left wheel
        dl = dtl*m_per_tick
        # distance travelled by right wheel
        dr = dtr*m_per_tick

        theta_dt = (dr-dl)/L
        theta_mid = theta + theta_dt/2
        dst = (dr+dl)/2
        x_dt = dst*cos(theta_mid)
        y_dt = dst*sin(theta_mid)

        theta_new = theta + theta_dt
        x_new = x + x_dt
        y_new = y + y_dt

        # Update the state estimation
        self._stateEstimate['x'] = x_new
        self._stateEstimate['y'] = y_new
        self._stateEstimate['theta'] = (theta_new + pi)%(2*pi)-pi
