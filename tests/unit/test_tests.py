import unittest

import pyiron_node_store


class TestVersion(unittest.TestCase):
    def test_version(self):
        version = pyiron_node_store.__version__
        print(version)
        self.assertTrue(version.startswith("0"))
