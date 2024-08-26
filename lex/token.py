from enum import Enum, auto
from dataclasses import dataclass

@dataclass
class Token:
    token_type: Enum
    lexeme: str