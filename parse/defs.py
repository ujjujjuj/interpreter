from __future__ import annotations
from dataclasses import dataclass,field
from enum import Enum
from typing import Callable
from .node import Node

@dataclass(frozen=True)
class Production:
    lhs: Enum
    rhs: tuple[Enum]
    func: Callable[..., Node]


@dataclass(frozen=True)
class LRItem:
    production: Production
    lookahead: frozenset[Enum]
    index: int


@dataclass
class ItemSet:
    items: frozenset[LRItem]
    idx: int
    neighbors: dict[Enum, ItemSet] = field(default_factory=lambda: {})


@dataclass
class ParseState:
    counter: int = 0
    basis_sets: dict[frozenset[LRItem], int] = field(default_factory=lambda: {})
    itemSets: dict[int, ItemSet] = field(default_factory=lambda: {})


@dataclass
class Action:
    aType: ActionType
    val: int


@dataclass
class SemanticItem:
    sym: Enum
    node: Node