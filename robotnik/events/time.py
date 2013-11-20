#!/usr/bin/python
# coding: utf-8

class Time(object):
    """ Time class handles time
    """

    def __init__(self, ):
        """
        """
        self.timeInMs = 0

    def addTimeInMs(self, timeInMs_):
        """
        """
        self.timeInMs = self.timeInMs + timeInMs_

    def setTimeInMs(self, timeInMs_):
        """
        """
        self.timeInMs = timeInMs_

    def getTimeInMs(self, ):
        """
        """
        return self.timeInMs
