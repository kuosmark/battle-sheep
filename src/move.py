class Move:
    def __init__(self, pasture, target, sheep) -> None:
        self.pasture = pasture
        self.target = target
        self.sheep = sheep

    def is_initial(self):
        return self.target is None
