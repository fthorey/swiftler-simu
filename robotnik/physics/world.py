#!/usr/bin/python
# coding: utf-8

from common import const
from events.timing import Timing
from events.event import EventIf
from events.scheduler import Scheduler

from time import sleep

class UpdateWorld(EventIf):
    """
    """
    def __init__(self, world_):
        """
        """
        self.world = world_

    def trigger(self, ):
        """
        """
        self.world.update()
        updateWorld = self.world.getScheduler().getEvent('UpdateWorld')
        updateWorld.setDelayInMs(self.world.getStepDurationInMs())

class World(object):
    """ World class provides access to all objects withing the simulated environment
    """

    def __init__(self, stepDurationInMs_):
        """
        """
        self.stepDurationInMs = stepDurationInMs_
        self.speedFactor = 1
        self.time = Timing()
        self.scheduler = Scheduler(self.time)

        updateWorld = self.scheduler.createEvent(UpdateWorld(self), 'UpdateWorld')
        updateWorld.setDelayInMs(self.stepDurationInMs)

    def getTime(self, ):
        """
        """
        return self.time

    def getScheduler(self, ):
        """
        """
        return self.scheduler

    def getSpeedFactor(self, ):
        """
        """
        return self.speedFactor

    def setSpeedFactor(self, speedFactor_):
        """
        """
        self.speedFactor = speedFactor_

    def getStepDurationInMs(self, ):
        """
        """
        return self.stepDurationInMs

    def step(self, steps_):
        """
        """
        self.scheduler.setEndOfWindowDelay(steps_ * self.stepDurationInMs)
        prevSimDateInMs = self.time.getSimTimeInMs()
        prevRealDateInMs = self.time.getRealTimeInMs()
        while (not self.scheduler.checkEvent()):
            simDateInMs = self.scheduler.getNextEventDateInMs()
            if simDateInMs is const.INVALID_DATE:
                raise Exception("No event scheduled")

            self.time.setSimTimeInMs(simDateInMs)
            deltaSimDelayInMs = simDateInMs - prevSimDateInMs
            prevSimDateInMs = simDateInMs

            deltaRealDelayInMs = self.time.getRealTimeInMs() - prevRealDateInMs
            if (deltaRealDelayInMs <= deltaSimDelayInMs):
                sleepTime = deltaSimDelayInMs - deltaRealDelayInMs) / self.speedFactor
                self.time.sleepTimeInMs((sleepTime)
            else:
                raise Exception("Real time lost")
            prevRealDateInMs = self.time.getRealTimeInMs()

    def update(self, ):
        """
        """
        print 'update world @: ' + str(self.time.getSimTimeInMs()) + 'ms'

        # self.physicsEngine.updateCollision()
        # self.physicsEngine.updatePhysics()
