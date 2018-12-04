#!/usr/bin/python
# -*- coding: utf-8 -*-

from Graph import Graph
from PheromoneMatrix import PheromoneMatrix
from Ant import Ant
from Plot import plot, plot2
from pprint import pprint
import sys
from mpi4py import MPI

if __name__ == "__main__":
    if len(sys.argv) < 7:
        print('{} <test> <num-formigas> <num-geracaos> <alpha> <beta> <rho>'.format(sys.argv[0]))
        sys.exit(1)

    # Alpha: importancia do Pheromonio
    # Beta: importancia maior para distancias
    
    # capturando os valores globais do paralelismo 
    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()
    
    # print(sys.argv[2], size)
    num_ants = int(int(sys.argv[2]) / size)
    # Gerando um Graph
    # Graph(num Formigas, Gerações, alpha, beta, rho)
    g = Graph(num_ants, int(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]), float(sys.argv[6]))

    # Carrega o grafo do arquivo passado como parametro
    points = g.load_from_file(sys.argv[1])

    # Imprime a solução
    print('Rank: {}'.format(rank))
    solution = g.solve()

    g.update_global()
    results = comm.gather(solution, root=0)
    if rank == 0:
        results.sort()
        # Imprimindo o custo da solução
        print("cost =", results[0][0])

        # Plotando grafo do caminho encontrado
        plot(points, results[0][1], int(sys.argv[7]))
        plot2(points, g.pm.matrix, int(sys.argv[7]))

