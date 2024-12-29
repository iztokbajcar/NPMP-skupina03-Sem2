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
    if function == "QCAD_CELL_INPUT":
        return CellFunction.INPUT
    elif function == "QCAD_CELL_OUTPUT":
        return CellFunction.OUTPUT
    elif function == "QCAD_CELL_FIXED":
        return CellFunction.FIXED
    else:
        return CellFunction.NORMAL


def const_cell_label_to_polarization(label: str) -> int:
    """Converts a constant cell label (i.e. -1) to a polarization (0 or 1).

    Args:
        label (str): The label of the fixed (constant) cell.

    Returns:
        int: The polarization (0 or 1).
    """
    if float(label) == -1:
        return 0
    else:
        return 1


def manhattan_dist(coords1: tuple[float, float], coords2: tuple[float, float]) -> float:
    """Calculates the manhattan distance between the two given coordinates.

    Args:
        coords1 (tuple[float, float]): The first coordinate.
        coords2 (tuple[float, float]): The second coordinate.

    Returns:
        float: The manhattan distance between the two coordinates.
    """
    return abs(coords1[0] - coords2[0]) + abs(coords1[1] - coords2[1])


def euclidean_dist(coords1: tuple[float, float], coords2: tuple[float, float]) -> float:
    """Calculates the euclidean distance between the two given coordinates.

    Args:
        coords1 (tuple[float, float]): The first coordinate.
        coords2 (tuple[float, float]): The second coordinate.

    Returns:
        float: The euclidean distance between the two coordinates.
    """
    return ((coords1[0] - coords2[0]) ** 2 + (coords1[1] - coords2[1]) ** 2) ** 0.5
