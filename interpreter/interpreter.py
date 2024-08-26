from parse import (
    Node,
    Statements,
    BinOp,
    Float,
    Assignment,
    Identifier,
    FunctionCall,
    StringLiteral,
)


class Interpreter:
    def __init__(self):
        self._locals = {}

    def getVal(self, node: Node) -> float:
        if isinstance(node, Float):
            return node.val
        elif isinstance(node, Identifier):
            if node.name not in self._locals:
                raise ValueError(
                    f'Cannot use variable "{node.name}" before initialization'
                )
            return self._locals[node.name]
        elif isinstance(node, StringLiteral):
            return node.val
        else:
            return self.getVal(self.interpret(node))

    def interpret(self, node: Node):
        if isinstance(node, Statements):
            lastNode = None
            for statement in node.statements:
                lastNode = self.interpret(statement)
            return lastNode
        elif isinstance(node, BinOp):
            leftVal = self.getVal(node.left)
            rightVal = self.getVal(node.right)
            if node.op == "+":
                return Float(val=leftVal + rightVal)
            elif node.op == "-":
                return Float(val=leftVal - rightVal)
            elif node.op == "*":
                return Float(val=leftVal * rightVal)
            elif node.op == "/":
                return Float(val=leftVal / rightVal)
        elif isinstance(node, Assignment):
            self._locals[node.identifier] = self.getVal(node.val)
        elif isinstance(node, FunctionCall):
            if node.name == "print":
                print(*[self.getVal(n) for n in node.args])
            return
        else:
            return node