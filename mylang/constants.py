from enum import Enum, auto


class NonTerminal(Enum):
    PROGRAM = auto()
    STATEMENTS = auto()
    STATEMENT = auto()

    EXPR = auto()
    FUNC_CALL = auto()
    FUNC_ARGS = auto()
    TERM = auto()
    FACTOR = auto()


class Terminal(Enum):
    IDENTIFIER = auto()
    NUMBER = auto()
    STR_LITERAL = auto()

    ASSIGNMENT = auto()
    PLUS = auto()
    MINUS = auto()
    TIMES = auto()
    DIVIDE = auto()
    LPAREN = auto()
    RPAREN = auto()
    COMMA = auto()

    NEWLINE = auto()


class Operation(Enum):
    OP_ADD = auto()
    OP_SUB = auto()
    OP_MUL = auto()
    OP_DIV = auto()
