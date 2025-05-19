from pyiron_workflow import as_function_node


@as_function_node
def product(x: float | int, y: float | int) -> float | int:
    result = x * y
    return result
