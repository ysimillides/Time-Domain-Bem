"""
This module contains various classes/functions to compute specific information (generating functions, fft)
"""
import numpy as _np



def backward_euler(z):
    """This is the generating function for the backward_euler method. To be called via the appropriate class(es)"""
    return 1 - z


def bdf2(z):
    """This is the generating function for the bdf2 (backwards differentiation formula),
    To be called via the appropriate class(es)"""
    return 1.5 - 2 * z + .5 * z ** 2