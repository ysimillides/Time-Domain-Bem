"""This module contains classes/functions to define waves/boundary waves.
Waves will be defined in classes to allow expansion at a later point if necessary.
"""
import numpy as _np

class AcousticBoundaryWave(object):

    pass

class GaussianIncidentWave(object):

    def __init__(self,frequency, direction, speed, tp, sigma):

        self._frequency = frequency
        self._direction = direction.reshape(-1,1) # _np transpose does not work for a 1dimensional array
        self._speed = speed
        self._tp = tp
        self._sigma = sigma #sigma stands for what variable?

    def value (self, time, points):

        theta = (self._direction[0]*points[0]+self._direction[1]*points[1]+self._direction[2]*points[2]) / self._speed
        trig = _np.cos(2 * _np.pi * (time - theta) * self._frequency)
        zeta = (time-self._tp-theta)**2
        sigma_squared = self._sigma**2
        exp = _np.exp(-1 * (zeta) / (2 * sigma_squared))
        value = 1 * trig * exp
        return value
