"""This submodule contains classes/functions that solve various pde's numerically"""
import bempp.api
import numpy as _np



class SolveAcousticHelmholtz(object):

    def __init__(self, wavenumbers, space, n_points, points):

        self._wavenumbers = wavenumbers
        self._space = space
        self._n_points = n_points
        self._points = points
        self._slp = bempp.api.operators.boundary.modified_helmholtz.single_layer(self._space, self._space, self._space,
                                                                                 self._wavenumbers)  # takes variables , domain, range , dual_to_range , wavenumber
        self._slp_pot = bempp.api.operators.potential.modified_helmholtz.single_layer(self._space, self._points, self._wavenumbers)
        #added a points input

    @property
    def wavenumbers(self):
        return self._wavenumbers

    @property
    def space(self):
        return self._space

    @property
    def n_points(self):
        return self._n_points

    @property
    def slp(self):
        return self._slp

    @property
    def slp(self):
        return self._slp

    def solve_single_layer(self, boundary_data): #boundary data is a python callable, n_points=number of evaluation points dimensions= dimensions of the points.

        dirichlet_fun = bempp.api.GridFunction(self._space, coefficients=boundary_data)  #get values from a python callable?

        lhs = self._slp

        rhs = dirichlet_fun

        neumann_fun, info = bempp.api.linalg.gmres(lhs, rhs, tol=1E-3)  # if everything works correctly, info = 0
        if info != 0:
            raise Exception("Convolution failed")

        u_evaluated = (self._slp_pot * neumann_fun).ravel()
        u_evaluated = u_evaluated.reshape([self._n_points, self._n_points])

        return u_evaluated