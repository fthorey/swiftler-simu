#!/usr/bin/python
# coding: utf-8

from math import degrees, sqrt, cos, sin, pi
from robots.robot import Robot
from controllers.gotogoal import GoToGoal
from controllers.avoidobstacle import AvoidObstacle
from supervisors.supervisor import Supervisor

from PyQt4 import QtCore

class WoggleSupervisor(Supervisor):
    """ WoggleSupervisor is a class that provides a way to control a Woggle robot.

    The WoggleSupervisor does not move the robot directly. Instead, the supervisor
    selects a controller to do the work and uses the controller outputs
    to generate the robot inputs.
    """

    def __init__(self, pos_):
        # Call parent constructor
        super(WoggleSupervisor, self,).__init__(pos_);

        # Create a go-to-goal controller
        self._controllers = {'gtg': GoToGoal()}

        # Current controller
        self._currController = self._controllers['gtg']

        # Store old values of wheel encoder ticks
        self._prevLeftTicks = 0
        self._prevRightTicks = 0

    def controller(self, ):
        """Return the current controller of the robot.
        """
        return self._currController

    def setController(self, controller_):
        """Set the controller of the robot.
        """
        self._currController = controller_

    def execute(self, info_, dt_):
        """Selects and executes a controller.
        """
        # Update the informations about the robot
        self._robotInfo = info_

        # 1 -> Update the estimation of the robot state
        self.updateOdometry()

        # 2 -> Execute the controller to obtain unicycle command (v, w) to apply
        v, w = self._currController.execute(self.posEstimate(), dt_)

        return v, w

    def updateOdometry(self, ):
        """Update the current estimation of the robot state.
        """
        # Get the number of ticks on each wheel since last call
        dtl = self._robotInfo.wheels.leftTicks - self._prevLeftTicks
        dtr = self._robotInfo.wheels.rightTicks - self._prevRightTicks

        # Save the wheel encoder ticks for the next estimate
        self._prevLeftTicks += dtl
        self._prevRightTicks += dtr

        # Get old state estimation (in m and rad)
        x, y, theta = self.posEstimate()

        # Get robot parameters (in m)
        R = self._robotInfo.wheels.radius
        L = self._robotInfo.wheels.baseLength
        m_per_tick = (2*pi*R) / self._robotInfo.wheels.ticksPerRev

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
        self.setPosEstimate((x_new, y_new, theta_new))
