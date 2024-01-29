class Racer:
    def __init__(self, jockey, dino):
        self.jockey = jockey
        self.dino = dino

        self.distance = 0
        self.distances = []

    def __str__(self):
        return f"{self.jockey.name} {self.dino.name} {self.distances[-1]}"
