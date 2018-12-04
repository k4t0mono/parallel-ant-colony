from Graph import Graph
from PheromoneMatrix import PheromoneMatrix
from Ant import Ant
from Plot import plot
from pprint import pprint
import sys

if __name__ == "__main__":
    g = Graph(10,100, 1,10, 10)
    points = g.load_from_file2(sys.argv[1])

    solution = g.solve()

    print("cost =", solution[0])
    # a = Ant(g)
    # path = a.find_circuit(0)
    # print("caminho:",path)

    # t = g.calc_lenght(path)
    # print(t)

    plot(points, solution[1])

