#!/usr/bin/python
# coding: utf-8

class Controller(object):
    """The Controller class defines a behavior for the supervisor class.
    Any implemention must inherit from this class and implement the
    'execute' method to return a unicycle model output
    """

    def execute(self, state_, goal_, dt_):
        """Given a state estimation and elapsed time,
        calculate and return robot motion parameters

        :param state_: Estimation of the current state of the robot (x,y,theta) (m,m,rad)
        :param dt_: Time elapsed (s) since last call to 'execute'
        """
        raise NotImplementedError("Controller.execute")

    def restart(self, ):
        """Restarts the controller
        """
        raise NotImplementedError("Controller.restart")
