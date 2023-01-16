import unittest
import pytest


@pytest.mark.usefixtures('client_class')
class BaseTestCase(unittest.TestCase):
    pass
