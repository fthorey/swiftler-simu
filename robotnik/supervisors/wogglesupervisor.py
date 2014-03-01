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

    def __init__(self, robot_, pos_):
        # Call parent constructor
        super(WoggleSupervisor, self,).__init__(robot_, pos_);

        # Create a go-to-goal controller
        self._controllers = {'obst': AvoidObstacle(robot_.proxSensors()),
                             'gtg': GoToGoal(),}

        # Current controller
        self._currController = self._controllers['gtg']

        # Store old values of wheel encoder ticks
        self._prevLeftTicks = 0
        self._prevRightTicks = 0

        # Set the goal (in m)
        self.setGoal(1, -10)

        # Distance from the goal to which the robot stop (in m)
        self.setStopDist(0.05)

    def controller(self, ):
        """Return the current controller of the robot.
        """
        return self._currController

    def setController(self, controller_):
        """Set the controller of the robot.
        """
        self._currController = controller_

    def execute(self, dt_):
        """Selects and executes a controller.
        """

        # Stop the robot if at goal
        if self.isAtGoal() or self.robot().isStopped():
            self.robot().setWheelSpeeds(0, 0)
            return

        # 1 -> Update the estimation of the robot state
        self.updateOdometry()

        # 2 -> Execute the controller to obtain command to apply to the robot
        v, w = self._currController.execute(self.posEstimate(), self.goal(), dt_)

        # Convert speed (in m/s) and angular rotation (in rad/s) to
        # angular speed to apply to each robot wheels (in rad/s)
        vel_l, vel_r = self.robot().dynamics().uni2Diff(v, w)

        # 3 -> Apply current speed to wheels
        self.robot().setWheelSpeeds(vel_l, vel_r)

    def updateOdometry(self, ):
        """Update the current estimation of the robot state.
        """
        ticks_per_rev = self.robot().leftWheelEncoder().ticksPerRev()
        left_ticks = int(self.robot().leftRevolutions()*ticks_per_rev)
        right_ticks = int(self.robot().rightRevolutions()*ticks_per_rev)

        dtl = left_ticks - self._prevLeftTicks
        dtr = right_ticks - self._prevRightTicks

        # Save the wheel encoder ticks for the next estimate
        self._prevLeftTicks += dtl
        self._prevRightTicks += dtr

        # Get old state estimation (in m and rad)
        x, y, theta = self.posEstimate()

        # Get robot parameters (in m)
        R = self.robot().wheelRadius()
        L = self.robot().wheelBaseLength()
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
        self.setPosEstimate((x_new, y_new, theta_new))
