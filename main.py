from Graph import Graph
from PheromoneMatrix import PheromoneMatrix
from Ant import Ant
from pprint import pprint
import sys

if __name__ == "__main__":
    g = Graph(5)
    g.load_from_file(sys.argv[1])
    p = PheromoneMatrix(5)

    a = Ant(g, p)
    c = a.find_circuit(0)
    print(c)

    t = g.calc_lenght(c)
    print(t)
