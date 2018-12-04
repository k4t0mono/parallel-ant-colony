import math
import pprint
from PheromoneMatrix import PheromoneMatrix
from Ant import Ant
from mpi4py import MPI

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
        self.comm = MPI.COMM_WORLD
        self.rank = self.comm.Get_rank()
    
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
            print('Rank: {:1d} - fim da geração {:3d}'.format(self.rank, gen))

        return (best_cost, best_solution)
                
    def update_pheromone_matrix(self, ants):
        self.pm.evaporate_pheromones()
        for ant in ants:
            for k in range(1, len(ant.path)):
                i = ant.path[k - 1]
                j = ant.path[k]
                self.pm.increase(i, j, 1) 
                # TODO coloquei 10 como valor fixo de aumento de feromonios,
                # podemos variar
        print(self.pm.matrix[0])
        self.update_global()
    
    def update_global(self):
        print('Rank {} antes do bcast: {}'.format(self.rank, self.pm.matrix[0]))
        pm2 = self.comm.gather(self.pm.matrix, root=0)

        if(self.rank == 0):
            for m in pm2[1:]:
                for i in range(self.size):
                    for j in range(self.size):
                        self.pm.matrix[i][j] += m[i][j]
        
            for i in range(self.size):
                    for j in range(self.size):
                        self.pm.matrix[i][j] /= self.comm.Get_size()
            
        self.pm.matrix = self.comm.bcast(self.pm.matrix, root=0)
        print('Rank {} fim do bcast: {}'.format(self.rank, self.pm.matrix[0]))


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
