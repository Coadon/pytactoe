from abc import ABC
from typing import Optional

import pygame as pg


class Graphic(ABC):
    def __init__(self, pos: tuple[int, int], scale: tuple[float, float]):
        self.pos = pos
        self.scale = scale

    def mouse_collide(self) -> bool:
        pass

    def update_properties(self):
        pass

    def update_draw(self, *args, **kwargs):
        pass


class ColorRect(Graphic):
    def __init__(self, pos: tuple[int, int], scale: tuple[float, float],
                 color: tuple[int, int, int], alpha: int = 255):
        super().__init__(pos, scale)
        self.color = color
        self.alpha = alpha
        self.rect = None
        self.surface = None
        self.update_properties()

    def mouse_collide(self) -> bool:
        return self.rect.collidepoint(pg.mouse.get_pos())

    def update_properties(self):
        self.rect = pg.Rect(self.pos, (self.scale[0], self.scale[1]))
        self.surface = pg.Surface(self.rect.size, pg.SRCALPHA)
        pg.draw.rect(self.surface, self.color, self.rect)
        self.surface.set_alpha(self.alpha)

    def update_draw(self, screen):
        screen.blit(self.surface, self.rect)
