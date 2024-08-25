from mylang import lexer, parser

test_code = """\
2*3+5\
"""

ast = parser.parse(code_str=test_code, lexer=lexer)

