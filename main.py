from Graph import Graph
from PheromoneMatrix import PheromoneMatrix
from Ant import Ant
from Plot import plot
from pprint import pprint
import sys
from mpi4py import MPI

if __name__ == "__main__":
    # Alpha: importancia do Pheromonio
    # Beta: importancia maior para distancias
    
    # capturando os valores globais do paralelismo 
    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()
    
    # Gerando um Graph
    # Graph(num Formigas, Gerações, alpha, beta, rho)
    g = Graph(100, 20, 1, 1, 0.5)

    # Carrega o grafo do arquivo passado como parametro
    points = g.load_from_file(sys.argv[1])

    # Imprime a solução
    print('Rank: {}'.format(rank))
    solution = g.solve()

    # Imprimindo o custo da solução
    print("cost =", solution[0])

    # Plotando grafo do caminho encontrado
    plot(points, solution[1])

