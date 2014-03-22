#!/usr/bin/python
# coding: utf-8

from controllers.pidcontroller import PIDController
import numpy as np
from math import pi, atan2, cos, sin, sqrt

class FollowWall(PIDController):
    """The FollowWall class steers the robot to a direction that is a linear combination
    of a vector tangential and a vector normal to a wall
    """

    def __init__(self, info_):

        # Call PIDController constructor
        super(FollowWall, self).__init__(info_)

        self._along_wall_vector = None
        self._to_wall_vector = None

    def getHeading(self, info_):
        """Get the direction in which the controller wants to move the robot
        as a vector.
        """
        # Get heading direction
        direction = info_.direction

        # Angles are normalised to positive values:
        # heading to left, means a wall has been detected by a
        # sensor on the left side of the robot, as angles
        # are measured positive CW, the angle must be multiplied
        # by -1. If heading is right, the angle is always positive.
        dirFactor = 1
        if direction is 'right':
            dirFactor = -1

        sensors = [(s, d) for s, d in zip(info_.sensors.insts, info_.sensors.dist)
                   if (d < info_.sensors.rmax)]

        # Make sure sensors are sorted from front to back
        sensors = sorted(sensors, key = lambda (p, d): abs(p.angle()))

        # No wall - drive a bit to the wall
        if len(sensors) == 0:
            return np.array([0.8, dirFactor * 0.6, 1])

        # Calculate vectors for each detecting sensors
        vectors = np.array([s.mapToParent(d, 0) for s, d in sensors])

        # Only one sensor detect a wall
        if len(sensors) == 1:
            sensor = sensors[0]
            reading = sensor[1]
            self._to_wall_vector = vectors[0]
            if self._along_wall_vector is None:
                # We've only started, it's a corner,
                # go perpendicular to its vector
                self._along_wall_vector = np.array([dirFactor * self._to_wall_vector[1],
                                                    -dirFactor * self._to_wall_vector[0],
                                                    1])

                # Which direction to go?
                # either away from this corner or directly to it.
                # let's blend ahead with corner:
                theta_h = sensor[0].angle() * reading/ info_.sensors.rmax
                return np.array([reading * cos(theta_h),
                                 reading * sin(theta_h),
                                 1])

            else:
                # To minimize jittering, blend with the previous
                # reading, and don't rotate more than 0.2 rad.
                prev_theta = atan2(self._along_wall_vector[1],
                                   self._along_wall_vector[0])

                self._along_wall_vector = np.array([dirFactor * self._to_wall_vector[1],
                                                    -dirFactor * self._to_wall_vector[0],
                                                    1])

                this_theta = atan2(self._along_wall_vector[1],
                                   self._along_wall_vector[0])

                dtheta = prev_theta - this_theta
                if abs(dtheta) > 0.2:
                    dtheta *= 0.2*abs(dtheta)

                self._along_wall_vector = np.array([
                            reading * cos(prev_theta - dtheta),
                            reading * sin(prev_theta - dtheta),
                            1])

        # More than one sensor detect the wall
        else:
            # Take the fist and the last
            self._along_wall_vector = vectors[0] - vectors[-1]
            a = vectors[-1]
            b = self._along_wall_vector
            self._to_wall_vector = a - b*np.dot(a,b)/np.dot(b,b)

        return self._along_wall_vector
