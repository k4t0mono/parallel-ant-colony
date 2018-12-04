from Graph import Graph
from PheromoneMatrix import PheromoneMatrix
from Ant import Ant
from Plot import plot
from pprint import pprint
import sys
from mpi4py import MPI

if __name__ == "__main__":
    # Graph(num Formigas, Gerações, alpha, beta, rho)
    # Alpha: importancia do Pheromonio
    # Beta: importancia maior para distancias
    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()
    # data = None

    # numDataForRank = 10
    # data = [(rank + 1) * i for i in range(numDataForRank)]


    # # Processo busca atualizar dados da variavel em outro processo (deve existir a variavel em todos)
    # data2 = comm.gather(data, root=0)
    # print('Rank: ',rank,', data: ' ,data)
    # print('Rank: ',rank,', data2: ' ,data2)

    g = Graph(100, 20, 1, 1, 0.5)
    points = g.load_from_file2(sys.argv[1])

    print('Rank: {}'.format(rank))
    solution = g.solve()

    print("cost =", solution[0])
    # a = Ant(g)
    # path = a.find_circuit(0)
    # print("caminho:",path)

    # t = g.calc_lenght(path)
    # print(t)

    plot(points, solution[1])

