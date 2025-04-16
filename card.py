class card:
    def __init__(self, rank, color):
        self.rank = rank
        self.color = color
        pass

    def show(self):
        print(f"| {self.rank} of {self.color} |")

