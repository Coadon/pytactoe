import pygame as pg

import histo
from constants import SCREEN_SIZE, ex, EX, OH, to_number, RoundResult, other_side, result_to_str
from gfx.board import Board
from gfx.button import TextButton
from gfx.drawable import Text
from gfx.fonts import font
from record import RoundRecord
from scene import Scene


class ScHistDetail(Scene):
    # start_timed = False

    def __init__(self) -> None:
        super().__init__()

        self.page_when_returning = 1

        self.round: RoundRecord = None
        self.round_result: RoundResult = None
        self.won_on_time: bool = False

        self.board = Board((SCREEN_SIZE[0] // 2 - 200, SCREEN_SIZE[1] // 2 - 200))

        self.top_text = Text((SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2 - 250), "", font("MID"), pg.Color(0, 0, 0))

        self.reset_btn = TextButton((SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2 + 250), (200, 30), "Return", font("MID"), pg.Color(0, 0, 0), on_click=self.cut_back)

        self.bottom_text = Text((SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2 + 280), "", font("MID"), pg.Color(0, 0, 0))

        self.grid = [[0 for _ in range(3)] for _ in range(3)]

    def start(self, **kwargs):
        self.page_when_returning = kwargs["PAGE"]
        round_raw = histo.get_round_by_id(kwargs["ID"])
        if round_raw is None:
            self.top_text.text = "Round not found."
            return
        self.top_text.text = round_raw[3]
        self.round = RoundRecord(round_raw[1])
        self.round_result, self.won_on_time = histo.deserialize_round_result(round_raw[2])
        result_str = result_to_str(self.round_result)
        self.bottom_text.text = "{} START - {}".format(self.round.starting_side, result_str)
        if self.won_on_time:
            self.bottom_text.text += " (won on time)"
        side = EX if self.round.starting_side == "X" else OH
        for move in self.round.moves:
            self.grid[move[0]][move[1]] = side
            side = other_side(side)

    def cut_back(self):
        self.next_scene_args = {"PAGE": self.page_when_returning}
        self.next_scene = "HIST_LIST"

    def reset(self):
        self.grid = [[0 for _ in range(3)] for _ in range(3)]
        self.round = None

    def draw(self, screen, dt: float):
        screen.fill((240, 240, 215))  # Splash color
        self.board.update_draw(screen, True, self.grid, 0)
        self.top_text.update_draw(screen)
        self.reset_btn.update_draw(screen)
        self.bottom_text.update_draw(screen)
