#!/usr/bin/python
# coding: utf-8

from math import atan2, fabs, log, sin, cos, degrees, pi, log1p
from controllers.pidcontroller import PIDController
import numpy as np
from PyQt4 import QtGui, QtCore


class AvoidObstacle(PIDController):
    """The AvoidObstacles class steers the robot to a direction calculated with
    the weighted sum of direction of obstacles detected by each sensors
    """

    def __init__(self, proxSensors_):

        # PID gains
        coeff = {'Kp': 0.8,
                 'Ki': 0.1,
                 'Kd': 0.01}

        # Call PIDController constructor
        super(AvoidObstacle, self).__init__(coeff)

        self._proxSensors = proxSensors_

        # Now we know the poses, it makes sense to also
        # calculate the weights
        self.weights = [(cos(p.getAngle())+1.5) for p in self._proxSensors]

        # Normalizing weights
        ws = sum(self.weights)
        self.weights = [w/ws for w in self.weights]

    def getIRDistance(self, sensor):
        """Converts the IR distance readings into a distance in meters
        """
        # Get the current reading of the sensor
        reading = sensor.reading()

        # Conver the reading to a distance (in m)
        irDistance = max( min( (log1p(3960) - log1p(reading))/30 + sensor.rmin(), sensor.rmax()),
                          sensor.rmin())

        return irDistance

    def getHeadingAngle(self, state_, goal_):
        """Get the direction in which the controller wants to move the robot.
        """
        vect_sensors = list()
        for sensor in self._proxSensors:
            # Get vector coordinates in robot coords frame
            begin_r = sensor.mapToParent(0, 0)
            end_r = sensor.mapToParent(self.getIRDistance(sensor), 0)
            # Transform the vector in robot coords frame
            xb_r, yb_r = begin_r.x(), begin_r.y()
            xe_r, ye_r = end_r.x(), end_r.y()
            vect_sensors.append(np.array([xe_r - xb_r, ye_r - yb_r]))

        vect_sensors = np.array(vect_sensors)

        heading = np.dot(vect_sensors.transpose(), self.weights)


        return atan2(heading[1], heading[0])
