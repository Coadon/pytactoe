import pygame as pg
import sys
from control import Control
from constants import CAPTION, SCREEN_SIZE
from gfx.fonts import setup_fonts

Vec2 = tuple[float, float]


def main():
    pg.init()
    pg.display.set_caption(CAPTION)
    pg.display.set_mode(SCREEN_SIZE)
    setup_fonts()
    Control().main_loop()
    pg.quit()
    sys.exit()


if __name__ == "__main__":
    main()
