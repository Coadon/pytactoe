import pygame as pg

from resource import resource_path

FONTS: dict[str, pg.Font] = {}

DEP_MONO_PATH = resource_path("assets/DepartureMono-Regular.otf")

def setup_fonts():
    global FONTS
    FONTS = {
        "BIGGER": pg.font.Font(DEP_MONO_PATH, 50),
        "BIG": pg.font.Font(DEP_MONO_PATH, 35),
        "MID": pg.font.Font(DEP_MONO_PATH, 25),
        "SMALL": pg.font.Font(DEP_MONO_PATH, 18),
    }


def font(name: str) -> pg.Font:
    global FONTS
    return FONTS[name]
