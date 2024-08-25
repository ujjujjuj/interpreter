from parse import ParserGenerator, Parser, Node
from .constants import *
from lex import Token


pg = ParserGenerator(
    start_symbol=NonTerminal.PROGRAM,
    terminal_symbols=list(Terminal),
    non_terminal_symbols=list(NonTerminal),
)


@pg.production(NonTerminal.PROGRAM, (NonTerminal.STATEMENTS,))
def parse_prog(expr):
    pass


@pg.production(
    NonTerminal.STATEMENTS,
    (NonTerminal.STATEMENTS, Terminal.NEWLINE, NonTerminal.STATEMENT),
)
def parse_statements_multi(expr):
    pass


@pg.production(NonTerminal.STATEMENTS, (NonTerminal.STATEMENT,))
def parse_statements_single(expr):
    pass


@pg.production(NonTerminal.STATEMENT, (NonTerminal.EXPR,))
def parse_statement_expt(expr):
    pass


@pg.production(
    NonTerminal.EXPR,
    (
        NonTerminal.EXPR,
        Terminal.PLUS,
        NonTerminal.TERM,
    ),
)
def parse_expr_add(expr):
    pass


@pg.production(
    NonTerminal.EXPR,
    (NonTerminal.TERM,),
)
def parse_expr_term(expr):
    pass


@pg.production(NonTerminal.TERM, (NonTerminal.TERM, Terminal.TIMES, NonTerminal.FACTOR))
def parse_term_mul(expr):
    pass


@pg.production(NonTerminal.TERM, (NonTerminal.FACTOR,))
def parse_term_fac(expr):
    pass


@pg.production(NonTerminal.FACTOR, (Terminal.LPAREN, NonTerminal.EXPR, Terminal.RPAREN))
def parse_fact_paren(expr):
    pass


@pg.production(NonTerminal.FACTOR, (Terminal.NUMBER,))
def parse_fact_num(expr):
    pass


# @pg.production(NonTerminal.PROGRAM, (NonTerminal.EXPR, NonTerminal.EXPR))
# def parse_prog(expr):
#     pass


# @pg.production(NonTerminal.EXPR, (Terminal.LPAREN, NonTerminal.EXPR))
# def parse_prog2(expr):
#     pass


# @pg.production(NonTerminal.EXPR, (Terminal.RPAREN,))
# def parse_prog3(expr):
#     pass


# @pg.production(NonTerminal.PROGRAM, (NonTerminal.EXPR,))
# def parse_prog(expr):
#     return expr


# @pg.production(
#     NonTerminal.EXPR,
#     (NonTerminal.EXPR, Terminal.PLUS, NonTerminal.EXPR),
# )
# def parse_expr_add(left: Node, right: Node):
#     pass

# # @pg.production(
# #     NonTerminal.EXPR,
# #     (NonTerminal.EXPR, Terminal.TIMES, NonTerminal.EXPR),
# # )
# # def parse_expr_mul(left: Node, right: Node):
# #     pass


# # @pg.production(
# #     NonTerminal.EXPR,
# #     (Terminal.LPAREN, NonTerminal.EXPR, Terminal.RPAREN),
# # )
# # def parse_expr_paren(left: Node, right: Node):
# #     pass

# @pg.production(NonTerminal.EXPR, (Terminal.NUMBER,))
# def parse_expr_num(token: Token):
#     pass

parser = pg.generate()
