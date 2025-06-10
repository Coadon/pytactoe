from abc import ABC

import pygame as pg

Vec2 = tuple[float, float]


class Drawable(ABC):
    def update_draw(self, *args, **kwargs):
        pass


class SurfRect(Drawable):
    def __init__(self, pos_tl: Vec2, surface: pg.Surface, alpha: int = 255):
        self.surface = None
        self.rect = None

        self.rect = surface.get_rect(topleft=pos_tl)
        self.surface = surface
        self.alpha = alpha

    def update_draw(self, screen: pg.Surface):
        self.surface.set_alpha(self.alpha)
        screen.blit(self.surface, self.rect)


class Text(Drawable):
    def __init__(self, pos: Vec2, text: str, font: pg.font.Font, color: pg.Color = pg.Color('black'), centered: bool = True):
        self.centered = centered
        self.text = text
        self.font = font
        self.color = color
        self.rect = None
        self.pos = pos

    def update_draw(self, screen: pg.Surface):
        rendered_text = self.font.render(self.text, True, self.color)
        self.rect = rendered_text.get_rect(**{"center" if self.centered else "topleft": self.pos})
        screen.blit(rendered_text, self.rect)

