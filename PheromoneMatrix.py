class PheromoneMatrix:

    def __init__(self, size):
        self.matrix = []
        for i in range(size):
            self.matrix.append([])
            for j in range(size):
                self.matrix[i].append(1)
    
    def get(self, i, j):
        return self.matrix[i][j]