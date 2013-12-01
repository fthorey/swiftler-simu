#!/usr/bin/python
# coding: utf-8

from math import atan2, fabs, log, sin, cos

class Controller(object):
    """ Controller class provides a default class for controllers
    """

    def __init__(self, ):
        """
        """

    def execute(self, stateEstimate, inputs, dt):
        """
        """

        return

class GoToGoal(Controller):
    """ GoToGoal class steers the robot towards a goal with a constant velocity using PID
    """

    def __init__(self, ):
        """
        """
        # PID gains
        # Proportional
        self.Kp = 5;
        # Integral
        self.Ki = 0.01;
        # Derivative
        self.Kd = 0.

        # Accumulated error
        self.E_k = 0;
        # error step k-1
        self.e_k_1 = 0;

    def execute(self, stateEstimate, goal, dt):
        """
        """

        # Retrieve the (relative) goal location
        x_g = goal.x()
        y_g = goal.y()

        # Get an estimate of the current pos
        x = stateEstimate[0].x()
        y = stateEstimate[0].x()
        theta = stateEstimate[1]

        # Compute the v,w that will get you to the goal

        # 1. Calculate the heading (angle) to the goal

        # Distance between goal and robot in x-direction
        u_x = x_g - x

        # Distance between goal and robot in y-direction
        u_y = y_g - y

        # Angle from robot to goal. Use ATAN2
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
        e_I = self.E_k + e_k*dt

        # Error for the derivative term
        # Approximate the derivative using the previous error, e_k_1
        e_D = (e_k - self.e_k_1) / dt

        w = self.Kp*e_P + self.Ki*e_I + self.Kd*e_D

        # 4. Save errors for the next time step
        E_k = e_I
        e_k_1 = e_k

        # velocity control
        v =  0.25/(log(fabs(w)+2)+1)

        return v, w
