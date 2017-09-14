import unittest
import numpy as _np
import Tdbempp.structures
from Tdbempp.convolution_quadrature import bdf2,backward_euler
epsilon = _np.finfo(float).eps


class TestStructures(unittest.TestCase):
    """
    This class tests that the structures functions properly, raising the required error messages where relevant,
    and that the change_in_time(dt), and the time steps are created as expected
    """

    """The following two tests, test that the change in time(dt) is calculated correctly.
    The first test tests that the time steps is created properly, and the second that it is not)"""

    def test_change_in_time1(self):
        ES=Tdbempp.structures.EquispacedTimeStepsToFrequencyFactory(10,bdf2,10,20, 10, 10)
        self.assertAlmostEqual(2, ES.dt, delta=epsilon)

    def test_change_in_time2(self):
        ES = Tdbempp.structures.EquispacedTimeStepsToFrequencyFactory(10,backward_euler,10,20, 10, 10)
        self.assertNotAlmostEqual(4, ES.dt, delta=epsilon)

    """The following two tests, test that the time_steps (array) creation behaves as expected. The first test checks
    that the time_steps are created correctly, and the second test that they're not"""

    def test_time_step_creation1(self):
        ES=Tdbempp.structures.EquispacedTimeStepsToFrequencyFactory(10, bdf2, 10, 40, 41, 10)
        self.assertSequenceEqual(list(ES.time_steps), list(_np.linspace(0,40,num=41)))

    def test_time_step_creation2(self):
        ES = Tdbempp.structures.EquispacedTimeStepsToFrequencyFactory(10, bdf2, 10, 40, 41, 10)
        self.assertFalse(list(ES.time_steps) == list(_np.linspace(0, 40, num=44)))

    """The following two tests, test that the frequency (array) creation behaves as expected. The first test checks
        that the frequency are created correctly, and the second test that they're not"""

    def test_frequency_creation1(self):
        Freq=Tdbempp.structures.EquispacedTimeStepsToFrequencyFactory(10, bdf2, 10, 10,10,100)
        Freq=Freq.frequencies
        self.assertSequenceEqual(list(Freq), list(_np.arange(100)))

    def test_frequency_creation2(self):
        Freq = Tdbempp.structures.EquispacedTimeStepsToFrequencyFactory(10, bdf2, 10, 10, 10, 100)
        Freq = Freq.frequencies
        self.assertFalse(list(Freq) == list(_np.arange(1000)))

    """The following  tests, test that errors are raised where expected (such as not implemented in these cases)"""

    def test_raise_error_time_steps(self):
        ES=Tdbempp.structures.FrequencyFactoryBase(1,2,3)
        with self.assertRaises(NotImplementedError):
            ES.time_steps

    def test_raise_error_final_time(self):
        ES = Tdbempp.structures.FrequencyFactoryBase(1, 2, 3)
        with self.assertRaises(NotImplementedError):
            ES.final_time

    def test_raise_error_number_of_time_steps(self):
        ES = Tdbempp.structures.FrequencyFactoryBase(1, 2, 3)
        with self.assertRaises(NotImplementedError):
            ES.number_of_time_steps

    def test_raise_error_evaluate_time_domain_boundary_data(self):
        ES = Tdbempp.structures.TimeDomainBoundaryData(1,2)
        with self.assertRaises(NotImplementedError):
            ES.evaluate(2)


if __name__ == '__main__':
    unittest.main()
