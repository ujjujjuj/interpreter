from __future__ import annotations
from lex import Lexer, Token
from typing import Callable, Any
from .node import Node
from enum import Enum
from .constants import *
from functools import cache
from collections import deque
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Rule:
    lhs: Enum
    rhs: tuple[Enum]
    func: Callable[..., Node]


@dataclass(frozen=True)
class AugmentedNode:
    rule: Rule
    lookahead: frozenset[Enum]
    index: int


@dataclass
class AugmentedGroup:
    nodes: frozenset[AugmentedNode]
    origin_symbol: Enum
    idx: int
    neighbors: dict[Enum, AugmentedGroup] = field(default_factory=lambda: {})


@dataclass
class AugmentationState:
    counter: int = 0
    used_augmented_generators: dict[frozenset[AugmentedNode], int] = field(
        default_factory=lambda: {}
    )
    groups: dict[int, AugmentedGroup] = field(default_factory=lambda: {})


AugmentedBlock = list[AugmentedNode]


class Parser:
    def __init__(
        self,
        start_symbol: str,
        terminal_symbols: list[Enum],
        non_terminal_symbols: list[Enum],
    ):

        self._start_symbol = start_symbol
        self._terminal_symbols = terminal_symbols
        self._non_terminal_symbols = non_terminal_symbols
        self._rules: list[Rule] = []

    def rule(self, lhs: Enum, rhs: frozenset[Enum]):
        def inner(func: Callable[..., Node]):
            self._rules.append(Rule(lhs=lhs, rhs=rhs, func=func))

        return inner

    @cache
    def _find_first(self, sym: Enum) -> set[Enum]:
        if sym in self._terminal_symbols:
            return {sym}

        first = set()
        for rule in self._rules:
            if rule.lhs != sym:
                continue

            for rhs_sym in rule.rhs:
                if rhs_sym == sym:
                    break

                rhs_first = self._find_first(rhs_sym)
                if len(rhs_first) != 0:
                    first.update(rhs_first)

        return first

    @cache
    def _find_follow(self, sym: Enum) -> set[Enum]:
        follow = set()
        if sym == self._start_symbol:
            follow.add(SpecialSymbol.END)

        for rule in self._rules:
            for idx, rhs_sym in enumerate(rule.rhs):
                if rhs_sym == sym:
                    if idx == len(rule.rhs) - 1:
                        if rule.lhs != sym:
                            follow.update(self._find_follow(rule.lhs))
                    else:
                        follow.update(self._find_first(rule.rhs[idx + 1]))

        return follow

    @cache
    def _find_rhs_first(self, rhs: frozenset[Enum]) -> set[Enum]:
        for rhs_sym in rhs:
            rhs_first = self._find_first(rhs_sym)
            if len(rhs_first) != 0:
                return rhs_first

        return {
            SpecialSymbol.END,
        }

    def _find_augmented_graph(
        self,
        last_augmented_nodes: frozenset[AugmentedNode] = None,
        augmentation_state: AugmentationState = None,
    ) -> int:

        if last_augmented_nodes in augmentation_state.used_augmented_generators:
            return augmentation_state.groups[
                augmentation_state.used_augmented_generators[last_augmented_nodes]
            ]

        if last_augmented_nodes[0].index == 0:
            origin_symbol = SpecialSymbol.EPSILON
        else:
            origin_symbol = last_augmented_nodes[0].rule.rhs[
                last_augmented_nodes[0].index - 1
            ]

        closure: list[AugmentedNode] = list(last_augmented_nodes)
        added_nodes: set[Enum, frozenset[Enum]] = set()
        q = deque(last_augmented_nodes)
        while q:
            augmented_node = q.popleft()

            if augmented_node.index == len(augmented_node.rule.rhs):
                continue

            next_symbol = augmented_node.rule.rhs[augmented_node.index]
            lookahead = self._find_rhs_first(
                augmented_node.rule.rhs[augmented_node.index + 1 :]
            ).union(set(augmented_node.lookahead))
            if len(lookahead) > 1 and SpecialSymbol.END in lookahead:
                lookahead.remove(SpecialSymbol.END)

            f_lookahead = frozenset(lookahead)
            if (next_symbol, f_lookahead) in added_nodes:
                continue
            added_nodes.add((next_symbol, f_lookahead))

            new_rules = []
            if next_symbol in self._non_terminal_symbols:
                for rule in self._rules:
                    if rule.lhs == next_symbol:
                        new_aug_node = AugmentedNode(
                            rule=rule, lookahead=f_lookahead, index=0
                        )
                        q.append(new_aug_node)
                        closure.append(new_aug_node)

        tup_closure = frozenset(closure)
        group = AugmentedGroup(
            nodes=tup_closure,
            origin_symbol=origin_symbol,
            idx=augmentation_state.counter,
        )
        augmentation_state.groups[group.idx] = group
        augmentation_state.counter += 1

        augmentation_state.used_augmented_generators[last_augmented_nodes] = group.idx

        next_aug_nodes: dict[Enum, list[AugmentedNode]] = {}
        for aug_node in tup_closure:
            if aug_node.index == len(aug_node.rule.rhs):
                continue

            new_aug_node = AugmentedNode(
                rule=aug_node.rule,
                lookahead=aug_node.lookahead,
                index=aug_node.index + 1,
            )

            if aug_node.rule.rhs[aug_node.index] not in next_aug_nodes:
                next_aug_nodes[aug_node.rule.rhs[aug_node.index]] = []
            next_aug_nodes[aug_node.rule.rhs[aug_node.index]].append(new_aug_node)

        for origin_symbol in next_aug_nodes:
            child_group = self._find_augmented_graph(
                last_augmented_nodes=tuple(next_aug_nodes[origin_symbol]),
                augmentation_state=augmentation_state,
            )
            group.neighbors[origin_symbol] = child_group

        return group

    def _get_action_goto(self):
        augmentation_state = AugmentationState()
        self._find_augmented_graph(
            last_augmented_nodes=(
                AugmentedNode(
                    Rule(SpecialSymbol.START, (self._start_symbol,), lambda: 42),
                    (SpecialSymbol.END,),
                    0,
                ),
            ),
            augmentation_state=augmentation_state,
        )

        for groupIdx in augmentation_state.groups:
            group = augmentation_state.groups[groupIdx]
            print(f"------ Group {group.idx} ------")
            for node in group.nodes:
                rule = list(map(lambda v: v.name, node.rule.rhs))
                rule.insert(node.index, ".")
                lookahead = list(map(lambda v: v.name, node.lookahead))
                nextGroupIdx = None
                if node.index < len(node.rule.rhs):
                    nextGroupIdx = group.neighbors[node.rule.rhs[node.index]].idx
                print(
                    f"{node.rule.lhs.name}: {' '.join(rule)} ; {' '.join(lookahead)} ; ---> {nextGroupIdx}"
                )

        # action = [
        #     [None]
        #     for _ in range(len(self._terminal_symbols) + 1)
        #     for _ in range(augmentation_state.counter)
        # ]
        # goto = [
        #     [None]
        #     for _ in range(len(self._non_terminal_symbols))
        #     for _ in range(augmentation_state.counter)
        # ]

        return augmentation_state

    def parse(self, code_str: str, lexer: Lexer):
        # for token in lexer.lex(code_str):
        #     print(token)
        # for nt_symbol in self._non_terminal_symbols:
        #     print(
        #         f"{nt_symbol}:\n  first={self._find_first(nt_symbol)}\n  follow={self._find_follow(nt_symbol)}"
        #     )
        # print()
        augmentation_state = self._get_action_goto()
        # for groupIdx in augmentation_state.groups:
        #     print("-----")
        #     for aug_node in augmentation_state.groups[groupIdx]:
        #         print(aug_node)
