from constants import EX, OH, RoundResult
from histo import RoundRecord
from match import Match
import histo


class Round():
    def __init__(self, match: Match, x_starts: bool = True):
        self.record = RoundRecord("X" if x_starts else "O")

        self.round_over = False
        self.result = RoundResult.Undetermined
        self.won_on_time = False
        self.x_turn = x_starts
        self.grid: list[list[int]] = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.first_move = True
        self.match = match

    def conclude(self, result: RoundResult, on_time=False):
        self.round_over = True
        self.result = result
        self.won_on_time = on_time

        self.record.conclude(result, on_time)
        histo.add_round(self.record)

        if not self.match.use:
            return

        self.match.timer_freeze = True
        if result == RoundResult.XWin:
            self.match.increment_x(1)
        elif result == RoundResult.OWin:
            self.match.increment_o(1)
        elif result == RoundResult.Draw:
            self.match.announce_draw()

    def test_for_full_grid(self):
        for row in self.grid:
            if 0 in row:
                return False
        return True

    def test_for_diagonal_fill(self, side: int):
        return ((self.grid[0][0] == side and self.grid[1][1] == side and self.grid[2][2] == side)
                or (self.grid[0][2] == side and self.grid[1][1] == side and self.grid[2][0] == side))

    def test_for_win(self):
        for row in self.grid:
            if row == [EX, EX, EX]:
                self.conclude(RoundResult.XWin)
                return True
            elif row == [OH, OH, OH]:
                self.conclude(RoundResult.OWin)
                return True
        for col in range(3):
            the_col = [self.grid[0][col], self.grid[1][col], self.grid[2][col]]
            if the_col == [EX, EX, EX]:
                self.conclude(RoundResult.XWin)
                return True
            elif the_col == [OH, OH, OH]:
                self.conclude(RoundResult.OWin)
                return True
        if self.test_for_diagonal_fill(EX):
            self.conclude(RoundResult.XWin)
            return True
        elif self.test_for_diagonal_fill(OH):
            self.conclude(RoundResult.OWin)
            return True
        return False

    def handle_move(self, square: tuple[int, int]):
        self.first_move = False
        self.grid[square[0]][square[1]] = EX if self.x_turn else OH
        self.x_turn = not self.x_turn
        self.record.add_move(square)
        if not self.test_for_win():
            if self.test_for_full_grid():
                self.conclude(RoundResult.Draw)
