import pygame as pg

FONTS: dict[str, pg.Font] = {}


def setup_fonts():
    global FONTS
    FONTS = {
        "BIGGER": pg.font.SysFont("Departure Mono", 50),
        "BIG": pg.font.SysFont("Departure Mono", 35),
        "MID": pg.font.SysFont("Departure Mono", 25),
        "SMALL": pg.font.SysFont("Departure Mono", 18),
    }


def font(name: str) -> pg.Font:
    global FONTS
    return FONTS[name]
