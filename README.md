Robotnik
========

A robot simulator build upon the pyQt framework and inspired
by Jean-Pierre de la Croix’s Matlab [+simiam](https://github.com/jdelacroix/simiam) project.
The main gui has been designed using [QtCreator](http://qt-project.org/wiki/Category:Tools::QtCreator)

To run the simulator in gui mode, you must have installed:
* [Python2.7](http://www.python.org/getit/)
* [PyQt](http://www.riverbankcomputing.com/software/pyqt/intro)
* [Numpy](https://www.python.org/downloads/)

Python 3 is not currently officially supported.

**Table of Contents**

- [Fast Forward](#fast-forward)
- [Overview](#overview)
    - [Start-up](#start-up)
    - [Simulation basics](#simulation-basics)
- [Robot basics](#robot-basics)
    - [Robot advance method](#robot-advance-method)
    - [Creating a new robot](#creating-a-new-robot)
- [Supervisor basics](#supervisor-basics)
    - [Creating a new supervisor](#creation-a-new-supervisor)
    - [Using a planner](#using a planner)
- [Dynamic basics](#dynamic-basics)

# Fast Forward #

Assuming you're using an Unix-like OS (`*BSD`, `GNU/Linux`, `OS X`, `Solaris`,
etc) and that **pyQt** is installed, go to the root directory **robotnik** and
just type in your favorite shell the following command:

```python
python robotnik.py
```

# Overview #

## Start-up ##

The main component of the **robotnik** simulator is the **world**,
built at start-up, in which every items evolve.

The world is populated during the initialization by reading a **json** template
file located into the **world/resources** directory.

```python
    def configureWorld(self, ):

        # Create a new world
        self._world = World(self)

        # Fill the world with data from the configuration file
        self._world.readConfigurationFile(self._filename)
```

The **world** template file contains a lot of information about
the state of the world, such as:
* the position size and color of every obstacles
* the number and types of robots

Alternatively, it's also possible to specify a specific world template to load when running the
**robotnik** simulator by typing the following command:

```python
python robotnik.py --world-path=path/to/template.json
```

Using the gui, it's also possible to load a new world at any time by clicking
on the **Open World** menu item.

## Simulation basics ##

The evolution of the world follows basics of software simulation.

The **robotnik** simulator class implements a timer which is configured
to trig periodically with specific step duration configured by the
`stepDuration` class attribute. By default it's set to 20ms. The minimum
value is 10ms. There is no maximum value, but the higher the value the
higher the is precision loss. The lower is the value, the higher is the
CPU load. A value of 20ms allows to achieve simulation speed factor up
to x5 on a decent computer without sacrificing precision.

When the simulator is started by pressing the `start` button, each time
the timer trigs, the `advance` method of the world class is called
which in turns is in charge of:

1. calling the `advance` method of each objects in the world
2. applying physics (collisions between objects detection)

```python
    def advance(self, ):
        # -> Call all items currently in the world advance method
        for robot in self.robots():
            robot.advance()

        # Apply physics (collisions detection)
        self._physics.apply()
```
This process is executed cyclically until the `stop` button is pressed.

# Robot basics #

Robots are objects able to evolve inside the world.

A robot is made of 3 main components:

1. A `supervisor` in charge of controlling its evolution given certain rules.
2. A `dynamics` in charge of calculating its new position in the world according
to the current command and its particular geometry.
3. `sensors` attached to its body that provide various information about the
world around.

The `advance` method of the robot uses these 3 main components to calculate at
each time step the new position of the robot using its `dynamics`,
according to the command provided by `supervisor`, calculated using data
from its `sensors`.

**For now, only differential drive robots are supported.**

## Robot advance method ##

The `advance` method of each robot is in charge of doing several things:

1. Execute the robot's `supervisor` to get the linear velocity `v` and
angular velocity `w` to apply to the robot's wheels.
2. Apply the new calculated speed to robot's wheels.
3. Update the robot position using its `dynamics`.

```python
    def advance(self, ):
        """Action to perform when the scene changes.
        """
        # 1 -> Execute the supervisor to obtain unicycle command (v,w) to apply
        v, w = self.supervisor().execute(self.info(), const.stepDuration)
        vel_l, vel_r = self.dynamics().uni2Diff(v, w)

        # 2 -> Apply current speed to wheels
        self.setWheelSpeeds(vel_l, vel_r)

        # 3 -> Update the robot position using dynamic and current command
        self._dynamics.update(const.stepDuration)
```

## Creating a new robot ##

The easiest way to create a new robot is to derive the `robot` class and
set its `dynamics` and `supervisor` attributes.

# Supervisor basics #

Supervisors are in charge of controlling robots.

To do so, they must at least  provide a method `execute(robotInfo, dt)`
which takes as arguments a structure containing informations about the
current state of the robot and the steps duration. It must return a set
of two values which are the linear velocity `v` and the angular velocity `w`
to apply the robot's wheels.

The `execute(robotInfo, dt)` method is called in the `advance` method of the
robot to calculate how robot shall evolve.

## Creating a new supervisor ##

The easiest way to create a new supervisor is to derive the `supervisor` class
and implement its `execute` method.

An example of a supervisor's execute method:

```python
    def execute(self, robotInfo_, dt_):
        # Execute planner to update goal if necessary
        self._planner.execute(robotInfo_, dt_)

        # Process state info
        self.processStateInfo(robotInfo_)

        # Switch:
        if self._current in self._states:
            for f, c in self._states[self._current]:
                if f():
                    c.restart()
                    self._current = c
                    print "Switched to {}".format(c.__class__.__name__)
                    break

        #execute the current controller
        return self._current.execute(self.info(), dt_)
```

## Using a planner ##

A default **goal** point is provided to the `supervisor`.

It's possible to register a `planner` to the `supervisor`. The
`execute` method of the `planner` is called at the beginning of
each `execute` method and is in charge of providing a **goal** point.
This **goal** can be a new one or a different one according to the selected
strategy.

The `planner` have access to the exact same information as the `supervisor`.
That is, the **robot info structure**.

# Dynamic basics #

For now, only the differential drive dynamics is supported.
