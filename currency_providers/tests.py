import unittest


class SimpleTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass


    def test_get_provider(self):
        provider_to_get = "mock"
