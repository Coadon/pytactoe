import pygame as pg
import sys

from graphic import ColorRect
from scene import Scene
from button import TextButton

CAPTION = "TIC TAC TOE"
SCREEN_SIZE = (1000, 600)
TARGET_FPS = 60.0

FONTS: dict[str, pg.Font] = {}


class Game(Scene):
    def __init__(self) -> None:
        super().__init__()
        self.cross = pg.image.load('assets/x_modified.png')
        self.cross_rect = self.cross.get_rect()
        self.text = FONTS["MID"].render("Tic Tac Toe", True, (0, 0, 0))
        self.btn = TextButton("Hi", FONTS["MID"], (0, 0, 0), (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2),
                              onclick=lambda: print("Button clicked!"))
        self.thing = ColorRect((0, 0), (50, 50), (255, 0, 0), alpha=50)

    def update(self):
        self.cross_rect.center = pg.mouse.get_pos()

    def draw(self, screen, dt: float):
        screen.fill((240, 240, 215))
        screen.blit(self.cross, self.cross_rect)
        screen.blit(self.text, (SCREEN_SIZE[0] // 2 - self.text.get_width() // 2, 50))
        self.btn.update_draw(screen)
        self.thing.update_draw(screen)
        pass


class Control:
    """
    Main game loop and things.
    """

    def __init__(self) -> None:
        screen = pg.display.get_surface()
        assert (screen is not None)

        self.screen: pg.Surface = screen
        self.should_stop = False
        self.clock = pg.time.Clock()
        self.scene_dict: dict[str, Scene] = {
            "GAME": Game()
        }
        self.scene: Scene = self.scene_dict["GAME"]

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.should_stop = True
            self.scene.call_event(event)

    def update(self):
        if not self.scene.active:
            self.scene.start()
            self.scene.active = True
        self.scene.update()
        if self.scene.next_scene:
            self.scene.active = False
            self.scene.reset()
            self.scene = self.scene_dict[self.scene.next_scene]

    def draw(self, dt):
        if self.scene.active:
            self.scene.draw(self.screen, dt)

    def display_fps(self):
        caption = "{} - FPS: {:.2f}".format(CAPTION, self.clock.get_fps())
        pg.display.set_caption(caption)

    def main_loop(self):
        self.screen.fill((240, 240, 215))  # Splash color
        while not self.should_stop:
            dt = self.clock.tick(TARGET_FPS)
            self.event_loop()
            self.update()
            self.draw(dt)
            pg.display.update()
            self.display_fps()


def main():
    global FONTS
    pg.init()
    pg.display.set_caption(CAPTION)
    pg.display.set_mode(SCREEN_SIZE)
    FONTS = {
        "BIG": pg.font.SysFont("Departure Mono", 50),
        "MID": pg.font.SysFont("Departure Mono", 25)}
    Control().main_loop()
    pg.quit()
    sys.exit()


if __name__ == "__main__":
    main()
