import pygame as pg

FONTS: dict[str, pg.Font] = {}


def setup_fonts():
    global FONTS
    FONTS = {
        "BIG": pg.font.SysFont("Departure Mono", 50),
        "MID": pg.font.SysFont("Departure Mono", 25)}


def font(name: str) -> pg.Font:
    global FONTS
    return FONTS[name]
