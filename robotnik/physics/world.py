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
        updateWorld.setDelay(self.world.getStepDuration())

class World(object):
    """ World class provides access to all objects withing the simulated environment
    """

    def __init__(self, stepDuration_):
        """
        """
        self.stepDuration = stepDuration_
        self.speedFactor = 1
        self.time = Timing()
        self.scheduler = Scheduler(self.time)
        self.robots = dict()

        updateWorld = self.scheduler.createEvent(UpdateWorld(self), 'UpdateWorld')
        updateWorld.setDelay(self.stepDuration)

    def addRobot(self, robot_):
        """
        """
        if robot_.getName() in self.robots:
            raise Exception("Can't add a robot with name: " + name_ + ", already exist")
        else:
            self.robots[robot_.getName()] = robot_

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

    def getStepDuration(self, ):
        """
        """
        return self.stepDuration

    def step(self, steps_):
        """
        """
        self.scheduler.setEndOfWindowDelay(steps_ * self.stepDuration)
        prevSimDate = self.time.getSimTime()
        prevRealDate = self.time.getRealTime()

        while (not self.scheduler.checkEvent()):
            # Go to the next event to trig
            simDate = self.scheduler.getNextEventDate()

            # CHeck if there are still events scheduled
            if simDate is const.INVALID_DATE:
                raise Exception("No event scheduled")

            # Update time
            self.time.setSimTime(simDate)
            deltaSimDelay = simDate - prevSimDate
            prevSimDate = simDate
            deltaRealDelay = self.time.getRealTime() - prevRealDate

            # Resynchronise on real time
            if deltaRealDelay <= deltaSimDelay:
                sleepTime = (deltaSimDelay - deltaRealDelay) / self.speedFactor
                self.time.sleepTime(sleepTime)
            # Don't raise exception when several events trig at the same time
            elif deltaSimDelay > 1e-10:
                raise Exception("Real time lost")

            # Update previous real time date
            prevRealDate = self.time.getRealTime()

    def update(self, ):
        """
        """
        print 'update world @: ' + str(self.time.getSimTime()) + 's'

        # Update robots
        for name, robot in self.robots.iteritems():
            robot.update(self.stepDuration)

        # self.physicsEngine.updateCollision()
        # self.physicsEngine.updatePhysics()
