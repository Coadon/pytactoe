from typing import Callable

import pygame as pg

from gfx.drawable import Drawable

Vec2 = tuple[float, float]


class TextButton(Drawable):
    def __init__(self, pos_center: Vec2, scale: Vec2, text: str, font: pg.Font, color: pg.Color,
                 on_click: callable = lambda: None):
        self.pos_center = pos_center
        self.scale = scale
        self.text = text
        self.font = font
        self.color = color
        self.on_click = on_click
        self.was_clicked = True

        self.text_surface = None
        self.text_rect = None
        self.box_rect = None
        self.box_surface = None
        self.update_property()

    def update_property(self):
        self.text_surface = self.font.render(self.text, False, self.color)
        self.text_rect = self.text_surface.get_rect(center=self.pos_center)
        self.box_rect = pg.Rect(
            self.text_rect.centerx - self.scale[0] // 2,
            self.text_rect.centery - self.scale[1] // 2,
            self.scale[0],
            self.scale[1]
        )
        self.box_surface = pg.Surface(self.box_rect.size, pg.SRCALPHA)
        pg.draw.rect(self.box_surface, self.color, self.box_surface.get_rect())
        self.box_surface.set_alpha(50)

    def update_draw(self, screen: pg.Surface):
        mouse_pos = pg.mouse.get_pos()
        if self.box_rect.collidepoint(mouse_pos):
            screen.blit(self.box_surface, self.box_rect)
            if pg.mouse.get_pressed()[0] == 1:
                if not self.was_clicked:
                    self.was_clicked = True
                    self.on_click()
            else:
                self.was_clicked = False

        screen.blit(self.text_surface, self.text_rect)


class GridButton(Drawable):
    def __init__(self, pos_tl: Vec2, scale: Vec2 = (50.0, 30.0), square_pos: tuple[int, int] = (0, 0),
                 on_click: Callable[[tuple[int, int]], None] = lambda square: None):
        self.square_pos = square_pos
        self.pos_tl = pos_tl
        self.scale = scale
        self.on_click = on_click
        self.was_clicked = True

        self.box_rect = None
        self.box_surface = None
        self.box_rect: pg.Rect
        self.update_box()

    def update_box(self):
        self.box_rect = pg.Rect(self.pos_tl[0], self.pos_tl[1], self.scale[0], self.scale[1])

    def draw_box(self, screen: pg.Surface):
        # How to draw a box? Here is a simple yet wierd way to do it:
        # https://stackoverflow.com/questions/61951026/pygame-drawing-a-border-of-a-rectangle
        pg.draw.rect(screen, (0, 0, 0), self.box_rect, 1)

    def update_draw(self, screen: pg.Surface):
        self.update_box()
        mouse_pos = pg.mouse.get_pos()
        if self.box_rect.collidepoint(mouse_pos):
            self.draw_box(screen)
            if pg.mouse.get_pressed()[0] == 1:
                if not self.was_clicked:
                    self.was_clicked = True
                    self.on_click(self.square_pos)
            else:
                self.was_clicked = False

