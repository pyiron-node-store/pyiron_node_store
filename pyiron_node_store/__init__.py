import importlib as _importlib
import sys as _sys
import types as _types
from importlib.metadata import entry_points as _entry_points

from ._version import get_versions as _get_versions

# might be very interesting to get tests at some point:
# https://stackoverflow.com/questions/40514205/how-to-dynamically-add-and-load-entry-points

__version__ = _get_versions()["version"]


del _get_versions

_MODULE_NAME = "pyiron_node_store"
_DEFAULT_SUB_MODULE_NAME = "nodes"

nodes = _types.ModuleType(_DEFAULT_SUB_MODULE_NAME)
_SUB_MODULES = {_DEFAULT_SUB_MODULE_NAME: nodes}
_ENTRY_POINTS: dict[dict] = {}


def _find_entry_points():
    registered_nodes = {}
    _ep = _entry_points()
    if _ep.__class__.__name__ == "SelectableGroups":
        _ep = [node for group in _ep.groups for node in _ep[group]]
    for node in _ep:
        if node.group.startswith(_MODULE_NAME):
            module = tuple(node.group.split(".") + [node.name])
            if module in registered_nodes:
                print(
                    f"Name clash! Will overwrite {module} with currently registered "
                    f"node {registered_nodes[module]} with new node {node}!"
                )
            registered_nodes[module] = node

    return registered_nodes


def _gen_name(module_path_list):
    if len(module_path_list) == 2:
        if module_path_list[0] != _MODULE_NAME:
            raise ValueError(
                f"Unintended use, module path must start with {_MODULE_NAME},"
                f"but got {module_path_list}."
            )
        return _DEFAULT_SUB_MODULE_NAME, module_path_list[1]
    else:
        return ".".join(module_path_list[1:-1]), module_path_list[-1]


def _gen_sub_module(module_path_list):
    _full_name = ".".join(module_path_list)
    _parent_mod_path = ".".join(module_path_list[:-1])
    _new_mod_name = module_path_list[-1]
    if _parent_mod_path not in _SUB_MODULES and _parent_mod_path != "":
        _gen_sub_module(module_path_list[:-1])

    _mod = _types.ModuleType(_new_mod_name)
    if _parent_mod_path == "":
        globals()[_new_mod_name] = _mod
    else:
        setattr(_SUB_MODULES[_parent_mod_path], _new_mod_name, _mod)
    _SUB_MODULES[_full_name] = _mod


def _flatten_to_nested(flat_dict):
    """
    Converts a flat dictionary with tuples as keys into a nested dictionary.

    Args:
        flat_dict (dict): A dictionary where the keys are tuples of strings.
                           e.g., {('some','path'): 'val1', ('some','other','path'):'val2'}

    Returns:
        dict: A nested dictionary reflecting the structure of the tuple keys.
              e.g., {'some': {'path': 'val1', 'other':{'path': 'val2'}}}
    """
    nested_dict = {}
    for keys, value in flat_dict.items():
        current_level = nested_dict
        for i, key in enumerate(keys):
            if i == len(keys) - 1:
                current_level[key] = value
            else:
                if key not in current_level:
                    current_level[key] = {}
                current_level = current_level[key]
    return nested_dict


def get_pyiron_nodes_dict():
    return _flatten_to_nested(_ENTRY_POINTS)


for _module_path_list, _entry_point in _find_entry_points().items():
    _mod_path, _mod_name = _gen_name(_module_path_list)
    if _mod_path not in _SUB_MODULES:
        _gen_sub_module(_module_path_list[1:-1])
    setattr(_SUB_MODULES[_mod_path], _mod_name, _entry_point.load())
    _ENTRY_POINTS[_module_path_list] = {
        "ep": _entry_point,
        "file": _importlib.util.find_spec(_entry_point.value).origin,
        "path_tuple": _module_path_list,
    }
