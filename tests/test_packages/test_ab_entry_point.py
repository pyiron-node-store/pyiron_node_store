import unittest

import pyiron_node_store


def process_pyiron_nodes_dict(pyiron_nodes_dict):
    result = {}
    for group in pyiron_nodes_dict:
        module = pyiron_nodes_dict[group]
        result[group] = [node for node in dir(module) if not node.startswith("_")]
    return result


class MyTestCase(unittest.TestCase):
    def test_entry_point_keys(self):
        self.assertEqual(
            process_pyiron_nodes_dict(pyiron_node_store.get_pyiron_nodes_dict()),
            {
                "nodes": ["math", "sum", "prod"],
                "mathematics": ["sum", "sum_b", "prod"],
                "some.long.package.path": ["sum"],
            },
        )


if __name__ == "__main__":
    unittest.main()
