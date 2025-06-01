from abc import ABC

import pygame as pg

Vec2 = tuple[float, float]


class Drawable(ABC):
    def update_draw(self, *args, **kwargs):
        pass


class SurfRect(Drawable):
    def __init__(self, pos: Vec2, surface: pg.Surface, alpha: int = 255):
        self.surface = None
        self.rect = None

        self.rect = surface.get_rect(topleft=pos)
        self.surface = surface
        self.alpha = alpha

    def update_draw(self, screen: pg.Surface):
        screen.blit(self.surface, self.rect)
