from typing import List, Tuple, Dict, Optional, Union, Set

import lexer


class StateItem:
    def __init__(self, left: str, right: List[Union[str, lexer.TokenType]], cfg_id: int, auto_generated: bool = False,
                 pos: int = 0):
        self.left: str = left
        self.right: List[Union[str, lexer.TokenType]] = right
        self.cfg_id: int = cfg_id
        self.pos: int = pos
        self.auto_generated: bool = auto_generated

    def __str__(self):
        right_hand = ''
        for k, item in enumerate(self.right):
            if k == self.pos:
                right_hand += ' ●'
            else:
                right_hand += ' '

            if isinstance(item, lexer.TokenType):
                right_hand += item.value
            elif type(item) is str:
                right_hand += item
            else:
                raise ValueError(item)
        if len(self.right) == self.pos:
            right_hand += '●'

        return f'<{self.__class__.__name__}%s {self.left}→{right_hand.strip()}>' % (
            '@' if self.auto_generated else ''
        )

    __repr__ = __str__

    def shift_cursor(self) -> 'StateItem':
        return StateItem(
            left=self.left,
            right=self.right,
            pos=self.pos + 1,
            cfg_id=self.cfg_id,
        )


class State:
    def __init__(self, *args: StateItem):
        self.root_items: List[StateItem] = sorted(list(args), key=str)
        self.items: List[StateItem] = sorted(list(args), key=str)
        self.idx: Optional[int] = None
        self.is_expanded: bool = False
        self.reduces: List[int] = list()
        self.shifts_by_terminal: Dict[str, int] = dict()
        self.shifts_by_non_terminal: Dict[str, int] = dict()

    def __str__(self):
        content = ''
        if self.items:
            for k, item in enumerate(self.items):
                content += '\n' + '  ' + str(item)
            content += '\n'

        return f'<{self.__class__.__name__} %s>%s</{self.__class__.__name__}>' % (
            ' '.join((
                f'idx={self.idx}' if self.idx is not None else '?',
                ('*' if self.is_expanded is False else ''),
                'shift=' + ';'.join(
                    f'{k}:{v}' for k, v in {**self.shifts_by_terminal, **self.shifts_by_non_terminal}.items()
                ),
            )),
            content
        )

    __repr__ = __str__


class ParserBuilder:
    def __init__(self):
        self.states: Dict[int, State] = dict()
        self.non_terminals: Dict[str, List[int]] = dict()
        self.first_set: Dict[str, Set[str]] = dict()
        self.follow_set: Dict[str, Set[str]] = dict()
        self.cfg: Dict[int, Tuple[str, List[str | lexer.TokenType]]] = dict()
        self.cfg_group: Dict[str, List[List[str | lexer.TokenType]]] = dict()

    def build_first_set(self) -> Dict[str, Set[str]]:
        first_set_non_terminals: Dict[str, Set[str]] = dict()
        first_set_terminals: Dict[str, Set[str]] = dict()
        for left, right in self.cfg.values():
            try:
                if right[0] in self.non_terminals:
                    if left not in first_set_non_terminals:
                        first_set_non_terminals[left] = set()
                    first_set_non_terminals[left].add(right[0])
                else:
                    if left not in first_set_terminals:
                        first_set_terminals[left] = set()
                    first_set_terminals[left].add(right[0])
            except IndexError as e:
                raise IndexError(f'{e} from {left}')
        completed = set(self.non_terminals).difference(first_set_non_terminals.keys())
        expand_queue: List[str] = list(first_set_non_terminals.keys())
        while expand_queue:
            target = expand_queue[0]
            expandable = True
            for non_term in first_set_non_terminals[target]:
                if non_term not in completed and non_term != target:
                    if target in first_set_non_terminals[non_term]:
                        for another_non_term in first_set_non_terminals[non_term]:
                            if another_non_term != target and another_non_term not in completed:
                                expandable = False
                                break
                    else:
                        expandable = False

                    if expandable is False:
                        # print(f' **** cant expand {non_term!r}, of {target!r}')
                        # print(f'{non_term!r}: {first_set_non_terminals[non_term]}')
                        # print(f'{target!r}: {first_set_non_terminals[target]}')
                        break
            if expandable is False:
                # Put back
                expand_queue.append(expand_queue[0])
                del expand_queue[0]
                # print(f'putback {target!r}')
                continue
            else:
                # print(f'first-set expand {target!r}')
                if target not in first_set_terminals:
                    first_set_terminals[target] = set()
                for non_term in first_set_non_terminals[target]:
                    first_set_terminals[target] |= first_set_terminals[non_term]
                completed.add(target)
                del expand_queue[0]
        return first_set_terminals

    def build_follow_set(self) -> Dict[str, Set[str]]:
        follow_set: Dict[str, Set[str]] = dict()
        completed: Set[str] = set()
        expand_queue: List[str] = list(self.non_terminals.keys())
        inheritors_dict: Dict[str, Set[str]] = dict()
        while len(expand_queue) > 0:
            expandable = True
            follow_terminals = set()
            inherit_follow_set = set()
            target = expand_queue[0]

            if target in completed:
                del expand_queue[0]
                continue

            if target not in inheritors_dict:
                inheritors = set()

                for right in self.cfg_group[target]:
                    if len(right) != 1:
                        continue

                    inheritor_candidate = right[-1]
                    # print('YYYYYY', inheritor_candidate)
                    other_uses = False
                    for cfg_idx, (other_left, other_right) in self.cfg.items():
                        if len(other_right) == 1 and (other_left == target or other_left in inheritors):
                            continue
                        if inheritor_candidate in other_right:
                            # print('       === ', other_left, '→', other_right)
                            other_uses = True
                            break
                    # print('   *** other_uses', other_uses)
                    if other_uses is False:
                        inheritors.add(inheritor_candidate)
                inheritors_dict[target] = inheritors
            else:
                inheritors = inheritors_dict[target]

            try:
                for cfg_idx, (left, right) in self.cfg.items():
                    for k, e in enumerate(right):
                        if e != target and e not in inheritors:
                            continue

                        if k + 1 < len(right):
                            follow_token = right[k + 1]
                            if follow_token in self.non_terminals:
                                follow_terminals |= self.first_set[follow_token]
                            else:
                                follow_terminals.add(follow_token)
                        else:
                            if left == target:
                                pass
                            else:
                                if right[-1] == target and left in inheritors:  # recursive
                                    # print('@@@@@', repr(target), '====', left, '→', right)
                                    continue
                                if left not in completed:
                                    # print(f'{left!r} not completed, of {target!r}')
                                    # print(f'  * {target!r} inherited by {inheritors!r}')
                                    raise StopIteration()
                                else:
                                    inherit_follow_set.add(left)
            except StopIteration:
                expandable = False

            if expandable is False:
                expand_queue.append(target)
                del expand_queue[0]
                continue
            else:
                for src in inherit_follow_set:
                    follow_terminals |= follow_set[src]
                follow_set[target] = follow_terminals
                completed.add(target)

                for inheritor in inheritors:
                    follow_set[inheritor] = follow_terminals
                    completed.add(inheritor)

                del expand_queue[0]
        return follow_set

    def assign_cfg(self, left: str, right: List[str | lexer.TokenType]):
        list_of_right: List[List[str | lexer.TokenType]] = list()
        list_of_right.append(right)
        # print(f'CFG---------{left} {right}')
        while True:
            expanded_right = list()
            continue_expanding = False
            for right in list(list_of_right):
                expanded = False
                for k1, case_token in enumerate(right):
                    if type(case_token) is not str:
                        continue
                    if case_token.endswith('?'):
                        expanded = True
                        case_0_exists = list()
                        case_1_not_exists = list()
                        for k2, org_token in enumerate(right):
                            if k1 == k2:
                                case_0_exists.append(org_token[:-1])
                            else:
                                case_0_exists.append(org_token)
                                case_1_not_exists.append(org_token)
                        # insert if not duplicated
                        for old_right in expanded_right:
                            if old_right == case_0_exists:
                                break
                        else:
                            expanded_right.append(case_0_exists)
                        for old_right in expanded_right:
                            if old_right == case_1_not_exists:
                                break
                        else:
                            expanded_right.append(case_1_not_exists)
                    elif '|' in case_token.replace(r'\|', ''):
                        expanded = True
                        for token_in_case in case_token.replace(r'\|', '{pipe}').split('|'):
                            token_in_case = token_in_case.replace('{pipe}', '|')
                            right_in_case = list()
                            for k2, org_token in enumerate(right):
                                if k1 == k2:
                                    right_in_case.append(token_in_case)
                                else:
                                    right_in_case.append(org_token)
                            # insert if not duplicated
                            for old_right in expanded_right:
                                if old_right == right_in_case:
                                    break
                            else:
                                expanded_right.append(right_in_case)
                if expanded:
                    continue_expanding = True
                else:
                    # insert if not duplicated
                    for old_right in expanded_right:
                        if old_right == right:
                            break
                    else:
                        expanded_right.append(right)
            if not continue_expanding:
                list_of_right = expanded_right
                break
            else:
                list_of_right = expanded_right
                pass  # pprint(expanded_right)

        for right in list_of_right:
            cfg_id = len(self.cfg) + 1

            for token in right:
                if type(token) is not str:
                    continue
                if token.endswith('?') or '|' in token:
                    raise ValueError(f'{left}, {right}')
            self.cfg[cfg_id] = left, right

            if left not in self.cfg_group:
                self.cfg_group[left] = list()
            self.cfg_group[left].append(right)

            if left not in self.non_terminals:
                self.non_terminals[left] = list()
            self.non_terminals[left].append(cfg_id)

    def build(self, cfg: List[Tuple[str, List]]):
        ignite_item = 'S', ['dml', lexer.TokenType.EOF]
        self.cfg[0] = ignite_item

        for cfg_id, (left, right) in enumerate(cfg, start=1):
            self.assign_cfg(left, right)
        # pprint(self.cfg)

        print('*** build_first_set ***')
        self.first_set = self.build_first_set()
        print('*** build_follow_set ***')
        self.follow_set = self.build_follow_set()
        self.assign_state(State(StateItem(left=ignite_item[0], right=ignite_item[1], cfg_id=0), ))

        print('*** expand ***')
        try_attempts = 1000000000000
        completed_state = 0
        while try_attempts > 0 and completed_state < len(self.states):
            try_attempts -= 1
            state = self.states[completed_state]
            completed_state += 1
            # print('expanding: ', state)
            self.expand(state)
            # print('expanded: ', state)

        for state in self.states.values():
            if len(state.reduces) > 1:
                for r1 in state.reduces:
                    left1, right1 = self.cfg[r1]
                    for r2 in state.reduces:
                        if r1 == r2:
                            continue
                        left2, right2 = self.cfg[r2]
                        intersect = self.follow_set[left1].intersection(self.follow_set[left2])
                        if intersect:
                            print(state)
                            raise ValueError(
                                f'Reduce duplicated{intersect} [{r1},{r2}] from {state.idx}\n'
                                f' * {left1}→{right1} ☞ {self.follow_set[left1]}\n'
                                f' * {left2}→{right2} ☞ {self.follow_set[left2]}'
                            )
        print('*** write_to_code ***')
        self.write_to_code()

    def write_to_code(self):
        with open('parser.py', 'w', encoding='utf-8') as write_file:
            tab = ' ' * 4
            print('from typing import List, Tuple', file=write_file)
            print('', file=write_file)
            print('from lexer import TokenType', file=write_file)
            print('from ParseTree import ParseTree', file=write_file)
            print('', file=write_file)
            print('', file=write_file)
            print('def parse(input_tokens: List[Tuple[TokenType, str]]) -> List[ParseTree]:', file=write_file)
            print(tab + 'tree_stack: List[ParseTree] = list()', file=write_file)
            print(tab + 'state_stack: List[int] = [0,]', file=write_file)
            print(tab + 'while input_tokens:', file=write_file)
            print(tab * 2 + 'lookahead_typ, lookahead = input_tokens[0]', file=write_file)
            print(tab * 2 + 'state: int = state_stack[-1]', file=write_file)
            print(tab * 2 + 'print("#########################")', file=write_file)
            print(tab * 2 + 'print("tree_stack:")', file=write_file)
            print(tab * 2 + 'print(*tree_stack[-3:], sep="\\n")', file=write_file)
            print(tab * 2 + 'print("state_stack:", state_stack)', file=write_file)
            print(tab * 2 + 'print("input_tokens:", repr(input_tokens[:3]))', file=write_file)
            print(tab * 2 + 'match state:', file=write_file)
            for state in self.states.values():
                print(tab * 3 + 'case %d:' % state.idx, file=write_file)
                for item in state.items:
                    if item.left == 'S':
                        follows = 'EOF'
                    else:
                        follows = ' '.join(sorted([
                            item.value if isinstance(item, lexer.TokenType) else item for item in
                            self.follow_set[item.left]
                        ]))
                    print(tab * 4 + '#', item, '☞', follows, file=write_file)
                k = 0
                for k, (key, dst_state) in enumerate(state.shifts_by_non_terminal.items(), start=k):
                    if type(key) is str:
                        print(tab * 4, f'{"if" if k == 0 else "elif"} '
                                       f'len(tree_stack) > 0 and tree_stack[-1].name == {repr(key)}:', file=write_file,
                              sep='')
                    else:
                        raise TypeError(key)
                    print(tab * 5 + f'print("▶ SHIFT : ({key})")', file=write_file)
                    print(tab * 5 + f'if tree_stack[-1].name == {key!r}:', file=write_file)
                    print(tab * 6, f'pass', file=write_file,
                          sep='')
                    print(tab * 5 + f'else:', file=write_file)
                    print(tab * 6 + f'if tree_stack[-1].data:', file=write_file)
                    print(tab * 7, f'new_tree = ParseTree(name={key!r}, data=tree_stack[-1].data)', file=write_file,
                          sep='')
                    print(tab * 6 + f'else:', file=write_file)
                    print(tab * 7, f'new_tree = ParseTree(name={key!r}, children=(tree_stack[-1],))', file=write_file,
                          sep='')
                    print(tab * 6, f'del tree_stack[-1]', file=write_file, sep='')
                    print(tab * 6, f'tree_stack.append(new_tree)', file=write_file, sep='')
                    print(tab * 5, f'state_stack.append({dst_state})', file=write_file, sep='')
                    print(tab * 5, f'continue', file=write_file, sep='')
                for k, (key, dst_state) in enumerate(state.shifts_by_terminal.items(), start=k):
                    if type(key) is str:
                        print(tab * 4, f'if lookahead == {repr(key)}:',
                              file=write_file,
                              sep='')
                    elif isinstance(key, lexer.TokenType):
                        print(tab * 4, f'if lookahead_typ.value == {repr(key.value)}:',
                              file=write_file,
                              sep='')
                    else:
                        raise TypeError(key)
                    if isinstance(key, lexer.TokenType) and key == lexer.TokenType.EOF:
                        print(tab * 5 + f'print("▶ ACCEPT : (%s,%s)"%(lookahead_typ, repr(lookahead)))',
                              file=write_file)
                        print(tab * 5 + f'return tree_stack', file=write_file)

                    else:
                        print(tab * 5 + f'print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))', file=write_file)

                        print(tab * 5, f'del input_tokens[0]', file=write_file, sep='')
                        if isinstance(key, lexer.TokenType):
                            print(tab * 5, f'tree_stack.append(ParseTree(name={key.value!r}, data=lookahead))',
                                  file=write_file,
                                  sep='')
                        else:
                            print(tab * 5, f'tree_stack.append(ParseTree(name={key!r}, data=lookahead))',
                                  file=write_file,
                                  sep='')
                        print(tab * 5, f'state_stack.append({dst_state})', file=write_file, sep='')
                        print(tab * 5, f'continue', file=write_file, sep='')

                # assert len(state.reduces) <= 1, state.reduces
                if state.reduces:
                    for cfg_id in state.reduces:
                        reduce_left, reduce_right = self.cfg[cfg_id]
                        reduce_conditions = list()
                        if reduce_left == 'S':
                            reduce_condition = 'True'
                            follows = 'EOF'
                        else:
                            for key in self.follow_set[reduce_left]:
                                if isinstance(key, lexer.TokenType):
                                    reduce_conditions.append(f'lookahead_typ.value == {key.value!r}')
                                else:
                                    reduce_conditions.append(f'lookahead == {key!r}')
                            if reduce_conditions:
                                if len(reduce_conditions) > 1:
                                    reduce_condition = '( ' + (
                                        f'\n{tab * 4}  or '.join(reduce_conditions)
                                    ) + f'\n{tab * 4})'
                                else:
                                    reduce_condition = reduce_conditions[0]
                            follows = ' '.join(sorted([
                                item.value if isinstance(item, lexer.TokenType) else item for item in
                                self.follow_set[reduce_left]
                            ]))

                        print(tab * 4 + f'if {reduce_condition}:', file=write_file)
                        print(
                            tab * 5 + f'print("▶ REDUCE : {reduce_left} → {" ".join(map(str, reduce_right))} ☞ {follows}")',
                            file=write_file)
                        print(tab * 5 + 'children=list()', file=write_file)
                        print(tab * 5 + 'for k in range(%d):' % len(reduce_right), file=write_file)
                        print(tab * 6 + 'tree = tree_stack.pop()', file=write_file)
                        print(tab * 6 + f'if tree.name == {reduce_left!r}:', file=write_file)
                        print(tab * 7 + 'children += list(reversed(tree.children))', file=write_file)
                        print(tab * 6 + 'else:', file=write_file)
                        print(tab * 7 + 'children.append(tree)', file=write_file)
                        print(tab * 6 + 'state_stack.pop()', file=write_file)
                        print(tab * 5 + 'children.reverse()', file=write_file)
                        print(tab * 5 + f'tree_stack.append(ParseTree(name={reduce_left!r}, children=children))',
                              file=write_file)
                        print(tab * 5 + 'continue', file=write_file)
                print(
                    tab * 4,
                    f'raise NotImplementedError("Unexpected(%s;%s, expected={" ".join(map(str, state.shifts_by_terminal.keys()))!r})" % (lookahead_typ, repr(lookahead)))',
                    file=write_file,
                    sep=''
                )
                print(tab * 4, file=write_file)
            # print(tab * 1 + 'return tree_stack', file=write_file)

    def expand(self, state: State):
        expanded_non_terminals: List[str] = list()
        completed_item: int = 0
        shifts_terminals: Set[str] = set()
        shifts_non_terminals: Set[str] = set()
        while completed_item < len(state.items):
            item = state.items[completed_item]
            completed_item += 1
            if item.pos == len(item.right):
                if item.cfg_id not in state.reduces:
                    state.reduces.append(item.cfg_id)
                continue
            if item.right[item.pos] in self.non_terminals:
                non_terminal = item.right[item.pos]
                if non_terminal not in expanded_non_terminals:
                    expanded_non_terminals.append(non_terminal)
                    for cfg_id in self.non_terminals[non_terminal]:
                        left, right = self.cfg[cfg_id]
                        # print('●●●●●●●●●●●●112')
                        state.items.append(StateItem(left=left, right=right, cfg_id=cfg_id, auto_generated=True))
                shifts_non_terminals.add(non_terminal)
            else:
                terminal = item.right[item.pos]
                # print('●●●●●●●●●●●●120', repr(terminal))
                shifts_terminals.add(terminal)
        # print('●●●●●●●●●●●●122', repr(shifts))
        for key in shifts_non_terminals:
            dst = self.transition_state(src=state, key=key)
            state.shifts_by_non_terminal[key] = dst.idx
        for key in shifts_terminals:
            dst = self.transition_state(src=state, key=key)
            state.shifts_by_terminal[key] = dst.idx
        state.is_expanded = True

    def transition_state(self, src: State, key: Union[str, lexer.TokenType]):
        items = list()
        for item in src.items:
            if item.pos < len(item.right) and item.right[item.pos] == key:
                items.append(item.shift_cursor())
        dst = State(*items)
        idx = self.exist_state(dst)
        if idx:
            return self.states[idx]
        else:
            self.assign_state(dst)
            return dst

    def exist_state(self, lhs: State) -> Optional[int]:
        for rhs in self.states.values():
            if len(lhs.root_items) != len(rhs.root_items):
                continue
            matched = True
            for k, left_item in enumerate(lhs.root_items):
                right_item = rhs.root_items[k]
                if left_item.left != right_item.left:
                    matched = False
                    break
                if left_item.pos != right_item.pos:
                    matched = False
                    break
                if len(left_item.right) != len(right_item.right):
                    matched = False
                    break
                for k2, left_token in enumerate(left_item.right):
                    right_token = right_item.right[k2]
                    if left_token != right_token:
                        matched = False
                        break
            if matched:
                return rhs.idx
        return None

    def assign_state(self, state: State) -> int:
        idx = len(self.states)
        self.states[idx] = state
        state.idx = idx
        return idx
