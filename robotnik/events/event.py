#!/usr/bin/python
# coding: utf-8

from common import const

class Event(object):
    """ Event class contains an event
    """

    # Invalid date
    const.INVALID_DATE = 0x7FFFFFFFFFFFFFFF

    # Event states
    const.NOT_ACTIVE = 'NOT_ACTIVE'
    const.ACTIVE = 'ACTIVE'
    const.PAUSE = 'PAUSE'
    const.INVALID_EVENT = 'INVALID_EVENT'

    def __init__(self, scheduler_, time_, eventIf_, name_):
        """
        """
        self.scheduler = scheduler_
        self.time = time_
        self.eventIf = eventIf_
        self.name = name_
        self.status = const.NOT_ACTIVE
        self.dateInMs = const.INVALID_DATE

    def __str__(self, ):
        """
        """
        return self.name

    def getName(self, ):
        """
        """
        return self.name

    def trigger(self, ):
        """
        """
        self.eventIf.trigger()

    def reset(self, ):
        """
        """
        self.status = const.NOT_ACTIVE
        self.dateInMs = const.INVALID_DATE
        self.scheduler.updateEvent()

    def setDelayInMs(self, delayInMs_):
        """
        """
        self.dateInMs = self.time.getTimeInMs() + delayInMs_
        self.status = const.ACTIVE
        self.scheduler.updateEvent()

    def setDateInMs(self, dateInMs_):
        """
        """
        self.dateInMs = dateInMs_
        self.status = const.ACTIVE
        self.scheduler.updateEvent()

    def getStatus(self, ):
        """
        """
        return self.status

    def setStatus(self, status_):
        """
        """
        self.status = status_

    def getDateInMs(self, ):
        """
        """
        return self.dateInMs

class EventIf(object):
    """ EventIf interface class allows the user to implement an event trigger function
    """

    def __init__(self, ):
        """
        """
        pass

    def trigger(self, ):
        """
        """
        raise NotImplementedError( "Should have implemented this method" )

class WindowEvent(EventIf):
    """ WindowEvent class contains a time window event
    """

    def __init__(self, scheduler_):
        """
        """
        self.scheduler = scheduler_
        self.event = self.scheduler.createEvent(self, 'windowEvent')

    def getEvent(self, ):
        """
        """
        return self.event

    def trigger(self, ):
        """
        """
        self.scheduler.setEndOfWindow(True)
