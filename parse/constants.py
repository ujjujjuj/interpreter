from enum import Enum, auto


class SpecialSymbol(Enum):
    START = "S'"
    END = "$"
    EPSILON = "e"


class ActionType(Enum):
    SHIFT = auto()
    REDUCE = auto()
    ACCEPT = auto()
    GOTO = auto()
