from parse import (
    ParserGenerator,
    Parser,
    Node,
    Float,
    BinOp,
    Assignment,
    Statements,
    FunctionCall,
    Identifier,
    StringLiteral,
)
from .constants import *
from lex import Token

pg = ParserGenerator(
    start_symbol=NonTerminal.PROGRAM,
    terminal_symbols=list(Terminal),
    non_terminal_symbols=list(NonTerminal),
)


@pg.production(NonTerminal.PROGRAM, (NonTerminal.STATEMENTS,))
def func(statements: Node):
    return statements


@pg.production(
    NonTerminal.STATEMENTS,
    (NonTerminal.STATEMENTS, Terminal.NEWLINE, NonTerminal.STATEMENT),
)
def func(statements: Statements, newline, statement: Node):
    return Statements(statements=[*statements.statements, statement])


@pg.production(NonTerminal.STATEMENTS, (NonTerminal.STATEMENT,))
def func(statement: Node):
    return Statements(statements=[statement])


@pg.production(
    NonTerminal.STATEMENT, (Terminal.IDENTIFIER, Terminal.ASSIGNMENT, NonTerminal.EXPR)
)
def func(identifier: str, equ: str, val: Node):
    return Assignment(identifier=identifier, val=val)


@pg.production(NonTerminal.STATEMENT, (NonTerminal.EXPR,))
def func(expr: Node):
    return expr


@pg.production(NonTerminal.EXPR, (NonTerminal.FUNC_CALL,))
def func(expr: Node):
    return expr


@pg.production(
    NonTerminal.FUNC_CALL,
    (Terminal.IDENTIFIER, Terminal.LPAREN, NonTerminal.FUNC_ARGS, Terminal.RPAREN),
)
def func(name: str, lparen: str, args: list[Node], rparen: str):
    return FunctionCall(name=name, args=args)


@pg.production(
    NonTerminal.FUNC_CALL,
    (Terminal.IDENTIFIER, Terminal.LPAREN, NonTerminal.FUNC_ARGS, Terminal.RPAREN),
)
def func(name: str, lparen: str, args: list[Node], rparen: str):
    return FunctionCall(name=name, args=args)


@pg.production(
    NonTerminal.FUNC_ARGS,
    (NonTerminal.FUNC_ARGS, Terminal.COMMA, NonTerminal.EXPR),
)
def func(args: list[Node], comma: str, expr: Node):
    return [*args, expr]


@pg.production(
    NonTerminal.FUNC_ARGS,
    (NonTerminal.EXPR,),
)
def func(expr: Node):
    return [expr]


@pg.production(
    NonTerminal.EXPR,
    (Terminal.STR_LITERAL,),
)
def func(val: str):
    return StringLiteral(val=val)


# ARITHMETIC


@pg.production(
    NonTerminal.EXPR,
    (
        NonTerminal.EXPR,
        Terminal.PLUS,
        NonTerminal.TERM,
    ),
)
def func(expr: Node, plus, term: Node):
    return BinOp(left=expr, right=term, op="+")


@pg.production(
    NonTerminal.EXPR,
    (
        NonTerminal.EXPR,
        Terminal.MINUS,
        NonTerminal.TERM,
    ),
)
def func(expr: Node, plus, term: Node):
    return BinOp(left=expr, right=term, op="-")


@pg.production(
    NonTerminal.EXPR,
    (NonTerminal.TERM,),
)
def func(term: Node):
    return term


@pg.production(NonTerminal.TERM, (NonTerminal.TERM, Terminal.TIMES, NonTerminal.FACTOR))
def func(term: Node, times, fac: Node):
    return BinOp(left=term, right=fac, op="*")


@pg.production(
    NonTerminal.TERM, (NonTerminal.TERM, Terminal.DIVIDE, NonTerminal.FACTOR)
)
def func(term: Node, times, fac: Node):
    return BinOp(left=term, right=fac, op="/")


@pg.production(NonTerminal.TERM, (NonTerminal.FACTOR,))
def func(fac: Node):
    return fac


@pg.production(NonTerminal.FACTOR, (Terminal.LPAREN, NonTerminal.EXPR, Terminal.RPAREN))
def func(lparen, expr: Node, rparen):
    return expr


@pg.production(NonTerminal.FACTOR, (Terminal.NUMBER,))
def func(num: str):
    return Float(val=float(num))


@pg.production(NonTerminal.FACTOR, (Terminal.IDENTIFIER,))
def func(name: str):
    return Identifier(name=name)


# END ARITHMETIC

parser = pg.generate()
