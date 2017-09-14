import unittest
import numpy as _np
from Tdbempp.waves import GaussianIncidentWave


class TestWaves(unittest.TestCase):
    def test_gaussian_incident_wave(self):
        dims = _np.array([1,2,3])
        first_wave = GaussianIncidentWave(10,dims,10,10,10)
        points = _np.array([0,1,2])
        val = first_wave.value(10,points)
        self.assertFalse(list(val) == list(points)) # TODO, correct with the correct command for a 3x3 array

if __name__ == '__main__':
    unittest.main()
