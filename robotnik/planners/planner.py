#!/USSR/bin/python
# coding: utf-8

from utils.struct import Struct

class Planner(object):
    """The planner class provides goal point to the supervisor which
    oversees the control of a single robot.
    """

    def __init__(self, ):
        """
        """
        self._goal = {}
        self._goal["x"] = -5
        self._goal["y"] = -5

    def getGoal(self, ):
        return self._goal

    def execute(self, robotInfo_, dt_):
        """
        """
        # Nothing to do for now.
