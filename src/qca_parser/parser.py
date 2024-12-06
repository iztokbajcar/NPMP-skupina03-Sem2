class QCAParser:
    """The .qca file parser object."""

    def __init__(self):
        self.version = None
        self.cells = []
        self.filename = None
        self.current_sections = []

    def push_section(self, section):
        """Pushes the section name to the top of the sections stack.

        Args:
            section (str): Section name.
        """
        print(f"Entering section [{section}]")
        self.current_sections.append(section)

    def try_pop_section(self, section):
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
            print(f"Leaving section [{section}]")
            self.current_sections.pop()
            return True

    def parse(self, filename):
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

                elif line.startswith("[") and line.endswith("]"):
                    section = line[1:-1]
                    self.push_section(section)

        return None


if __name__ == "__main__":
    parser = QCAParser()
    parser.parse("example_majoritygate.qca")
