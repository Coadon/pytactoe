from typing import Callable

import pygame as pg

from constants import EX, OH
from gfx.drawable import Drawable, SurfRect
from gfx.button import GridButton

SQUARE_LEN = 133
BOARD_LEN = 400

BUTTON_LEN = 110
PADDING = 12

"""
Coordinates of squares:
(0, 0) (1, 0) (2, 0)
(0, 1) (1, 1) (2, 1)
(0, 2) (1, 2) (2, 2)
"""

FADE_ALPHA = 60


class Board(Drawable):
    image_x: pg.Surface
    image_o: pg.Surface

    @staticmethod
    def load_images():
        Board.image_x = pg.image.load("assets/graphic_ex.png")
        Board.image_o = pg.image.load("assets/graphic_oh.png")

    @staticmethod
    def create_grid(create_func):
        return [[create_func(x, y) for y in range(3)] for x in range(3)]

    def __init__(self, pos: tuple[int, int],
                 on_grid_click: Callable[[tuple[int, int]], None] = lambda pos: None) -> None:

        self.grid_boxes_oh: list[list[SurfRect]] = []
        self.grid_boxes_ex: list[list[SurfRect]] = []
        self.grid_buttons: list[list[GridButton]] = []
        self.pos = pos
        self.wall_color = pg.Color(0, 0, 0)
        self.on_grid_click = on_grid_click
        self.TOP_LEFT_POS = None
        self.update_transform()

    def debounce_buttons(self):
        for x in range(3):
            for y in range(3):
                self.grid_buttons[x][y].was_clicked = True

    def update_transform(self) -> None:
        self.TOP_LEFT_POS = [[(self.pos[0] + x * SQUARE_LEN, self.pos[1] + y * SQUARE_LEN) for y in range(3)] for x in
                             range(3)]

        def create_button(x, y):
            return GridButton(
                (self.TOP_LEFT_POS[x][y][0] + PADDING, self.TOP_LEFT_POS[x][y][1] + PADDING),
                (BUTTON_LEN, BUTTON_LEN),
                (x, y),
                self.on_grid_click
            )

        def create_surf_rect(image, x, y):
            return SurfRect(
                (self.TOP_LEFT_POS[x][y][0] + PADDING, self.TOP_LEFT_POS[x][y][1] + PADDING),
                pg.transform.scale(image, (BUTTON_LEN, BUTTON_LEN))
            )

        self.grid_buttons = Board.create_grid(create_button)
        self.grid_boxes_ex = Board.create_grid(lambda x, y: create_surf_rect(self.image_x, x, y))
        self.grid_boxes_oh = Board.create_grid(lambda x, y: create_surf_rect(self.image_o, x, y))

    def draw_walls(self, screen: pg.Surface):
        # Draw the vertical walls
        for x in range(1, 3):
            pg.draw.line(screen, self.wall_color, (self.pos[0] + x * SQUARE_LEN, self.pos[1]),
                         (self.pos[0] + x * SQUARE_LEN, self.pos[1] + BOARD_LEN), 5)
        # Draw the horizontal walls
        for y in range(1, 3):
            pg.draw.line(screen, self.wall_color, (self.pos[0], self.pos[1] + y * SQUARE_LEN),
                         (self.pos[0] + BOARD_LEN, self.pos[1] + y * SQUARE_LEN), 5)

    def update_draw(self, screen: pg.Surface, locked: bool, grid: list[list[int]], fade: int) -> None:
        """
        Update and draw the board on the given screen.
        :param screen:
        :param locked:
        :param grid:
        :param fade:
        :return:
        """
        self.draw_walls(screen)
        for x in range(3):
            for y in range(3):
                if grid[x][y] == EX:
                    self.grid_boxes_ex[x][y].alpha = FADE_ALPHA if fade in (2, 3) else 255
                    self.grid_boxes_ex[x][y].update_draw(screen)
                elif grid[x][y] == OH:
                    self.grid_boxes_oh[x][y].alpha = FADE_ALPHA if fade in (1, 3) else 255
                    self.grid_boxes_oh[x][y].update_draw(screen)
                elif not locked:
                    self.grid_buttons[x][y].update_draw(screen)
