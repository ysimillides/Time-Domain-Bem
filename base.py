"""This module contains classes/functions that allow us to input the pde/data and get a solution using the various classes"""

import numpy as _np

class PDEToBeSolved(object):

    def __init__(self,pde,boundary_data,solver):

        self._solver = solver
        self._pde = pde
        self._boundary_data = boundary_data

    pass

