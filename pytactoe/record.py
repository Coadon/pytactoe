from constants import RoundResult


class RoundRecord:
    def __init__(self, starting_side: str):
        self.starting_side = starting_side
        self.result: RoundResult = RoundResult.Undetermined
        self.won_on_time: bool = False
        self.moves = []

    def add_move(self, move: tuple[int, int]):
        self.moves.append((move[0], move[1]))

    def conclude(self, result: RoundResult, won_on_time: bool):
        self.result = result
        self.won_on_time = won_on_time

    def __repr__(self):
        s = "X" if self.starting_side == "X" else "O"
        for move in self.moves:
            s += f"{move[0]}{move[1]}"
        return s


