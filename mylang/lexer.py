from .constants import *
from lex import Lexer

lexer = Lexer()

lexer.add(Terminal.IDENTIFIER, r"[_a-zA_Z][_a-zA-Z0-9]*")
lexer.add(Terminal.NUMBER, r"\d+")
lexer.add(Terminal.STR_LITERAL, r'"(\\.|[^"\\])*"')

lexer.add(Terminal.ASSIGNMENT, r"\=")
lexer.add(Terminal.PLUS, r"\+")
lexer.add(Terminal.MINUS, r"\-")
lexer.add(Terminal.TIMES, r"\*")
lexer.add(Terminal.DIVIDE, r"\/")
lexer.add(Terminal.LPAREN, r"\(")
lexer.add(Terminal.RPAREN, r"\)")
lexer.add(Terminal.COMMA, r"\,")

lexer.add(Terminal.NEWLINE, r"\n")

lexer.ignore("[ \t]+")
