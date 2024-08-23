from enum import Enum, auto
from dataclasses import dataclass

class TokenType(Enum):
    NUMBER = auto()
    PLUS = auto()
    MINUS = auto()
    TIMES = auto()
    DIVIDE = auto()
    LPAREN = auto()
    RPAREN = auto()

@dataclass
class Token:
    token_type: TokenType
    lexeme: str