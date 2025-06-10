import pygame as pg

from gfx.drawable import Drawable, Text
from scene import Scene
from gfx.button import TextButton
from constants import SCREEN_SIZE
from gfx.fonts import font


class ScHistList(Scene):
    class Row(Drawable):
        def __init__(self, ) -> None:
            super().__init__()
            self.text = font("SMALL").render("Rounds History", True, (0, 0, 0))
            self.rect = self.text.get_rect()

    def __init__(self) -> None:
        super().__init__()
        self.title = Text((50, 50), "Rounds History", font("MID"), pg.Color(0, 0, 0), centered=False)
        self.ui_rows: list[ScHistList.Row] = []

    def start(self, *args, **kwargs):
        pass

    def draw(self, screen, dt: float):
        screen.fill((240, 240, 215))
        self.title.update_draw(screen)
