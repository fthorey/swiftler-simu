#!/usr/bin/python
# coding: utf-8

from common import const
from PyQt4 import QtGui, QtCore
from physics import Physics

class World(QtGui.QGraphicsScene):
    """ World class provides access to all objects within the simulated environment
    """

    def __init__(self, parent):
        """
        """
        # Call parent constructor
        super(World, self).__init__(parent)

        # Physics that rules the world
        self.physics = Physics(self)

    # Set the physics that rules the world
    def setPhysics(self, physics_):
        """
        """
        self.physics = physics_

    def addObject(self, object_, position_):
        """
        """
        object_.setPos(position_)
        self.addItem(object_)

    # Action to perform when the scene changes
    def advance(self, ):
        """
        """
        # Call parent advance method
        super(World, self).advance()

        # Apply physics
        self.physics.apply()
