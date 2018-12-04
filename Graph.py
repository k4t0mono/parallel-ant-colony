import math
import pprint
from PheromoneMatrix import PheromoneMatrix
from Ant import Ant

class Graph:

    def __init__(self, num_ants, generations, alpha, beta, rho):
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        # self.size = size
        # self.pm = PheromoneMatrix(size, 0.5)
        self.adj_matrix = []
        # for i in range(size):
        #     self.adj_matrix.append([])
        #     for j in range(size):
        #         self.adj_matrix[i].append((0, 0))
        self.num_ants = num_ants
        self.generations = generations
    
    def solve(self):
        best_cost = None
        best_solution = []

        for gen in range(self.generations):
            ants = [Ant(self) for i in range(self.num_ants)]
            for ant in ants:
                path = ant.find_circuit()
                cost = self.calc_lenght(path)
                if(best_cost == None):
                    best_cost = cost
                    best_solution = path
                elif(best_cost > cost):
                    best_cost = cost
                    best_solution = path
            self.update_pheromone_matrix(ants)

        return (best_cost, best_solution)
                

    # def solve(self, graph: Graph):
    #     """
    #     :param graph:
    #     """
    #     best_cost = float('inf')
    #     best_solution = []
    #     for gen in range(self.generations):
    #         # noinspection PyUnusedLocal
    #         ants = [_Ant(self, graph) for i in range(self.ant_count)]
    #         for ant in ants:
    #             for i in range(graph.rank - 1):
    #                 ant._select_next()
    #             ant.total_cost += graph.matrix[ant.tabu[-1]][ant.tabu[0]]
    #             if ant.total_cost < best_cost:
    #                 best_cost = ant.total_cost
    #                 best_solution = [] + ant.tabu
    #             # update pheromone
    #             ant._update_pheromone_delta()
    #         self._update_pheromone(graph, ants)
    #         # print('generation #{}, best cost: {}, path: {}'.format(gen, best_cost, best_solution))
    #     return best_solution, best_cost

    def update_pheromone_matrix(self, ants):
        self.pm.evaporate_pheromones()
        for ant in ants:
            for k in range(1, len(ant.path)):
                i = ant.path[k - 1]
                j = ant.path[k]
                self.pm.increase(i, j, 10) 
                # TODO coloquei 10 como valor fixo de aumento de feromonios,
                # podemos variar


    def calc_lenght(self, circuit):
        total = 0
        for i in range(len(circuit) - 1):
            total += self.get(circuit[i], circuit[i+1])[1]

        return total

    def load_from_file(self, path):
        with open(path) as fl:
            lns = fl.read().split('\n')

        data = []
        for ln in lns:
            data.append(ln.split(' '))

        for i in range(self.size):
            for j in range(self.size):
                dt = data[i][j].split(',')
                self.adj_matrix[i][j] = (int(dt[0]), int(dt[1]))
    
    def distance(self, city1: dict, city2: dict):
        return math.sqrt((city1['x'] - city2['x']) ** 2 + (city1['y'] - city2['y']) ** 2)
    
    def load_from_file2(self, path):
        
        self.adj_matrix = []
        cities = []
        points = []
        with open(path) as f:
            for line in f.readlines():
                city = line.split(' ')
                cities.append(dict(index=int(city[0]), x=int(city[1]), y=int(city[2])))
                points.append((int(city[1]), int(city[2])))
        rank = len(cities)
        self.size = len(cities)
        self.pm = PheromoneMatrix(self.size, self.rho)
        for i in range(rank):
            row = []
            for j in range(rank):
                if(i != j):
                    row.append((1, self.distance(cities[i], cities[j])))
                else:
                    row.append((0, 0))

            self.adj_matrix.append(row)
        # pprint.pprint(self.adj_matrix)

        return points

    def out_neighboors_of(self, index):
        n = []
        for j in range(self.size):
            if self.adj_matrix[index][j][0] > 0:
                n.append(j)

        return n

    def in_neighboors_of(self, index):
        n = []
        for i in range(self.size):
            if self.adj_matrix[i][index][0] > 0:
                n.append(i)

        return n

    def neighboors_of(self, index):
        n = self.in_neighboors_of(index) + self.out_neighboors_of(index)
        return list(set(n))

    def get(self, i, j):
        return self.adj_matrix[i][j]
