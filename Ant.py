# from Graph import Graph
from PheromoneMatrix import PheromoneMatrix
from numpy.random import choice

class Ant:

    def __init__(self, graph):
        self.graph = graph
        self.passed = []
        self.path = []
        for i in range(graph.size):
            self.passed.append(False)

    def find_circuit(self, start=0):
        c = [start]
        self.passed[start] = True
        for i in range(self.graph.size - 1):
            c.append(self.find_next(c[-1]))
        c.append(start)
        self.path = c
        return c

    def find_next(self, vertex):
        neighbors = self.graph.neighboors_of(vertex)
        possibles = self.remove_passed(neighbors)
        prob = self.calc_probs(vertex, possibles)
        # print("probs", prob)
        draw = choice(possibles, 1, p=prob)[0]
        # print("escolha", draw)

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
        #TODO calcular usando alpha e beta
        ph = self.graph.pm.get(a, b)
        (_, d) = self.graph.get(a, b)

        return ((ph**self.graph.alpha) * (1/d ** self.graph.beta))
