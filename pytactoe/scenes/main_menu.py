import pygame as pg
from scene import Scene
from gfx.drawable import SurfRect
from gfx.button import TextButton
from constants import SCREEN_SIZE
from gfx.fonts import font
from scenes.game import ScGame


class ScMainMenu(Scene):
    def __init__(self) -> None:
        super().__init__()
        self.text = font("BIGGER").render("Tic Tac Toe", True, (0, 0, 0))

        self.btn_timed_game = TextButton((SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2), (300, 30),
                                         "TIMED GAME", font("MID"), pg.Color(0, 0, 0),
                                         on_click=self.cut_to_timed_game)

        self.btn_casual_game = TextButton((SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2 + 70), (300, 30),
                                          "CASUAL GAME", font("MID"), pg.Color(0, 0, 0),
                                          on_click=self.cut_to_casual_game)

    def cut_to_timed_game(self):
        ScGame.start_timed = True
        self.next_scene = "GAME"

    def cut_to_casual_game(self):
        ScGame.start_timed = False
        self.next_scene = "GAME"

    def draw(self, screen, dt: float):
        screen.fill((240, 240, 215))
        screen.blit(self.text, (SCREEN_SIZE[0] // 2 - self.text.get_width() // 2, 50))
        self.btn_timed_game.update_draw(screen)
        self.btn_casual_game.update_draw(screen)
