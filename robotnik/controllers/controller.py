#!/usr/bin/python
# coding: utf-8

from math import atan2, fabs, log, sin, cos, degrees, pi
from utils import const

class Controller(object):
    """ Controller class provides a default class for controllers
    """

    def __init__(self, ):
        """
        """

    def execute(self, stateEstimate, inputs, dt):
        """
        """

class Rotate(Controller):
    """ Rotate make the robot to rotate
    """

    def __init__(self, ):
        """
        """
    # the goal must be expressed in m and the time step in s
    def execute(self, stateEstimate, goal, dt):
        """
        """
        v = 0.1
        w = 0.5
        return v, w

class GoToGoal(Controller):
    """ GoToGoal class steers the robot towards a goal with a constant velocity using PID
    """

    def __init__(self, ):
        """
        """
        # PID gains
        # Proportional
        self.Kp = 0.9
        # Integral
        self.Ki = 0.1
        # Derivative
        self.Kd = 0.01

        # Accumulated error
        self.E_k = 0;
        # error step k-1
        self.e_k_1 = 0;

    # the goal must be expressed in m and the time step in s
    def execute(self, stateEstimate, goal, dt):
        """
        """
        # Retrieve the goal location (in m)
        x_g = goal.x()
        y_g = goal.y()

        # Get an estimate of the current pos (in m and rad)
        x, y = stateEstimate['x'], stateEstimate['y']
        theta = stateEstimate['theta']

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
        e_I = self.E_k + e_k*dt
        e_I = (e_I + pi)%(2*pi) - pi

        # Error for the derivative term
        # Approximate the derivative using the previous error, e_k_1
        e_D = (e_k - self.e_k_1) / dt

        w = self.Kp*e_P + self.Ki*e_I + self.Kd*e_D # (in rad/s)

        # 4. Save errors for the next time step
	 self.E_k = e_I
        self.e_k_1 = e_k

        # velocity control
        v =  0.25/(log(fabs(w)+2)+1)

        return v, w
