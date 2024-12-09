from cell import Cell
from utils import parse_cell_function


class QCAParser:
    """The .qca file parser object."""

    def __init__(self):
        self.version = None
        self.cells = []
        self.filename = None
        self.current_sections = []
        self.last_cell_x = None
        self.last_cell_y = None
        self.last_cell_function = None
        self.last_cell_clock = None

    def in_section(self, section: str) -> bool:
        """Checks if the given section is currently open.

        Args:
            section (str): Section name.

        Returns:
            bool: Whether the given section is currently open or not.
        """
        return section in self.current_sections

    def last_section(self) -> str:
        """Returns the name of the most recent section.

        Returns:
            str: The name of the most recent section.
        """
        if len(self.current_sections) == 0:
            return None
        return self.current_sections[-1]

    def push_section(self, section: str):
        """Pushes the section name to the top of the sections stack.

        Args:
            section (str): Section name.
        """
        print(f"{(2*len(self.current_sections)) * ' '}[{section}]")
        self.current_sections.append(section)

    def try_pop_section(self, section: str) -> bool:
        """Tries to pop the section name from the sections stack.
        Returns false if the given section name doesn't match the name of the
        top section.

        Args:
            section (str): Section name.

        Returns:
            bool: Whether the operation was successful or not.
        """
        last_section = self.current_sections[-1]

        if section != last_section:
            # the name of the most recent opening tag
            # doesn't match this closing tag
            return False
        else:
            print(f"{(2*(len(self.current_sections)-1)) * ' '}[#{section}]")
            self.current_sections.pop()
            return True

    def handle_opening_tag(self, section: str):
        pass

    def handle_closing_tag(self, section: str):
        if section == "TYPE:QCADCell":
            # save the cell
            cell = Cell(
                self.last_cell_x,
                self.last_cell_y,
                self.last_cell_function,
                self.last_cell_clock,
            )
            self.cells.append(cell)
            print(f"Parsed cell: {cell}")

    def _get_min_cell_x(self) -> float:
        """Returns the minimum x coordinate of all cells in the design."""
        return min([cell.x for cell in self.cells])

    def _get_min_cell_y(self) -> float:
        """Returns the minimum y coordinate of all cells in the design."""
        return min([cell.y for cell in self.cells])

    def _get_min_cell_x_distance(self) -> float:
        """Returns the minimum x distance between two cells in the design.

        Returns:
            float: The minimum x distance between two cells.
        """
        return min(
            [abs(a.x - b.x) for a in self.cells for b in self.cells if a.x != b.x]
        )

    def _get_min_cell_y_distance(self) -> float:
        """Returns the minimum y distance between two cells in the design.

        Returns:
            float: The minimum y distance between two cells.
        """
        return min(
            [abs(a.y - b.y) for a in self.cells for b in self.cells if a.y != b.y]
        )

    def construct_graph(self, cells: list[Cell]) -> None:
        min_x_dist = self._get_min_cell_x_distance()
        print(min_x_dist)

    def parse(self, filename: str) -> None:
        """Parses the file with the given filename.

        Args:
            filename (string): The filename of the file to be parsed. Should end in .qca.

        Returns:
            None: The parsed design object. Currently always None, TODO implement a better representation.
        """
        self.filename = filename

        with open(filename, "r") as f:
            for line_no, line in enumerate(f):
                line = line.strip()

                # skip empty lines
                if len(line) == 0:
                    continue

                if line.startswith("[#") and line.endswith("]"):
                    section = line[2:-1]

                    if not self.try_pop_section(section):
                        print(
                            f"ERROR: closing tag ({section}) doesn't match the previous opening tag ({last_section})."
                        )
                        return None

                    self.handle_closing_tag(section)

                elif line.startswith("[") and line.endswith("]"):
                    section = line[1:-1]
                    self.push_section(section)

                    self.handle_opening_tag(section)

                # read cell coordinates
                if (
                    self.in_section("TYPE:QCADCell")
                    and not self.in_section("TYPE:CELL_DOT")
                    and not self.in_section("TYPE:QCADLabel")
                ):
                    if line.startswith("x="):
                        self.last_cell_x = float(line.split("=")[1])
                        print(f"x={self.last_cell_x}")
                    elif line.startswith("y="):
                        self.last_cell_y = float(line.split("=")[1])
                    elif line.startswith("cell_options.clock="):
                        self.last_cell_clock = int(line.split("=")[1])
                    elif line.startswith("cell_function="):
                        self.last_cell_function = parse_cell_function(
                            line.split("=")[1]
                        )

        # normalize cell coordinates
        min_cell_x = self._get_min_cell_x()
        min_cell_y = self._get_min_cell_y()
        min_cell_x_dist = self._get_min_cell_x_distance()
        min_cell_y_dist = self._get_min_cell_y_distance()
        print("Min x:", min_cell_x)
        print("Min y:", min_cell_y)
        print("Min x distance:", min_cell_x_dist)
        print("Min y distance:", min_cell_y_dist)

        for c in self.cells:
            c.x -= min_cell_x
            c.y -= min_cell_y
            c.x /= min_cell_x_dist
            c.y /= min_cell_y_dist

        print("*****")
        print(f"File {filename} parsed successfully, got {len(self.cells)} cells.")
        for c in self.cells:
            print(c)
        print("*****")

        return None


if __name__ == "__main__":
    parser = QCAParser()
    parser.parse("example_majoritygate.qca")
