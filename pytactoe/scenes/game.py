from match import Match
from round import Round
from constants import SCREEN_SIZE, ex, other_side, to_result, EX, OH, to_number
from gfx.board import Board
from gfx.button import TextButton
from gfx.drawable import Text
from gfx.fonts import font
from scene import Scene

import pygame as pg


class ScGame(Scene):
    start_timed = False

    def __init__(self) -> None:
        super().__init__()

        self.match: Match = None
        self.round: Round = None

        self.board = Board((SCREEN_SIZE[0] // 2 - 200, SCREEN_SIZE[1] // 2 - 200), self.handle_grid_click)

        self.top_text = Text((SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2 - 250), "Spare", font("MID"), pg.Color(0, 0, 0))

        self.reset_btn = TextButton((SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2 + 250), (200, 30), "Reset Round", font("MID"), pg.Color(0, 0, 0), on_click=self.new_round)

        self.abandon_btn = TextButton((100, SCREEN_SIZE[1] - 10), (200, 30), "Abandon Game", font("SMALL"), pg.Color(0, 0, 0), on_click=self.abandon_game)

        self.score_x_text = Text((SCREEN_SIZE[0] // 2 - 300, SCREEN_SIZE[1] // 2 - 250), "", font("BIG"), pg.Color(0, 0, 0))
        self.score_o_text = Text((SCREEN_SIZE[0] // 2 + 300, SCREEN_SIZE[1] // 2 - 250), "", font("BIG"), pg.Color(0, 0, 0))
        self.timer_x_text = Text((SCREEN_SIZE[0] // 2 - 310, SCREEN_SIZE[1] // 2 - 200), "", font("MID"), pg.Color(0, 0, 0))
        self.timer_o_text = Text((SCREEN_SIZE[0] // 2 + 300, SCREEN_SIZE[1] // 2 - 200), "", font("MID"), pg.Color(0, 0, 0))
        self.match_status_text = Text((SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2 + 280), "", font("MID"), pg.Color(0, 0, 0))

    def start(self):
        self.match = Match(use=ScGame.start_timed)
        self.abandon_btn.text = "Abandon Game" if self.match.use else "Leave"
        self.abandon_btn.update_property()
        self.new_round()
        self.update_texts()

    def abandon_game(self):
        self.next_scene = "MAIN_MENU"

    def reset(self):
        self.match = None
        self.round = None

    def handle_timeout(self, side: int):
        self.round.conclude(to_result(other_side(side)), True)  # Draw on timeout
        self.update_texts()

    def handle_grid_click(self, square: tuple[int, int]):
        self.round.handle_move(square)
        self.update_texts()

    def new_round(self):
        self.match.reset_timer(initial_time=4_500.0)
        self.round = Round(match=self.match, x_starts=self.match.ex_is_first_mover)
        self.match.ex_is_first_mover = not self.match.ex_is_first_mover
        self.update_texts()

    def update_texts(self):
        if self.match.match_over:
            if self.match.score_x >= self.match.first_to:
                self.top_text.text = "X WINS GAME"
            elif self.match.score_o >= self.match.first_to:
                self.top_text.text = "O WINS GAME"
        elif self.round.round_over:
            if self.round.result == 1:
                self.top_text.text = "DRAW"
            elif self.round.result == 2:
                self.top_text.text = "X WINS ROUND"
            elif self.round.result == 3:
                self.top_text.text = "O WINS ROUND"
            if self.round.won_on_time:
                self.top_text.text += " (TIMEOUT)"
        else:
            if self.round.first_move:
                self.top_text.text = "FIRST MOVE: "
            else:
                self.top_text.text = "TURN: "
            if self.round.x_turn:
                self.top_text.text += "X"
            else:
                self.top_text.text += "O"

        if self.match.score_x == self.match.first_to - 1 or self.match.score_o == self.match.first_to - 1:
            self.match_status_text.text = "GAME POINT"
        elif self.match.match_over:
            self.match_status_text.text = "GAME OVER"
        else:
            self.match_status_text.text = f"FIRST TO {self.match.first_to}"

    def update(self):
        if self.round.result == 1:  # Draw
            self.board.wall_color = pg.Color(200, 200, 200)
        else:
            self.board.wall_color = pg.Color(0, 0, 0)

        self.score_x_text.text = f"X: {int(self.match.score_x)}" + ("*" if self.match.star == EX else "")
        self.score_o_text.text = f"O: {int(self.match.score_o)}" + ("*" if self.match.star == OH else "")
        self.timer_x_text.text = f"{self.match.timer_x / 1000 : .1f}"
        self.timer_o_text.text = f"{self.match.timer_o / 1000 : .1f}"

    def draw(self, screen, dt: float):
        screen.fill((240, 240, 215))  # Splash color
        self.board.update_draw(screen, self.round.round_over or self.match.match_over,
                               self.round.grid, to_number(self.round.result))
        self.top_text.update_draw(screen)
        self.reset_btn.update_draw(screen)
        self.abandon_btn.update_draw(screen)
        if self.match.use:
            self.score_x_text.update_draw(screen)
            self.score_o_text.update_draw(screen)
            self.timer_x_text.update_draw(screen)
            self.timer_o_text.update_draw(screen)

            if not self.round.round_over:
                if self.round.x_turn:
                    pg.draw.rect(screen, (0, 0, 0), pg.Rect(SCREEN_SIZE[0] // 2 - 400, 25, 200, 100), 2)
                else:
                    pg.draw.rect(screen, (0, 0, 0), pg.Rect(SCREEN_SIZE[0] // 2 + 200, 25, 200, 100), 2)
            else:
                if self.round.result == 2:
                    pg.draw.rect(screen, (0, 0, 0), pg.Rect(SCREEN_SIZE[0] // 2 - 400, 25, 200, 100), 2)
                elif self.round.result == 3:
                    pg.draw.rect(screen, (0, 0, 0), pg.Rect(SCREEN_SIZE[0] // 2 + 200, 25, 200, 100), 2)

            if not self.round.first_move:
                self.match.tick_timer(dt, ex(self.round.x_turn), self.handle_timeout)

            self.match_status_text.update_draw(screen)
