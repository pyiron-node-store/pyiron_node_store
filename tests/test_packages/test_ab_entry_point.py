import unittest

import pyiron_node_store


class MyTestCase(unittest.TestCase):
    def test_entry_point_keys(self):
        self.assertEqual(
            {
                key: [node for node in dir(value) if not node.startswith("_")]
                for key, value in pyiron_node_store._SUB_MODULES.items()
            },
            {
                "nodes": ["math", "prod", "sum"],
                "mathematics": ["prod", "sum", "sum_b"],
                "some": "long",
                "some.long": "package",
                "some.long.package": ["path"],
                "some.long.package.path": ["sum"],
            },
        )


if __name__ == "__main__":
    unittest.main()
