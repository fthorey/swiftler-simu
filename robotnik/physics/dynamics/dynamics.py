#!/usr/bin/python
# coding: utf-8

class DifferentialDrive(object):
    """ DifferentialDrive class implements a differential drive behavior
    """

    def __init__(self, wheelRadius_, wheelBaseLength_):
        """
        """
        self.wheelRadius = wheelRadius_
        self.wheelBaseLength = wheelBaseLength_
