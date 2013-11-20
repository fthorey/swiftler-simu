#!/usr/bin/python
# coding: utf-8

from common import const
from events.time import Time
from events.event import EventIf
from events.scheduler import Scheduler

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
        self.time = Time()
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

    def getStepDurationInMs(self, ):
        """
        """
        return self.stepDurationInMs

    def step(self, steps_):
        """
        """
        self.scheduler.setEndOfWindowDelay(steps_ * self.stepDurationInMs)
        while (not self.scheduler.checkEvent()):
            dateInMs = self.scheduler.getNextEventDateInMs()
            if dateInMs is const.INVALID_DATE:
                raise Exception("No event scheduled")
            self.time.setTimeInMs(dateInMs)

    def update(self, ):
        """
        """
        print 'update world @: ' + str(self.time.getTimeInMs()) + 'ms'

        # self.physicsEngine.updateCollision()
        # self.physicsEngine.updatePhysics()
