import pygame as pg
from pygame import Color

import histo
from gfx.drawable import Drawable, Text
from scene import Scene
from gfx.button import TextButton
from constants import SCREEN_SIZE, to_number, RoundResult, EX
from gfx.fonts import font

ROWS_PER_PAGE = 15


class HistRow(Drawable):
    def __init__(self, y_pos: float, odd: bool, date: str, starting_side: str, winner: str, won_on_time: bool,
                 rec_id: int, page_now: int, parent_scene: Scene) -> None:
        super().__init__()
        self.parent_scene = parent_scene
        self.page_now = page_now
        self.rec_id = rec_id
        self.y_pos = y_pos
        self.bg_color = (220, 220, 220) if odd else (200, 200, 200)

        # Text elements
        self.date_text = font("SMALL").render(date, True, (0, 0, 0))
        self.starting_side_text = font("SMALL").render(starting_side[0], True, (0, 0, 0))
        self.winner_text = font("SMALL").render(winner, True, (0, 0, 0))
        self.won_on_time_text = font("SMALL").render("Yes" if won_on_time else "No", True, (0, 0, 0))

        # Button for details
        self.details_button = TextButton((900, y_pos + 15),
                                         (100, 30),
                                         "Details",
                                         font("SMALL"),
                                         Color(0, 0, 0),
                                         on_click=self.cut_to_details)

    def cut_to_details(self):
        self.parent_scene.next_scene_args = {"ID": self.rec_id, "PAGE": self.page_now}
        self.parent_scene.next_scene = "HIST_DETAIL"

    def update_draw(self, screen: pg.Surface):
        # Draw background
        pg.draw.rect(screen, self.bg_color, (0, self.y_pos, SCREEN_SIZE[0], 30))

        # Draw text elements
        screen.blit(self.date_text, (10, self.y_pos + 5))
        screen.blit(self.starting_side_text, (350, self.y_pos + 5))
        screen.blit(self.winner_text, (500, self.y_pos + 5))
        screen.blit(self.won_on_time_text, (650, self.y_pos + 5))

        # Draw the details button
        self.details_button.update_draw(screen)


class ScHistList(Scene):

    def __init__(self) -> None:
        super().__init__()
        self.page_num = 0
        self.page_now = 0
        self.last_page_rows_cnt = 0
        self.total_row_cnt = 0

        self.title = Text((SCREEN_SIZE[0] // 2, 20), "Rounds History", font("MID"), Color(0, 0, 0), centered=True)

        self.return_btn = TextButton((45, 20), (80, 30), "Return", font("SMALL"), Color(0, 0, 0),
                                     on_click=self.return_to_menu)
        self.clear_btn = TextButton((SCREEN_SIZE[0] - 45, 20), (80, 30), "Clear", font("SMALL"), Color(0, 0, 0),
                                    on_click=self.clear_history)
        self.next_btn = TextButton((SCREEN_SIZE[0] // 2 + 130, 550), (50, 50), ">", font("BIGGER"), Color(0, 0, 0),
                                   on_click=self.next_page)
        self.prev_btn = TextButton((SCREEN_SIZE[0] // 2 - 130, 550), (50, 50), "<", font("BIGGER"), Color(0, 0, 0),
                                   on_click=self.prev_page)
        self.page_ind = Text((SCREEN_SIZE[0] // 2, 550), "0", font("BIG"), Color(0, 0, 0), centered=True)

        self.head_1 = Text((10, 60), "DATE & TIME", font("SMALL"), Color(0, 0, 0), centered=False)
        self.head_2 = Text((350, 60), "STARTER", font("SMALL"), Color(0, 0, 0), centered=False)
        self.head_3 = Text((500, 60), "WINNER", font("SMALL"), Color(0, 0, 0), centered=False)
        self.head_4 = Text((650, 60), "WON ON TIME", font("SMALL"), Color(0, 0, 0), centered=False)

        self.ui_rows: list[HistRow] = []

    def return_to_menu(self):
        self.next_scene = "MAIN_MENU"

    def clear_history(self):
        histo.clear_history()
        self.start()

    def next_page(self):
        if self.page_now >= self.page_num:
            return
        self.page_now += 1
        self.update_rows()

    def prev_page(self):
        if self.page_now == 1:
            return
        self.page_now -= 1
        self.update_rows()

    def start(self, *args, **kwargs):
        self.total_row_cnt = histo.get_round_count()
        if self.total_row_cnt is None:
            self.total_row_cnt = 0
        self.last_page_rows_cnt = self.total_row_cnt % ROWS_PER_PAGE
        self.page_num = self.total_row_cnt // ROWS_PER_PAGE + (self.last_page_rows_cnt != 0)
        self.page_now = kwargs["page"] if "page" in kwargs else 1
        self.update_rows()

    def update_rows(self):
        self.ui_rows.clear()
        self.page_ind.text = f"{str(self.page_now)}/{str(self.page_num)}"
        start = (self.page_now - 1) * ROWS_PER_PAGE
        end = start + ROWS_PER_PAGE
        row_data = histo.get_round_range(start, end)
        print(start, end)
        print(row_data)

        for i, row in enumerate(row_data):
            odd = (i % 2 == 0)
            row_id, row_rec, win_state_encoding, date = row
            winner, won_on_time = histo.deserialize_round_result(win_state_encoding)
            self.ui_rows.append(HistRow(
                100 + i * 30,  # Use the index `i` for positioning
                odd,
                date,
                row_rec[0],
                "X" if to_number(winner) == EX else "O",
                won_on_time,
                row_id,
                self.page_now,
                self)  # Pass `row_id` explicitly
            )

    def draw(self, screen, dt: float):
        screen.fill((240, 240, 215))
        self.title.update_draw(screen)
        self.return_btn.update_draw(screen)
        self.clear_btn.update_draw(screen)
        self.next_btn.update_draw(screen)
        self.prev_btn.update_draw(screen)

        self.page_ind.update_draw(screen)
        self.head_1.update_draw(screen)
        self.head_2.update_draw(screen)
        self.head_3.update_draw(screen)
        self.head_4.update_draw(screen)

        for row in self.ui_rows:
            row.update_draw(screen)
