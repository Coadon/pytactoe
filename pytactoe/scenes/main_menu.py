import webbrowser
import pygame as pg
from scene import Scene
from gfx.button import TextButton
from constants import SCREEN_SIZE
from gfx.fonts import font


class ScMainMenu(Scene):
    def __init__(self) -> None:
        super().__init__()
        self.text = font("BIG").render("Tic Tac Toe", False, (0, 0, 0))

        self.btn_timed_game = TextButton((SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2), (300, 30),
                                         "Timed", font("MID"), pg.Color(0, 0, 0),
                                         on_click=self.cut_to_timed_game)

        self.btn_casual_game = TextButton((SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2 + 70), (300, 30),
                                          "Casual", font("MID"), pg.Color(0, 0, 0),
                                          on_click=self.cut_to_casual_game)

        self.btn_history = TextButton((SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2 + 140), (300, 30),
                                      "History", font("MID"), pg.Color(0, 0, 0),
                                      on_click=self.cut_to_history)

        self.source_link = TextButton((SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] - 20), (500, 20),
                                      "Released under the MIT License", font("SMALL"), pg.Color(0, 0, 0),
                                      on_click=lambda: webbrowser.open("https://github.com/Coadon/pytactoe/"))

    def cut_to_timed_game(self):
        self.next_scene_args = {"start_timed": True}
        self.next_scene = "GAME"

    def cut_to_casual_game(self):
        self.next_scene_args = {"start_timed": False}
        self.next_scene = "GAME"

    def cut_to_history(self):
        self.next_scene = "HIST_LIST"

    def draw(self, screen, dt: float):
        screen.fill((240, 240, 215))
        screen.blit(self.text, (SCREEN_SIZE[0] // 2 - self.text.get_width() // 2, 50))
        self.btn_timed_game.update_draw(screen)
        self.btn_casual_game.update_draw(screen)
        self.btn_history.update_draw(screen)
        self.source_link.update_draw(screen)
