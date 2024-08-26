from __future__ import annotations
from dataclasses import dataclass


class Node:
    def __repr__(self):
        cls_name = self.__class__.__name__
        attrs = ", ".join(f"{k}={v!r}" for k, v in vars(self).items())
        return f"{cls_name}({attrs})"


@dataclass
class Float(Node):
    val: float


@dataclass
class BinOp(Node):
    left: Node
    right: Node
    op: str


@dataclass
class Assignment(Node):
    identifier: str
    val: Node


@dataclass
class Statements(Node):
    statements: list[Node]


@dataclass
class Identifier(Node):
    name: str

@dataclass
class FunctionCall(Node):
    name: str
    args: list[Node]

@dataclass
class StringLiteral(Node):
    val: str