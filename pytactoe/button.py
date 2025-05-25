import pygame as pg

from graphic import Graphic


class TextButton(Graphic):
    def __init__(self, text: str, font: pg.Font, color: tuple[int, int, int], pos: tuple[int, int],
                 scale: tuple[float, float] = (50.0, 30.0), onclick: callable = lambda: None):
        super().__init__(pos, scale)
        self.text = text
        self.font = font
        self.color = color
        self.onclick = onclick
        self.was_clicked = False

        self.text_surface = None
        self.text_rect = None
        self.box_rect = None
        self.box_surface = None
        self.update_properties()

    def mouse_collide(self) -> bool:
        return self.box_rect.collidepoint(pg.mouse.get_pos())

    def update_properties(self):
        self.text_surface = self.font.render(self.text, True, self.color)
        self.text_rect = self.text_surface.get_rect(center=self.pos)
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
                    self.onclick()
            else:
                self.was_clicked = False

        screen.blit(self.text_surface, self.text_rect)
