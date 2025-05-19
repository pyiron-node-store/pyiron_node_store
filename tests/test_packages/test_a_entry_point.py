import unittest
import pyiron_node_store


class MyTestCase(unittest.TestCase):
    def test_entry_point_keys(self):
        self.assertEqual([n for n in pyiron_node_store.get_pyiron_nodes_dict()], ["nodes"])


if __name__ == '__main__':
    unittest.main()
