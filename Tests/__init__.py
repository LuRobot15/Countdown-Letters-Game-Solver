import unittest
from .test_createDict import TestCreateDict
from .test_main import TestMain
from .test_countdownSolver import TestCountdownSolver

def suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(TestCreateDict))
    suite.addTest(loader.loadTestsFromTestCase(TestMain))
    suite.addTest(loader.loadTestsFromTestCase(TestCountdownSolver))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    test_suite = suite()
    runner.run(test_suite)
