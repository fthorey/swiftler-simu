#!/usr/bin/python
# coding: utf-8

from math import pi, ceil

class WheelEncoder(object):
    """
    """

    def __init__(self, ticksPerRev_, wheelRadius_):
        """
        """
        # Store Wheel radius
        self._wheelRadius = wheelRadius_

        # Store the number of ticks in a revolution (2pi)
        self._ticksPerRev = ticksPerRev_

        # Store the current number of ticks
        self._ticks = 0

    def ticksPerRev(self, ):
        """
        """
        return self._ticksPerRev

    def ticks(self, ):
        """
        """
        return self._ticks

    # def dist2Ticks(self, distance_):
    #     """
    #     """
    #     return (distance_ * self._ticksPerRev)/ (2*pi)

    # def updateTicks(self, wheelVelocity_, dt_):
    #     """
    #     """
    #     self._ticks = self._ticks + self.dist2Ticks(wheelVelocity_ * dt_)

    def resetTicks(self, ):
        """
        """
        self._ticks = 0
