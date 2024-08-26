from mylang import lexer, parser
from interpreter import Interpreter

test_code = """\
a = 3*(3+6)
b = 42
print(a+b)\
"""

interpreter = Interpreter()
while True:
    code = input("> ")
    ast = parser.parse(code, lexer=lexer)
    node = interpreter.interpret(ast)
    if node:
        print(interpreter.getVal(node))
