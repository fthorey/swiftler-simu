#!/usr/bin/python
# coding: utf-8

from physics.world import World
from robots.robot import Robot

# Step duration of 1ms
world = World(1e-3)
# Run @ 1e3 time slower than real time
world.setSpeedFactor(1e-3)

robot1 = Robot('Robot1', 0.021, 0.0885)
world.addRobot(robot1)
world.step(10)
