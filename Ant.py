#!/usr/bin/python
# -*- coding: utf-8 -*-

from PheromoneMatrix import PheromoneMatrix
from numpy.random import choice

class Ant:
    
    # Construtor da classe Ant
    def __init__(self, graph):
        self.graph = graph
        self.passed = []
        self.path = []
        for i in range(graph.size):
            self.passed.append(False)

    # Metodo para encontrar um circuito a partir do vertice inicial (start)
    def find_circuit(self, start=0):
        c = [start]
        self.passed[start] = True
        for i in range(self.graph.size - 1):
            c.append(self.find_next(c[-1]))
        c.append(start)
        self.path = c
        return c

    # Decisão do proximo vertice a se seguir
    def find_next(self, vertex):
        neighbors = self.graph.neighboors_of(vertex)
        possibles = self.remove_passed(neighbors)
        prob = self.calc_probs(vertex, possibles)
        draw = choice(possibles, 1, p=prob)[0]

        self.passed[draw] = True
        return draw
    
    # remove da lista de vizinhos os nós já visitados
    def remove_passed(self, neighbors):
        return [x for x in neighbors if not self.passed[x]]

    # Calcula a propabilidade referente a um vizinho deste
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

    # Calcula a força com que o feromonio vai ponderar na probabilidade
    def calc_pheromone_strength(self, a, b):
        ph = self.graph.pm.get(a, b)
        (_, d) = self.graph.get(a, b)

        return ((ph**self.graph.alpha) * (1/d ** self.graph.beta))
