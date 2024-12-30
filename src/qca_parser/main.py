from parser import QCAParser
from simulator import Simulator

if __name__ == "__main__":
    parser = QCAParser()
    graph = parser.parse("or.qca")
    parser.visualize_graph()

    simulator = Simulator(graph)
    simulator.simulate(10, 0.01)
    # simulator.simulate(10, 3.1415926535897932384626433)
