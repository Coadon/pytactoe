from constants import RoundResult


def serialize_square(move: tuple[int, int]) -> int:
    return move[0] + move[1] * 3


def deserialize_square(serialized: int) -> tuple[int, int]:
    return serialized % 3, serialized // 3


class RoundRecord:
    def __init__(self, rec: str):
        self.starting_side = rec[0]
        self.result: RoundResult = RoundResult.Undetermined
        self.won_on_time: bool = False
        self.moves: list[tuple[int, int]] = []
        for i in range(1, len(rec)):
            move = deserialize_square(int(rec[i]))
            self.moves.append(move)

    def add_move(self, move: tuple[int, int]):
        self.moves.append((move[0], move[1]))

    def conclude(self, result: RoundResult, won_on_time: bool):
        self.result = result
        self.won_on_time = won_on_time

    def __repr__(self):
        s = "X" if self.starting_side == "X" else "O"
        for move in self.moves:
            s += str(serialize_square(move))
        return s
