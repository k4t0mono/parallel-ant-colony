class Graph:

    def __init__(self, size):
        self.size = size

        self.adj_matrix = []
        for i in range(size):
            self.adj_matrix.append([])
            for j in range(size):
                self.adj_matrix[i].append((0, 0))

    def calc_lenght(self, circuit):
        total = 0
        for i in range(len(circuit) - 1):
            total += self.get(circuit[i], circuit[i+1])[1]

        total += self.get(circuit[-1], circuit[0])[1]
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
