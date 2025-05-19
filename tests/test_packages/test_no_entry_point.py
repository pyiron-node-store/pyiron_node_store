import unittest
import pyiron_node_store


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(pyiron_node_store.get_pyiron_nodes_dict(), {"nodes": {}})


if __name__ == '__main__':
    unittest.main()
