from mylang import lexer, parser

test_code = """\
1+2*(3+4)\
"""

ast = parser.parse(code_str=test_code, lexer=lexer)

