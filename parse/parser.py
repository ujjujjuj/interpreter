from lex import Lexer, Token
from .node import Node
from enum import Enum
from .constants import *
from functools import cache
from collections import deque, defaultdict
from .defs import *


class Parser:
    def __init__(
        self, action_goto: list[dict[Enum, Action]], productions: list[Production]
    ):
        self._productions = productions
        self._action_goto = action_goto

    def parse(self, code_str: str, lexer: Lexer):

        token_stack: list[Enum] = []
        state_stack: list[int] = [0]

        tok_iter = iter(lexer.lex(code_str=code_str))
        tok_consume = True
        tok = None
        while True:
            try:
                if tok_consume:
                    tok = next(tok_iter)
                tok_consume = False
            except StopIteration:
                if tok.token_type == SpecialSymbol.END:
                    raise ValueError("Parsing error: No more tokens left")
                tok = Token(token_type=SpecialSymbol.END, lexeme="$")
                tok_consume = False

            if len(state_stack) == 0:
                raise ValueError("Parsing error: Ran out of states")

            state = state_stack[-1]

            if tok.token_type not in self._action_goto[state]:
                raise SyntaxError("Parsing error: No action to perform")

            action = self._action_goto[state][tok.token_type]

            if action.aType == ActionType.SHIFT:
                token_stack.append(tok)
                state_stack.append(action.val)
                tok_consume = True
                continue
            elif action.aType == ActionType.REDUCE:
                prod = self._productions[action.val]

                node = prod.func(
                    *[
                        sym.node if isinstance(sym, SemanticItem) else sym.lexeme
                        for sym in token_stack[-len(prod.rhs) :]
                    ]
                )

                token_stack = token_stack[: -len(prod.rhs)]
                state_stack = state_stack[: -len(prod.rhs)]

                sym = self._action_goto[state_stack[-1]][prod.lhs].val
                token_stack.append(SemanticItem(sym=prod.lhs, node=node))
                state_stack.append(sym)
                continue
            elif action.aType == ActionType.ACCEPT:
                break

        startItem = token_stack.pop()
        return startItem.node


class ParserGenerator:
    def __init__(
        self,
        start_symbol: str,
        terminal_symbols: list[Enum],
        non_terminal_symbols: list[Enum],
    ):

        self._start_symbol = start_symbol
        self._terminal_symbols = terminal_symbols
        self._non_terminal_symbols = non_terminal_symbols
        self._productions: list[Production] = []

    def production(self, lhs: Enum, rhs: frozenset[Enum]):
        def inner(func: Callable[..., Node]):
            self._productions.append(Production(lhs=lhs, rhs=rhs, func=func))

        return inner

    @cache
    def _find_first(self, sym: Enum) -> set[Enum]:
        if sym in self._terminal_symbols:
            return {sym}

        first = set()
        for production in self._productions:
            if production.lhs != sym:
                continue

            for rhs_sym in production.rhs:
                if rhs_sym == sym:
                    break

                rhs_first = self._find_first(rhs_sym)
                if len(rhs_first) != 0:
                    first.update(rhs_first)
                    break

        return first

    @cache
    def _find_item_follow(self, item: LRItem) -> set[Enum]:
        for rhs_sym in item.production.rhs[item.index + 1 :]:
            rhs_first = self._find_first(rhs_sym)
            if len(rhs_first) != 0:
                return rhs_first

        return item.lookahead

    def _find_parse_graph(
        self,
        basis_set: frozenset[LRItem] = None,
        parse_state: ParseState = None,
    ) -> int:

        if basis_set in parse_state.basis_sets:
            return parse_state.itemSets[parse_state.basis_sets[basis_set]]

        closure: list[LRItem] = list(basis_set)
        added_nodes: set[Enum, frozenset[Enum]] = set()
        q = deque(basis_set)
        while q:
            lrItem = q.popleft()

            if lrItem.index == len(lrItem.production.rhs):
                continue

            next_symbol = lrItem.production.rhs[lrItem.index]
            lookahead = self._find_item_follow(lrItem)

            f_lookahead = frozenset(lookahead)
            if (next_symbol, f_lookahead) in added_nodes:
                continue
            added_nodes.add((next_symbol, f_lookahead))

            if next_symbol in self._non_terminal_symbols:
                for production in self._productions:
                    if production.lhs == next_symbol:
                        new_item = LRItem(
                            production=production, lookahead=f_lookahead, index=0
                        )
                        q.append(new_item)
                        closure.append(new_item)

        tup_closure = frozenset(closure)
        group = ItemSet(
            items=tup_closure,
            idx=parse_state.counter,
        )
        parse_state.itemSets[group.idx] = group
        parse_state.counter += 1

        parse_state.basis_sets[basis_set] = group.idx

        next_aug_nodes: dict[Enum, list[LRItem]] = {}
        for aug_node in tup_closure:
            if aug_node.index == len(aug_node.production.rhs):
                continue

            new_aug_node = LRItem(
                production=aug_node.production,
                lookahead=aug_node.lookahead,
                index=aug_node.index + 1,
            )

            if aug_node.production.rhs[aug_node.index] not in next_aug_nodes:
                next_aug_nodes[aug_node.production.rhs[aug_node.index]] = []
            next_aug_nodes[aug_node.production.rhs[aug_node.index]].append(new_aug_node)

        for origin_symbol in next_aug_nodes:
            child_group = self._find_parse_graph(
                basis_set=frozenset(next_aug_nodes[origin_symbol]),
                parse_state=parse_state,
            )
            group.neighbors[origin_symbol] = child_group

        return group

    def _get_action_goto(self):
        init_prod = Production(SpecialSymbol.START, (self._start_symbol,), lambda: 42)
        self._productions.insert(0, init_prod)

        parse_state = ParseState()
        self._find_parse_graph(
            basis_set=(
                LRItem(
                    init_prod,
                    (SpecialSymbol.END,),
                    0,
                ),
            ),
            parse_state=parse_state,
        )

        prodIdx: dict[Production, int] = {}
        for idx, prod in enumerate(self._productions):
            prodIdx[prod] = idx

        action_goto: list[dict[Enum, Action]] = [{} for _ in range(parse_state.counter)]

        for groupIdx in range(parse_state.counter):
            group = parse_state.itemSets[groupIdx]

            for item in group.items:
                if item.index == len(item.production.rhs):
                    for lookahead_sym in item.lookahead:
                        action_goto[groupIdx][lookahead_sym] = Action(
                            aType=(
                                ActionType.ACCEPT
                                if lookahead_sym == SpecialSymbol.END
                                and item.production.lhs == SpecialSymbol.START
                                else ActionType.REDUCE
                            ),
                            val=prodIdx[item.production],
                        )

            for neigh in group.neighbors:
                if neigh in self._terminal_symbols:
                    if neigh in action_goto[groupIdx]:
                        raise SyntaxError(f"Shift/Reduce conflict")
                    action_goto[groupIdx][neigh] = Action(
                        aType=ActionType.SHIFT, val=group.neighbors[neigh].idx
                    )
                else:
                    action_goto[groupIdx][neigh] = Action(
                        aType=ActionType.GOTO, val=group.neighbors[neigh].idx
                    )

        return action_goto

    def generate(self) -> Parser:
        action_goto = self._get_action_goto()
        return Parser(action_goto=action_goto, productions=self._productions)
