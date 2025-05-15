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


def _find_entry_points():
    registered_nodes = {}
    for node in _entry_points():
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


def get_pyiron_nodes_dict():
    result = {}
    for path, module in _SUB_MODULES.items():
        work = result
        work_before = result
        key = None
        for key in path.split("."):
            work_before = work
            if key in work:
                work = work[key]
            else:
                work[key] = {}
                work = work[key]
        work_before[key] = module
    return result


for _module_path_list, _entry_point in _find_entry_points().items():
    _mod_path, _mod_name = _gen_name(_module_path_list)
    if _mod_path not in _SUB_MODULES:
        _gen_sub_module(_module_path_list[1:-1])
    setattr(_SUB_MODULES[_mod_path], _mod_name, _entry_point.load())
