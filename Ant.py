from Graph import Graph
from PheromoneMatrix import PheromoneMatrix
from numpy.random import choice

class Ant:

    def __init__(self, graph: Graph, pm: PheromoneMatrix):
        self.graph = graph
        self.passed = []
        for i in range(graph.size):
            self.passed.append(False)
        self.pm = pm

    def find_circuit(self, start):
        c = [start]
        self.passed[start] = True
        for i in range(self.graph.size - 1):
            c.append(self.find_next(c[-1]))

        return c

    def find_next(self, vertex):
        neighbors = self.graph.neighboors_of(vertex)
        possibles = self.remove_passed(neighbors)
        prob = self.calc_probs(vertex, possibles)
        draw = choice(possibles, 1, p=prob)[0]

        # print(possibles)
        # print(prob)
        # print(draw)

        self.passed[draw] = True
        return draw

    def remove_passed(self, neighbors):
        return [x for x in neighbors if not self.passed[x]]

    def calc_probs(self, vertex, neighbors):
        phs_dict = {}
        sum = 0
        for v in neighbors:
            phs = self.calc_pheromone_strength(vertex, v)
            phs_dict[v] = phs
            sum += phs

        probs = []
        for v in neighbors:
            probs.append(phs_dict[v] / sum)

        return probs

    def calc_pheromone_strength(self, a, b):
        ph = self.pm.get(a, b)
        (_, d) = self.graph.get(a, b)

        return ph * 1/d
