import pygame as pg
from scene import Scene
from gfx.button import TextButton
from constants import SCREEN_SIZE
from gfx.fonts import font


class ScTestB(Scene):
    def __init__(self) -> None:
        super().__init__()
        self.btn = TextButton("Thing", font("MID"), pg.Color(255, 0, 0), (SCREEN_SIZE[0] * 0.8, SCREEN_SIZE[1] * 0.2),
                              on_click=self.btn_change_scene)

    def btn_change_scene(self):
        self.next_scene = "GAME"

    def draw(self, screen, dt: float):
        screen.fill((240, 240, 215))
        self.btn.update_draw(screen)
        mouse = pg.mouse.get_pos()
        pg.draw.rect(screen, (0, 0, 0), pg.Rect(mouse[0], mouse[1], 40, 40), 1)
        pass
