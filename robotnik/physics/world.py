#!/usr/bin/python
# coding: utf-8

from common import const
from PyQt4 import QtGui, QtCore

class World(QtGui.QGraphicsScene):
    """ World class provides access to all objects within the simulated environment
    """

    def __init__(self, parent):
        """
        """
        # Call parent constructor
        super(World, self).__init__(parent)

    def addRobot(self, robot_):
        """
        """
        self.addItem(robot_)
