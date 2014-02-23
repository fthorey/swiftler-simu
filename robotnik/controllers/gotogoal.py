#!/usr/bin/python
# coding: utf-8

from math import atan2, fabs, log, sin, cos, degrees, pi
from controllers.controller import Controller

class GoToGoal(Controller):
    """ The GoToGoal class steers the robot towards a goal with a certain linear velocity using PID
    """

    def __init__(self, ):
        # PID gains
        # Proportional
        self._Kp = 0.8
        # Integral
        self._Ki = 0.1
        # Derivative
        self._Kd = 0.01

        # Accumulated error
        self._E_k = 0;
        # error step k-1
        self._e_k_1 = 0;

    def execute(self, state_, goal_, dt_):
        """ Take an estimation of the current state and a heading goal to
        process the appropriate linear velocity v (m/s) and angular velocity (rad/s) to steers
        the robot toward this goal direction.

        :param state_: Estimation of the current state of the robot (x,y,theta) (m,m,rad)
        :param goal_: Heading goal of the robot (m)
        :param dt_: Time elapsed since last call to 'execute'
        """
        # Retrieve the goal location (in m)
        x_g, y_g = goal_

        # Get an estimate of the current pos (in m and rad)
        x, y = state_['x'], state_['y']
        theta = state_['theta']

        # Compute the v,w that will get you to the goal

        # 1. Calculate the heading (angle) to the goal

        # Distance between goal and robot in x-direction (in m)
        u_x = x_g - x

        # Distance between goal and robot in y-direction (in m)
        u_y = y_g - y

        # Angle from robot to goal. Use ATAN2 (in rad)
        theta_g = atan2(u_y, u_x)

        # 2. Calculate the heading error

        # Error between the goal angle and robot's angle
        # Use ATAN2 to make sure this stays in [-pi,pi]
        e_k = theta_g - theta
        e_k = atan2(sin(e_k), cos(e_k))

        # 3. Calculate PID for the steering angle

        # Error for the proportional term
        e_P = e_k

        # Error for the integral term
        # Approximate the integrale using the accumulated error, E_k and the error
        # for this time step
        e_I = self._E_k + e_k*dt_
        e_I = (e_I + pi)%(2*pi) - pi

        # Error for the derivative term
        # Approximate the derivative using the previous error, e_k_1
        e_D = (e_k - self._e_k_1) / dt_

        w = self._Kp*e_P + self._Ki*e_I + self._Kd*e_D # (in rad/s)

        # 4. Save errors for the next time step
        self._E_k = e_I
        self._e_k_1 = e_k

        # velocity control
        v =  0.25/(log(fabs(w)+2)+1)

        return v, w
