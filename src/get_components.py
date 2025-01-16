from qca_parser.parser import QCAParser

class GetComponents:

    def __init__(self, component_names=None):
        self.components = {}
        if not component_names:
            component_names = ['negator', 'and', 'or' , 'majority', '1bit_fulladder', '4bit_fulladder']
        self.component_names = component_names

    def get_components(self):
        '''
            For every component in component_names returns a QCAParser object, parsed from a file {component}.qca.
        '''
        for component in self.component_names:
            parser = QCAParser()
            parser.parse(f"src/komponente_QCA_files/{component}.qca")
            self.components[component] = parser

# primer
if __name__ == "__main__":
    get_components = GetComponents()
    get_components.get_components()
    components = get_components.components
    components['1bit_fulladder'].visualize_graph()



