from parse import Parser, Node
from .constants import *
from lex import Token


parser = Parser(
    start_symbol=NonTerminal.PROGRAM,
    terminal_symbols=list(Terminal),
    non_terminal_symbols=list(NonTerminal),
)


@parser.rule(NonTerminal.PROGRAM, (Terminal.DIVIDE, NonTerminal.EXPR, Terminal.NUMBER))
def parse_prog(expr):
    pass


@parser.rule(
    NonTerminal.PROGRAM, (Terminal.LPAREN, NonTerminal.STATEMENT, Terminal.NUMBER)
)
def parse_prog2(expr):
    pass


@parser.rule(
    NonTerminal.PROGRAM, (Terminal.DIVIDE, NonTerminal.STATEMENT, Terminal.PLUS)
)
def parse_prog3(expr):
    pass


@parser.rule(NonTerminal.PROGRAM, (Terminal.LPAREN, NonTerminal.EXPR, Terminal.PLUS))
def parse_prog3(expr):
    pass


@parser.rule(NonTerminal.EXPR, (Terminal.MINUS,))
def parse_prog5(expr):
    pass


@parser.rule(NonTerminal.STATEMENT, (Terminal.MINUS,))
def parse_prog4(expr):
    pass


# @parser.rule(NonTerminal.PROGRAM,(NonTerminal.EXPR,NonTerminal.EXPR))
# def parse_prog(expr):
#     pass


# @parser.rule(NonTerminal.EXPR,(Terminal.LPAREN,NonTerminal.EXPR))
# def parse_prog2(expr):
#     pass


# @parser.rule(NonTerminal.EXPR,(Terminal.RPAREN,))
# def parse_prog3(expr):
#     pass

# @parser.rule(NonTerminal.PROGRAM, (NonTerminal.EXPR,))
# def parse_prog(expr):
#     return expr


# @parser.rule(
#     NonTerminal.EXPR,
#     (NonTerminal.EXPR, Terminal.PLUS, NonTerminal.EXPR),
# )
# def parse_expr_add(left: Node, right: Node):
#     pass

# # @parser.rule(
# #     NonTerminal.EXPR,
# #     (NonTerminal.EXPR, Terminal.TIMES, NonTerminal.EXPR),
# # )
# # def parse_expr_mul(left: Node, right: Node):
# #     pass


# # @parser.rule(
# #     NonTerminal.EXPR,
# #     (Terminal.LPAREN, NonTerminal.EXPR, Terminal.RPAREN),
# # )
# # def parse_expr_paren(left: Node, right: Node):
# #     pass

# @parser.rule(NonTerminal.EXPR, (Terminal.NUMBER,))
# def parse_expr_num(token: Token):
#     pass
