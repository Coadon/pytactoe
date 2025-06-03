EMPTY = 0
EX = 1
OH = 2

CAPTION = "TIC TAC TOE"
SCREEN_SIZE = (1000, 600)
TARGET_FPS = 60.0


class RoundResult:
    Undetermined, Draw, XWin, OWin = range(4)


def ex(is_ex):
    """Returns the EX side if is_ex is True, otherwise returns the OH side."""
    return EX if is_ex else OH


def to_result(side: int):
    return RoundResult.XWin if side == EX else RoundResult.OWin if side == OH else RoundResult.Undetermined


def to_number(result: RoundResult):
    return EX if result == RoundResult.XWin else OH if result == RoundResult.OWin else EMPTY


def other_side(side: int):
    """Returns the other side: EX if side is OH, and OH if side is EX."""
    return OH if side == EX else EX if side == OH else 0
