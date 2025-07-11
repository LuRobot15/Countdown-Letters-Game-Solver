import unittest
from Tests.test_CreateDict import TestCreateDict
from Tests.test_CountdownSolver import TestCountdownSolver
from Tests.CLI.test_Main import TestMain


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
