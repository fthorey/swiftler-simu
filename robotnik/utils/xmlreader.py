#!/usr/bin/python
# coding: utf-8

import xml.etree.ElementTree as ET
from PyQt4 import QtGui, QtCore

class XMLReader(object):
    """
    A class to handle reading and parsing of XML files for the simulator
    """

    def __init__(self, file_):
        _tree = None
        try:
            _tree = ET.parse(file_)
        except IOError:
            raise Exception('[XMLReader.__init__] Could not open ' + str(file_))
        except ET.ParseError:
            raise Exception('[XMLReader.__init__] Could not parse ' + str(file_))

        self._root = _tree.getroot()

    def parseColor(self, color):
        """
        Convert a color attribute value to int

        None will yield None, '#FFACDD' will yield 0xFFACDD

        Scope:
            Private
        Parameters:
            color ----> the color to be converted
        Return:
            An integer value in the (AA)RRGGBB format
        """
        if color is None:
            return color
        if color[0] == "#":
            return int(color[1:],16)
        color = color.lower()
        if color == 'black':
            return 0x000000
        if color == 'red':
            return 0xFF0000
        if color == 'green':
            return 0x00FF00
        if color == 'blue':
            return 0x0000FF
        raise Exception('[XMLReader.parseColor] Bad color value in XML!')

    def parseConfiguration(self):
        """
        Parse a simulation configuration file

        Scope:
            Private
        Parameters:
            None
        Return:
            A list of the objects in the simulation.
        """

        simulator_objects = []

        # robots
        for robot in self._root.findall('robot'):
            robot_type = robot.get('type')
            supervisor = robot.find('supervisor')
            if supervisor == None:
                raise Exception(
                    '[XMLReader.parseConfiguration] No supervisor specified!')

            dimension = robot.find('dimension')
            if dimension == None:
                raise Exception(
                    '[XMLReader.parseConfiguration] No dimension specified!')

            pose = robot.find('pose')
            if pose == None:
                raise Exception(
                    '[XMLReader.parseConfiguration] No pose specified!')

            try:
                x, y, theta = pose.get('x'), pose.get('y'), pose.get('theta')
                if x == None or y == None or theta == None:
                    raise Exception(
                        '[XMLReader.parseConfiguration] Invalid pose!')

                if robot_type ==  "Woggle":
                    wheelRadius = dimension.get('wheelradius')
                    wheelBaseLength = dimension.get('wheelbaselength')
                    if wheelRadius == None or wheelBaseLength == None:
                        raise Exception(
                            '[XMLReader.parseConfiguration] Invalid dimension!')

                    robot_color = self.parseColor(robot.get('color'))

                    simulator_objects.append(('robot',
                                              robot_type,
                                              supervisor.attrib['type'],
                                              (float(x),
                                               float(y),
                                               float(theta)),
                                              robot_color,
                                              (float(wheelRadius),
                                               float(wheelBaseLength)
                                           )))
            except ValueError:
                raise Exception(
                    '[XMLReader.parseConfiguration] Invalid robot (bad value)!')

        # obstacles
        for obstacle in self._root.findall('obstacle'):
            pose = obstacle.find('pose')
            if pose == None:
                raise Exception(
                    '[XMLReader.parseConfiguration] No pose specified!')

            geometry = obstacle.find('geometry')
            if geometry == None:
                raise Exception(
                    '[XMLReader.parseConfiguration] No geometry specified!')
            try:
                points = []
                for point in geometry.findall('point'):
                    x, y = point.get('x'), point.get('y')
                    if x == None or y == None:
                        raise Exception(
                            '[XMLReader.parseConfiguration] Invalid point!')
                    points.append((float(x), float(y)))

                if len(points) < 3:
                    raise Exception(
                        '[XMLReader.parseConfiguration] Too few points!')

                x, y, theta = pose.get('x'), pose.get('y'), pose.get('theta')

                if x == None or y == None or theta == None:
                    raise Exception(
                        '[XMLReader.parseConfiguration] Invalid pose!')

                color = self.parseColor(obstacle.get('color'))
                simulator_objects.append(('obstacle',
                                          (float(x),
                                           float(y),
                                           float(theta)),
                                          points,
                                          color))
            except ValueError:
                raise Exception(
                        '[XMLReader.parseConfiguration] Invalid obstacle (bad value)!')

        return simulator_objects
