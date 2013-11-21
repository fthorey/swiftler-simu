#!/usr/bin/python
# coding: utf-8

from physics.world import World
from robots.robot import Robot

world = World(100)

robot1 = Robot('Robot1', 0.021, 0.0885)
world.addRobot(robot1)
world.step(10)
