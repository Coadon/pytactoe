import pygame as pg
from scene import Scene
from gfx.drawable import SurfRect
from gfx.button import TextButton
from constants import SCREEN_SIZE
from gfx.fonts import font


class ScTestA(Scene):
    def __init__(self) -> None:
        super().__init__()
        self.image = SurfRect((0, 0), pg.image.load("assets/x_modified.png"))
        self.text = font("MID").render("Tic Tac Toe", True, (0, 0, 0))
        self.btn = TextButton("Hi", font("MID"), pg.Color(0, 0, 0), (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2),
                              on_click=self.btn_change_scene)

    def btn_change_scene(self):
        self.next_scene = "SWITCH"

    def update(self):
        self.image.rect.center = pg.mouse.get_pos()

    def draw(self, screen, dt: float):
        mouse = pg.mouse.get_pos()
        screen.fill((240, 240, 215))
        screen.blit(self.text, (SCREEN_SIZE[0] // 2 - self.text.get_width() // 2, 50))
        self.image.update_draw(screen)
        self.btn.update_draw(screen)
        pg.draw.rect(screen, (0, 0, 0), pg.Rect(mouse[0], mouse[1], 40, 40), 1)
        pass
