class Racer:
    def __init__(self, jockey, dino):
        self.jockey = jockey
        self.dino = dino

        self.distance = 0
        self.distances = []
        self.placements = []

    def __str__(self):
        return f"{self.jockey.name} {self.dino.name} {self.distance}"

    def __repr__(self):
        return f"{self.jockey.name} {self.dino.name} {self.distance}"

    def __lt__(self, other):
        # check distances array, going backwards. in case of tie, check cumulative distance by previous round
        i = len(self.distances) - 1

        while True:
            if self.distances[i] < other.distances[i]:
                return True
            elif self.distances[i] > other.distances[i]:
                return False
            else:
                # tiebreaker case, check distance in previous round
                i -= 1

                # reached the beginning, both racers have tied every segment of the race!
                if i == -1:
                    # ERROR
                    return None
