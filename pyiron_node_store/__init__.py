from importlib.metadata import entry_points
import sys

from ._version import get_versions

__version__ = get_versions()["version"]

module_name = 'pyiron_node_store'
registered_nodes = {}
for node in entry_points():
    if node.group.startswith(module_name + '.'):
        sub_module = node.group[len(module_name)+1:]
        registered_nodes["pyiron_node_store." + sub_module + '.' + node.name] = node

print(registered_nodes)

sys.modules.update(registered_nodes)