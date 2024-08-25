from enum import Enum, auto


class NonTerminal(Enum):
    PROGRAM = auto()
    STATEMENTS = auto()
    STATEMENT = auto()
    
    EXPR = auto()
    TERM = auto()
    FACTOR = auto()


class Terminal(Enum):
    NUMBER = auto()
    PLUS = auto()
    MINUS = auto()
    TIMES = auto()
    DIVIDE = auto()
    LPAREN = auto()
    RPAREN = auto()

    NEWLINE = auto()


class Operation(Enum):
    OP_ADD = auto()
    OP_SUB = auto()
    OP_MUL = auto()
    OP_DIV = auto()
