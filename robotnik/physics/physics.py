#!/usr/bin/python
# coding: utf-8

from common import const
from PyQt4 import QtGui, QtCore

class Physics(object):
    """ Physics that rules a world
    """

    def __init__(self, world_):
        """
        """
        # Set the world on which the physics apply
        self.world = world_

    # Apply physics at each step
    def apply(self, ):
        """
        """
        # Check all item currently in the scene
        for item in self.world.items():
            if self.world.collidingItems(item):
                print 'hello'

        # Detect bodies collision
        self.detectBodyCollision()

        # Proximity sensors detection
        self.proximitySensorDetection()

    # Detect body collision
    def detectBodyCollision(self, ):
        """
        """

    # Proximity sensors collision
    def proximitySensorDetection(self, ):
        """
        """
