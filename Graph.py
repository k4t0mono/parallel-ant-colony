import math
import pprint
from PheromoneMatrix import PheromoneMatrix
from Ant import Ant
from mpi4py import MPI

class Graph:

    # Graph(num Formigas, Gerações, alpha, beta, rho)
    
    def __init__(self, num_ants, generations, alpha, beta, rho):
        self.alpha = alpha      # Alpha: importancia do Pheromonio
        self.beta = beta        # Beta: importancia maior para distancias
        self.rho = rho          # Grau de evaporação de feromonio
        self.adj_matrix = []    
        self.num_ants = num_ants
        self.generations = generations

        # Controle dos processos existentes
        self.comm = MPI.COMM_WORLD
        self.rank = self.comm.Get_rank()

    # Encontra uma solução de acordo com a quantidade de gerações
    def solve(self):
        # melhor custo
        best_cost = None
        # melhor solução
        best_solution = []

        # Paraleelismo é feito nessas gerações
        # Calculando uma media  da matriz de feromonio a cada geração
        for gen in range(self.generations):
            ants = [Ant(self) for i in range(self.num_ants)]
            for ant in ants:
                path = ant.find_circuit()
                cost = self.calc_lenght(path)
                # Melhor solução encontrada  é referente ao melhor custo tido
                # Calculo de quanto foi o custo é referente ao find_circuito
                if(best_cost == None):
                    best_cost = cost
                    best_solution = path
                elif(best_cost > cost):
                    best_cost = cost
                    best_solution = path
            # Manda para todos processos a matriz media de feromonio para calculo da proxima geração
            self.update_pheromone_matrix(ants)
            print('Rank: {:1d} - fim da geração {:3d}'.format(self.rank, gen))

        # retorna o melhor custo encontrado
        return (best_cost, best_solution)
                
    # Atualiza a matrix de feromonio levando em consideração a quantidade de formigas 
    # que passaram por ai e tambem a evaporação do feromonio
    def update_pheromone_matrix(self, ants):
        self.pm.evaporate_pheromones()
        for ant in ants:
            for k in range(1, len(ant.path)):
                i = ant.path[k - 1]
                j = ant.path[k]
                self.pm.increase(i, j, 1)
        print(self.pm.matrix[0])
        self.update_global()
    
    # Reunindo os valores ao processo pai
    def update_global(self):
        print('Rank {} antes do bcast: {}'.format(self.rank, self.pm.matrix[0]))

        # Processo pai pega todos valores dos outros processos
        pm2 = self.comm.gather(self.pm.matrix, root=0)
        
        # Calculando uma matriz media para a matriz de feromonio
        if(self.rank == 0):
            for m in pm2[1:]:
                for i in range(self.size):
                    for j in range(self.size):
                        self.pm.matrix[i][j] += m[i][j]
        
            for i in range(self.size):
                    for j in range(self.size):
                        self.pm.matrix[i][j] /= self.comm.Get_size()

        # Envia os dados a todos outros processos para atualizarem essa matriz de feromonio para a matriz media
        self.pm.matrix = self.comm.bcast(self.pm.matrix, root=0)
        print('Rank {} fim do bcast: {}'.format(self.rank, self.pm.matrix[0]))

    # Calcula o tamanho do circuito
    def calc_lenght(self, circuit):
        total = 0
        for i in range(len(circuit) - 1):
            total += self.get(circuit[i], circuit[i+1])[1]
        return total

    # Calcula a distancia entre dois vertices
    # (levando em consideração os valores x e y no plano cartesiano)
    def distance(self, city1: dict, city2: dict):
        return math.sqrt((city1['x'] - city2['x']) ** 2 + (city1['y'] - city2['y']) ** 2)
    
    # Pega os dados a partir de um arquivo criando a matrix de feromonio
    def load_from_file(self, path):
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
        return points

    # Visinhos de saida para grafo direcionado
    def out_neighboors_of(self, index):
        n = []
        for j in range(self.size):
            if self.adj_matrix[index][j][0] > 0:
                n.append(j)
        return n

    # Vizinhos de entrada para grafo direcionado
    def in_neighboors_of(self, index):
        n = []
        for i in range(self.size):
            if self.adj_matrix[i][index][0] > 0:
                n.append(i)

        return n

    # Todos vizinhos a um nó
    def neighboors_of(self, index):
        n = self.in_neighboors_of(index) + self.out_neighboors_of(index)
        return list(set(n))

    # Captura um valor da matriz
    def get(self, i, j):
        return self.adj_matrix[i][j]
