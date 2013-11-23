#!/usr/bin/python
# coding: utf-8

class Pos2D(object):
    """
    """

    def __init__(self, x_, y_, theta_):
        """
        """
        self.x = x_
        self.y = y_
        self.theta = theta_

    def getX(self, ):
        """
        """
        return self.x

    def getY(self, ):
        """
        """
        return self.y

    def getTheta(self, ):
        """
        """
        return self.theta

    def setX(self, x_):
        """
        """
        self.x = x_

    def setY(self, y_):
        """
        """
        self.y = y_

    def setTheta(self, theta_):
        """
        """
        self.theta = theta_

    def setPose(self, pose_):
        """
        """
        self.x = pose_.getX()
        self.y = pose_.getY()
        self.theta = pose_.getTheta()

    def unPack(self,):
        return self.x, self.y, self.theta
