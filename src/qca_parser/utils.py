from cell import CellFunction


def parse_cell_function(function: str) -> CellFunction:
    """Parses the given cell function string and returns the
    corresponding CellFunction constant.

    Args:
        function (str): The cell function string, as used in the QCADesigner's .qca files.
        Should be one of "QCAD_CELL_MODE_INPUT", "QCAD_CELL_MODE_OUTPUT", or "QCAD_CELL_MODE_NORMAL".

    Returns:
        CellFunction: The CellFunction object corresponding to the given string.
        If an invalid string is given, the function returns CellFunction.NORMAL.
    """
    if function == "QCAD_CELL_MODE_INPUT":
        return CellFunction.INPUT
    elif function == "QCAD_CELL_MODE_OUTPUT":
        return CellFunction.OUTPUT
    else:
        return CellFunction.NORMAL
