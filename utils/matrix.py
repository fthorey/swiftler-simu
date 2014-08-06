#!/usr/bin/python
# coding: utf-8

import numpy as np

def transformationMatrix(dx_, dy_, theta_):
    """Return the 3x3 transformation matrix allowing to convert
    from sensors coordinates to robot coordinates
    """
    #Z-axis ccw rotation transformation matrix
    T = np.array([\
                  [np.cos(theta_), -np.sin(theta_), dx_],\
                  [np.sin(theta_), np.cos(theta_), dy_],\
                  [0, 0, 1.0]])
    return T
