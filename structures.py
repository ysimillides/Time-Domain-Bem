"""
This submodule contains various classes to evaluate boundary data from certain frequencies.
"""
from __future__ import division
import numpy as _np
import numpy.fft as fft


class FrequencyFactoryBase(object):
    """Takes parameters speed, generating_function and radius"""
    def __init__(self, speed, generating_function, radius):

        self._speed = speed
        self._generating_function = generating_function
        self._radius = radius

    @property
    def final_time(self):
        raise NotImplementedError("Not implemented.")

    @property
    def number_of_time_steps(self):
        raise NotImplementedError("Not implemented.")

    @property
    def time_steps(self):
        raise NotImplementedError("Not implemented.")

    @property
    def speed(self):
        return self._speed

    @property
    def generating_function(self):
        return self._generating_function

    @property
    def radius(self):
        return self._radius



class EquispacedTimeStepsToFrequencyFactory(FrequencyFactoryBase):
    """
    This class creates equally spaced time steps for use. Takes parameters final_time, number_of_time_steps
    and number_of_frequencies
    """

    def __init__(self,speed,generating_function,radius, final_time, number_of_time_steps, number_of_frequencies):

        super(EquispacedTimeStepsToFrequencyFactory, self).__init__(speed, generating_function, radius)
        self._final_time = final_time
        self._number_of_time_steps = number_of_time_steps
        self._dt = final_time / number_of_time_steps
        self._number_of_frequencies = number_of_frequencies

    @property
    def final_time(self):
        return self._final_time

    @property
    def number_of_time_steps(self):
        return self._number_of_time_steps

    @property
    def dt(self):
        return self._dt

    @property
    def time_steps(self):
        return _np.linspace(
            start=0, stop=self.final_time, num=self._number_of_time_steps
        )

    @property
    def frequency_steps(self):
        return _np.linspace(
            start=0, stop=self.final_time, num=self._number_of_frequencies
        )

    @property
    def frequencies(self):
        return _np.arange(self._number_of_frequencies)

    @property
    def wavenumbers(self):
        zeta = self._radius* _np.exp(2j * _np.pi * _np.arange(self._number_of_frequencies) / self._number_of_frequencies)
        generator = self._generating_function(zeta)
        return generator / (self._speed * self.dt)

    @property
    def zeta(self):
        return self._radius * _np.exp(
            2j
            * _np.pi
            * _np.arange(self._number_of_frequencies)
            / self._number_of_frequencies
        )

    def forward_transform(self,values):
        if self._number_of_frequencies >= self._number_of_time_steps:
            difference = self._number_of_frequencies - self._number_of_time_steps
            time_values = values
            #time_values = _np.vstack([([values]), _np.zeros((difference, values.shape[1]))])  # frequency domain. Laplace for more time_steps
            exponent = _np.arange(self._number_of_frequencies)  # would also work as times, since the frequencie zeros arent altered
            _lambda_ = self._radius ** exponent
            _lambda_ = _lambda_.reshape(-1, 1)
            time_values = fft.fft(_lambda_ * time_values, axis=0)
        if self._number_of_time_steps > self._number_of_frequencies:
            exponent = _np.arange(number_of_time_steps)
            _lambda_ = radius ** exponent
            _lambda_ = _lambda_.reshape(-1, 1)
            time_values = fft.fft(_lambda_ * values, axis=0)
            time_values = time_values[0:number_of_frequencies,:]  # if we are under resolving, we will only have Nf wavelengths to evaluate data on the boundary
        return time_values

    def inverse_transform(self,values):
        if self._number_of_frequencies >= self._number_of_time_steps:
            values = fft.ifft(values, axis=0)
            for i in range(self._number_of_frequencies):  # changed from freqs to time_steps
                _lambda_ = (1 / self._radius) ** i
                values[i, :, :] = _lambda_ * values[i, :, :]  # commented out the radius bit
            result = values[0:self._number_of_time_steps, :,:]  # re-arranged order #changed from 0 to timesteps to difference till end
        return result  # needs to have further calculation of the radius, due to mistake in calculation. changed from time_steps to freqs

class TimeDomainBoundaryData(object):
    """
    This class converts the boundary data into values required. Takes  points and dimensions .
    """
    def __init__(self, points,dimension):

        self._points = points
        self._dimension = dimension

    @property
    def points(self):
        return self._points

    @property
    def dimension(self):
        return self._dimension

    def evaluate(self, time_steps):  # evaluates the boundary data across a set number of points/timesteps

        raise NotImplementedError("Needs to be implemented by subclass.")


class AnalyticTimeDomainBoundaryData(TimeDomainBoundaryData):
    """This class provides access to analytic boundary data specified by a Python callable. Takes points, function and
    dimension"""

    def __init__(self, points, dimension, fun):

        super(AnalyticTimeDomainBoundaryData, self).__init__(points,dimension)
        self._fun = fun

    def evaluate(self, time_steps): # possibly also need frequencies?

        result = _np.zeros((len(time_steps), self.points.shape[1]), dtype='float64') #only evaluates time_steps, pads with zeroes otherwise?
        for index, t in enumerate(time_steps):
            result[index, :] = self._fun.value(t,self.points) # changed from t , points to points,t to try something
        return result
