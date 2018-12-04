class PheromoneMatrix:

    def __init__(self, size, rho):
        self.rho = rho # indice de evaporacao dos feromonios
        self.matrix = []
        for i in range(size):
            self.matrix.append([])
            for j in range(size):
                self.matrix[i].append(1)
    
    def get(self, i, j):
        return self.matrix[i][j]

    def evaporate_pheromones(self):
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[0])):
                self.matrix[int(i)][int(j)] *= self.rho
    
    def increase(self, i, j, value):
        self.matrix[i][j] += value
    