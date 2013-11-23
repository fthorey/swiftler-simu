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
    def __init__(self, worldCtrl_):
        """
        """
        self.worldCtrl = worldCtrl_

    def trigger(self, ):
        """
        """
        self.worldCtrl.update()
        updateWorld = self.worldCtrl.getScheduler().getEvent('UpdateWorld')
        updateWorld.setDelay(self.worldCtrl.getWorldModel().getStepDuration())

class World(object):
    """ World class provides access to all objects within the simulated environment
    """

    def __init__(self, stepDuration_):
        """
        """
        self.worldModel = WorldModel(stepDuration_)
        self.worldCtrl = WorldCtrl(self.worldModel)

    def setSpeedFactor(self, speedFactor_):
        """
        """
        self.worldModel.setSpeedFactor(speedFactor_)

    def addRobot(self, robot_):
        """
        """
        self.worldModel.addRobot(robot_)

    def step(self, steps_):
        """
        """
        self.worldCtrl.step(steps_)

class WorldModel(object):
    """ WorldModel class is a container for all objects within the simulated environment
    """

    def __init__(self, stepDuration_):
        """
        """
        self.stepDuration = stepDuration_
        self.speedFactor = 1
        self.robots = dict()

    def addRobot(self, robot_):
        """
        """
        if robot_.getName() in self.robots:
            raise Exception("Can't add a robot with name: " + name_ + ", already exist")
        else:
            self.robots[robot_.getName()] = robot_

    def getRobots(self, ):
        """
        """
        return self.robots

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

    def update(self, ):
        """
        """

        # Update robots
        for name, robot in self.robots.iteritems():
            robot.update(self.stepDuration)
            print 'robot position: X=' + str(robot.getPos().getX()) + ' Y=' + str(robot.getPos().getY())

        # self.physicsEngine.updateCollision()
        # self.physicsEngine.updatePhysics()

class WorldCtrl(object):
    """ WorldCtrl class manages updates within the simulated environment
    """

    def __init__(self, worldModel_):
        """
        """
        self.time = Timing()
        self.scheduler = Scheduler(self.time)
        self.worldModel = worldModel_

        updateWorld = self.scheduler.createEvent(UpdateWorld(self), 'UpdateWorld')
        updateWorld.setDelay(self.worldModel.getStepDuration())

    def getTime(self, ):
        """
        """
        return self.time

    def getScheduler(self, ):
        """
        """
        return self.scheduler

    def getWorldModel(self, ):
        """
        """
        return self.worldModel

    def step(self, steps_):
        """
        """
        self.scheduler.setEndOfWindowDelay(steps_ * self.worldModel.getStepDuration())
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
                sleepTime = (deltaSimDelay - deltaRealDelay) / self.worldModel.getSpeedFactor()
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
        self.worldModel.update()
