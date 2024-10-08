from mylang import lexer, parser
from interpreter import Interpreter

interpreter = Interpreter()
while True:
    code = input("> ")
    ast = parser.parse(code, lexer=lexer)
    node = interpreter.interpret(ast)
    if node:
        print(interpreter.getVal(node))
