#!/usr/bin/python
# coding: utf-8

class Timing(object):
    """ Time class handles time
    """

    def __init__(self, ):
        """
        """
        self.simTime = 0

    def addSimTime(self, simTime_):
        """
        """
        self.simTime = self.simTime + simTime_

    def setSimTime(self, simTime_):
        """
        """
        self.simTime = simTime_

    def getSimTime(self, ):
        """
        """
        return self.simTime

    def getRealTime(self, ):
        """
        """
        from time import time
        return time()

    def sleepTime(self, sleepTime_):
        """
        """
        from time import sleep
        sleep(sleepTime_)
