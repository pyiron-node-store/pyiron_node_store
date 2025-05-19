import unittest
from importlib.metadata import entry_points as _entry_points

import pkg_resources

ENTRY_POINTS = [
    {
        "ep": "pyiron_node_store.test_node_1",
        "name": "math",
        "ep_def": "node_template.math",
    },
]


class MyTestCase(unittest.TestCase):
    def setUp(self):
        print("set-up")
        self.entries = pkg_resources.working_set.entries
        self.entry_keys = pkg_resources.working_set.entry_keys
        self.by_key = pkg_resources.working_set.by_key
        distribution = pkg_resources.Distribution(__file__)
        for ep in ENTRY_POINTS:
            entry_point = pkg_resources.EntryPoint.parse(
                f"{ep['name']} = {ep['ep_def']}", dist=distribution
            )
            distribution._ep_map = {ep["ep"]: {ep["name"]: entry_point}}
            pkg_resources.working_set.add(distribution)

    def tearDown(self):
        print("tear down")
        pkg_resources.working_set.entries = self.entries
        pkg_resources.working_set.entry_keys = self.entry_keys
        pkg_resources.working_set.by_key = self.by_key

    def test_something(self):
        print(_entry_points())
        import pyiron_node_store as pns

        self.assertEqual(list(pns.get_pyiron_nodes_dict().keys()), ["nodes"])


if __name__ == "__main__":
    unittest.main()
