from abc import ABC
import pygame as pg


class Scene(ABC):
    def __init__(self) -> None:
        self.active: bool = False
        self.next_scene_args: dict[str, object] = {}
        self.next_scene = None

    def start(self, *args, **kwargs):
        pass

    def reset(self):
        pass

    def update(self):
        pass

    def call_event(self, event: pg.Event):
        pass

    def draw(self, screen: pg.Surface, dt: float):
        pass
