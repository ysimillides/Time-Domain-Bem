import unittest
import Tdbempp.convolution_quadrature

class TestConvolutionQuadrature(unittest.TestCase):
    """This class tests that the functions in the computation module work as expected.  """
    def test_backward_euler(self):
        result = Tdbempp.convolution_quadrature.backward_euler(10)
        self.assertEqual(result, -9)

    def test_backward_euler2(self):
        result = Tdbempp.convolution_quadrature.backward_euler(1)
        self.assertNotEqual(result, 1)

    def test_bdf2(self):
        result = Tdbempp.convolution_quadrature.bdf2(4)
        self.assertEqual(result, 1.5)

    def test_bdf2_2(self):
        result = Tdbempp.convolution_quadrature.bdf2(0)
        self.assertNotEqual(result, 0)

if __name__ == '__main__':
    unittest.main()