#!/usr/bin/python
# coding: utf-8

from event import Event, WindowEvent
from common import const

class Scheduler(object):
    """ Scheduler class handles events scheduling
    """

    def __init__(self, time_):
        """
        """
        self.time = time_
        self.events = dict()
        self.currentEvent = None
        self.currentDate = const.INVALID_DATE
        self.windowEvent = WindowEvent(self)
        self.isEow = False

    def createEvent(self, eventIf_, name_):
        """
        """
        # Check if events already exist
        if name_ in self.events.keys():
            raise Exception("Can't create an event with name: " + name_ + ", already exist")
        else:
            self.events[name_] = Event(self, self.time, eventIf_, name_)

        # Update all events
        self.updateEvent()
        return self.events[name_]

    def updateEvent(self, ):
        """
        """
        self.currentEvent = None
        self.currentDate = const.INVALID_DATE
        for name, event in self.events.iteritems():
            if event.getStatus() is const.ACTIVE:
                if (event.getDate() < self.currentDate):
                    self.currentDate = event.getDate()
                    self.currentEvent = event

    def checkEvent(self, ):
        """
        """
        if self.currentDate <= self.time.getSimTime():
            while self.currentDate <= self.time.getSimTime():
                self.triggerCurrentEvent()
        return self.isEow;

    def triggerCurrentEvent(self, ):
        """
        """
        self.currentEvent.setStatus(const.NOT_ACTIVE)
        self.currentEvent.trigger()
        self.updateEvent()

    def setEndOfWindow(self, eow_):
        """
        """
        self.isEow = eow_

    def getEndOfWindow(self, ):
        """
        """
        return self.isEow

    def setEndOfWindowDelay(self, delay_):
        """
        """
        self.isEow = False
        self.windowEvent.getEvent().setDelay(delay_)

    def getNextEventDate(self, ):
        """
        """
        return self.currentDate

    def getNextEvent(self, ):
        """
        """
        return self.currentEvent

    def getEvent(self, name_):
        """
        """
        try:
            return self.events[name_]
        except KeyError:
            print "The event with name: " + name_ + ", has never been registered"
            raise
