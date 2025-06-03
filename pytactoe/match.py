from constants import EX, OH, EMPTY


class Match():
    def __init__(self, first_to: int = 7, use: bool = False):
        self.first_to = first_to
        self.match_over = False

        self.use = use
        self.score_x = 0
        self.score_o = 0
        self.star = EMPTY
        self.timer_x = 0.0
        self.timer_o = 0.0
        self.timer_freeze = False
        self.ex_is_first_mover = False

    def check_score(self):
        if self.first_to == -1:
            return
        if self.score_x == self.score_o and self.score_x == self.first_to - 1:
            self.first_to += 2
        elif self.score_x >= self.first_to or self.score_o >= self.first_to:
            self.match_over = True

    def increment_x(self, score: int):
        self.score_x += score
        self.check_score()

    def increment_o(self, score: int):
        self.score_o += score
        self.check_score()

    def tick_timer(self, dt: float, side: int, timeout_callback: callable = None):
        if self.timer_freeze:
            return
        elif side == EX:
            self.timer_x -= dt
            if self.timer_x <= 0:
                timeout_callback(EX)
                self.timer_x = 0
                self.timer_freeze = True
        elif side == OH:
            self.timer_o -= dt
            if self.timer_o <= 0:
                timeout_callback(OH)
                self.timer_o = 0
                self.timer_freeze = True

    def reset_timer(self, initial_time: float):
        self.timer_freeze = False
        self.timer_o = initial_time
        self.timer_x = initial_time

    def announce_draw(self):
        self.timer_freeze = True
        if self.timer_x > self.timer_o:
            if self.star == EX:
                self.increment_x(1)
                self.star = EMPTY
            else:
                self.star = EX
        else:
            if self.star == OH:
                self.increment_o(1)
                self.star = EMPTY
            else:
                self.star = OH
