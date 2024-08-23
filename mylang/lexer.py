from .constants import *
from lex import Lexer

lexer = Lexer()

lexer.add(Terminal.NUMBER, r"\d+")
lexer.add(Terminal.PLUS, r"\+")
lexer.add(Terminal.MINUS, r"\-")
lexer.add(Terminal.TIMES, r"\*")
lexer.add(Terminal.DIVIDE, r"\/")
lexer.add(Terminal.LPAREN, r"\(")
lexer.add(Terminal.RPAREN, r"\)")
lexer.ignore("[ \t]+")
