import pygame as pg
from scene import Scene
from scenes.game import ScGame
from scenes.main_menu import ScMainMenu
from constants import TARGET_FPS, CAPTION


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
            "MAIN_MENU": ScMainMenu(),
            "GAME": ScGame(),
        }
        self.scene: Scene = self.scene_dict["MAIN_MENU"]

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.should_stop = True
            self.scene.call_event(event)

    def update(self):
        if self.scene.next_scene:
            self.scene.active = False
            self.scene.reset()
            if self.scene.next_scene == "STOP":
                self.should_stop = True
            self.scene, self.scene.next_scene = self.scene_dict[self.scene.next_scene], None
        if not self.scene.active:
            self.scene.start()
            self.scene.active = True
        self.scene.update()

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
