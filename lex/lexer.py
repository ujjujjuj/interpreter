from typing import Optional, Callable, Any
from .token import Token
import re
from enum import Enum


class Lexer:
    def __init__(self):
        self._token_list = []
        self._ignore_list = []

    def add(
        self,
        token_name: Enum,
        token_pattern: str,
    ):
        self._token_list.append((token_name, token_pattern))

    def ignore(self, ignore_pattern: str):
        self._ignore_list.append(ignore_pattern)

    def lex(self, code_str: str):
        return LexerIter(self, code_str=code_str)


class LexerIter:
    def __init__(self, lexer: Lexer, code_str: str):
        self._lexer = lexer
        self._code_str = code_str
        self._curr = 0

    def __iter__(self):
        return self

    def __next__(self) -> Token:
        if self._curr == len(self._code_str):
            raise StopIteration

        for token_type, token_pattern in self._lexer._token_list:
            lexeme = re.match("^" + token_pattern, self._code_str[self._curr :])
            if lexeme == None:
                continue

            span = lexeme.span()
            lexeme = self._code_str[self._curr + span[0] : self._curr + span[1]]
            self._curr += span[1]

            return Token(token_type=token_type, lexeme=lexeme)

        for ignore_pattern in self._lexer._ignore_list:
            ignore_lexeme = re.match("^" + ignore_pattern, self._code_str[self._curr :])
            if ignore_lexeme != None:
                span = ignore_lexeme.span()
                self._curr += span[1]
                return next(self)

        raise SyntaxError(f"Invalid lexeme at offset: {self._curr}")
