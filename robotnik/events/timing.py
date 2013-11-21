#!/usr/bin/python
# coding: utf-8

class Timing(object):
    """ Time class handles time
    """

    def __init__(self, ):
        """
        """
        self.simTimeInMs = 0

    def addSimTimeInMs(self, simTimeInMs_):
        """
        """
        self.simTimeInMs = self.simTimeInMs + simTimeInMs_

    def setSimTimeInMs(self, simTimeInMs_):
        """
        """
        self.simTimeInMs = simTimeInMs_

    def getSimTimeInMs(self, ):
        """
        """
        return self.simTimeInMs

    def getRealTimeInMs(self, ):
        """
        """
        from time import time
        return time() * 1e-3

    def sleepTimeInMs(self, sleepTimeInMs_):
        """
        """
        from time import sleep
        sleep(sleepTimeInMs_ * 1e-3)
