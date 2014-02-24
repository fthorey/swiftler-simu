#!/usr/bin/python
# coding: utf-8

from sensors.proximity import ProximitySensor
from PyQt4 import QtGui, QtCore

class WoggleIRSensor(ProximitySensor):
    """The WoggleIRSensor class returns measurements specific to IR sensors
    embedded on the Woggle
    """
    def __init__(self, pos_):
        # Call the generic proximity sensors constructor
        super(WoggleIRSensor, self).__init__(pos_)

    def distance2Value(self, distance):
        """Returns the distance calculation from the distance readings of the proximity sensors
        """
        if distance < self.rmin() :
            return 3960;
        else:
            return (3960*exp(-30*(distance-self.rmin())));
