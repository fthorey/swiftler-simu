#!/usr/bin/python
# coding: utf-8

class WheelEncoder(object):
    """ The WheelEncoder class represents a generic class for wheel encoders
    """

    def __init__(self, ticksPerRev_, wheelRadius_):
        # Store Wheel radius
        self._wheelRadius = wheelRadius_

        # Store the number of ticks in a revolution (2pi)
        self._ticksPerRev = ticksPerRev_

        # Store the current number of ticks
        self._ticks = 0

    def ticksPerRev(self, ):
        """Return the constant number of ticks that occurs during a single (2*pi) revolution
        """
        return self._ticksPerRev

    def ticks(self, ):
        """Return the current number of ticks that already occured
        """
        return self._ticks

    def resetTicks(self, ):
        """Reset the current number of ticks
        """
        self._ticks = 0
