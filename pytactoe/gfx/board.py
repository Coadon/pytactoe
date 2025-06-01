import pygame as pg
from drawable import Drawable


class Board(Drawable):
    def __init__(self, pos: tuple[int, int]):
        self.pos = pos

    def update_draw(self, screen: pg.Surface):
        pg.draw.rect(screen, self.color, self.rect)