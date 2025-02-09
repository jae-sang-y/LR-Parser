from typing import List, Tuple

from lexer import TokenType
from ParseTree import ParseTree


def parse(input_tokens: List[Tuple[TokenType, str]]) -> List[ParseTree]:
    tree_stack: List[ParseTree] = list()
    state_stack: List[int] = [0,]
    while input_tokens:
        lookahead_typ, lookahead = input_tokens[0]
        state: int = state_stack[-1]
        print("#########################")
        print("tree_stack:")
        print(*tree_stack[-3:], sep="\n")
        print("state_stack:", state_stack)
        print("input_tokens:", repr(input_tokens[:3]))
        match state:
            case 0:
                # <StateItem S→●query EOF> ☞ EOF
                # <StateItem@ query→●insert_statement> ☞ EOF
                # <StateItem@ insert_statement→●INSERT INTO dst select-query> ☞ EOF
                if len(tree_stack) > 0 and tree_stack[-1].name == 'query':
                    print("▶ SHIFT : (query)")
                    if tree_stack[-1].name == 'query':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='query', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='query', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(1)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'insert_statement':
                    print("▶ SHIFT : (insert_statement)")
                    if tree_stack[-1].name == 'insert_statement':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='insert_statement', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='insert_statement', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(2)
                    continue
                if lookahead == 'INSERT':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='INSERT', data=lookahead))
                    state_stack.append(3)
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='INSERT')" % (lookahead_typ, repr(lookahead)))
                
            case 1:
                # <StateItem S→query ●EOF> ☞ EOF
                if lookahead_typ.value == 'EOF':
                    print("▶ ACCEPT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    return tree_stack
                raise NotImplementedError("Unexpected(%s;%s, expected='TokenType.EOF')" % (lookahead_typ, repr(lookahead)))
                
            case 2:
                # <StateItem query→insert_statement●> ☞ EOF
                if lookahead_typ.value == 'EOF':
                    print("▶ REDUCE : query → insert_statement ☞ EOF")
                    children=list()
                    for k in range(1):
                        tree = tree_stack.pop()
                        if tree.name == 'query':
                            children += list(reversed(tree.children))
                        else:
                            children.append(tree)
                        state_stack.pop()
                    children.reverse()
                    tree_stack.append(ParseTree(name='query', children=children))
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='')" % (lookahead_typ, repr(lookahead)))
                
            case 3:
                # <StateItem insert_statement→INSERT ●INTO dst select-query> ☞ EOF
                if lookahead == 'INTO':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='INTO', data=lookahead))
                    state_stack.append(5)
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='INTO')" % (lookahead_typ, repr(lookahead)))
                
            case 4:
                # <StateItem S→query EOF●> ☞ EOF
                if True:
                    print("▶ REDUCE : S → query TokenType.EOF ☞ EOF")
                    children=list()
                    for k in range(2):
                        tree = tree_stack.pop()
                        if tree.name == 'S':
                            children += list(reversed(tree.children))
                        else:
                            children.append(tree)
                        state_stack.pop()
                    children.reverse()
                    tree_stack.append(ParseTree(name='S', children=children))
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='')" % (lookahead_typ, repr(lookahead)))
                
            case 5:
                # <StateItem insert_statement→INSERT INTO ●dst select-query> ☞ EOF
                # <StateItem@ dst→●IDT . IDT> ☞ , EOF GROUP IDT SELECT WHERE
                if len(tree_stack) > 0 and tree_stack[-1].name == 'dst':
                    print("▶ SHIFT : (dst)")
                    if tree_stack[-1].name == 'dst':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='dst', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='dst', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(6)
                    continue
                if lookahead_typ.value == 'IDT':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='IDT', data=lookahead))
                    state_stack.append(7)
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='TokenType.identifier')" % (lookahead_typ, repr(lookahead)))
                
            case 6:
                # <StateItem insert_statement→INSERT INTO dst ●select-query> ☞ EOF
                # <StateItem@ select-query→●SELECT select-list FROM sources> ☞ EOF
                # <StateItem@ select-query→●SELECT select-list FROM sources where_clause> ☞ EOF
                # <StateItem@ select-query→●SELECT select-list FROM sources groupby_clause> ☞ EOF
                # <StateItem@ select-query→●SELECT select-list FROM sources where_clause groupby_clause> ☞ EOF
                if len(tree_stack) > 0 and tree_stack[-1].name == 'select-query':
                    print("▶ SHIFT : (select-query)")
                    if tree_stack[-1].name == 'select-query':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='select-query', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='select-query', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(8)
                    continue
                if lookahead == 'SELECT':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SELECT', data=lookahead))
                    state_stack.append(9)
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='SELECT')" % (lookahead_typ, repr(lookahead)))
                
            case 7:
                # <StateItem dst→IDT ●. IDT> ☞ , EOF GROUP IDT SELECT WHERE
                if lookahead == '.':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='.', data=lookahead))
                    state_stack.append(10)
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='.')" % (lookahead_typ, repr(lookahead)))
                
            case 8:
                # <StateItem insert_statement→INSERT INTO dst select-query●> ☞ EOF
                if lookahead_typ.value == 'EOF':
                    print("▶ REDUCE : insert_statement → INSERT INTO dst select-query ☞ EOF")
                    children=list()
                    for k in range(4):
                        tree = tree_stack.pop()
                        if tree.name == 'insert_statement':
                            children += list(reversed(tree.children))
                        else:
                            children.append(tree)
                        state_stack.pop()
                    children.reverse()
                    tree_stack.append(ParseTree(name='insert_statement', children=children))
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='')" % (lookahead_typ, repr(lookahead)))
                
            case 9:
                # <StateItem select-query→SELECT ●select-list FROM sources groupby_clause> ☞ EOF
                # <StateItem select-query→SELECT ●select-list FROM sources where_clause groupby_clause> ☞ EOF
                # <StateItem select-query→SELECT ●select-list FROM sources where_clause> ☞ EOF
                # <StateItem select-query→SELECT ●select-list FROM sources> ☞ EOF
                # <StateItem@ select-list→●expr , select-list> ☞ FROM
                # <StateItem@ select-list→●expr> ☞ FROM
                # <StateItem@ expr→●IDT . IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SQL> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SMP> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SUM ( expr )> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                if len(tree_stack) > 0 and tree_stack[-1].name == 'expr':
                    print("▶ SHIFT : (expr)")
                    if tree_stack[-1].name == 'expr':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='expr', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='expr', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(11)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'select-list':
                    print("▶ SHIFT : (select-list)")
                    if tree_stack[-1].name == 'select-list':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='select-list', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='select-list', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(12)
                    continue
                if lookahead_typ.value == 'SMP':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SMP', data=lookahead))
                    state_stack.append(13)
                    continue
                if lookahead == 'SUM':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SUM', data=lookahead))
                    state_stack.append(14)
                    continue
                if lookahead_typ.value == 'IDT':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='IDT', data=lookahead))
                    state_stack.append(15)
                    continue
                if lookahead_typ.value == 'SQL':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SQL', data=lookahead))
                    state_stack.append(16)
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='TokenType.sql_mapper_parameter SUM TokenType.identifier TokenType.single_quoted_literal')" % (lookahead_typ, repr(lookahead)))
                
            case 10:
                # <StateItem dst→IDT . ●IDT> ☞ , EOF GROUP IDT SELECT WHERE
                if lookahead_typ.value == 'IDT':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='IDT', data=lookahead))
                    state_stack.append(17)
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='TokenType.identifier')" % (lookahead_typ, repr(lookahead)))
                
            case 11:
                # <StateItem select-list→expr ●, select-list> ☞ FROM
                # <StateItem select-list→expr●> ☞ FROM
                if lookahead == ',':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name=',', data=lookahead))
                    state_stack.append(18)
                    continue
                if lookahead == 'FROM':
                    print("▶ REDUCE : select-list → expr ☞ FROM")
                    children=list()
                    for k in range(1):
                        tree = tree_stack.pop()
                        if tree.name == 'select-list':
                            children += list(reversed(tree.children))
                        else:
                            children.append(tree)
                        state_stack.pop()
                    children.reverse()
                    tree_stack.append(ParseTree(name='select-list', children=children))
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected=',')" % (lookahead_typ, repr(lookahead)))
                
            case 12:
                # <StateItem select-query→SELECT select-list ●FROM sources groupby_clause> ☞ EOF
                # <StateItem select-query→SELECT select-list ●FROM sources where_clause groupby_clause> ☞ EOF
                # <StateItem select-query→SELECT select-list ●FROM sources where_clause> ☞ EOF
                # <StateItem select-query→SELECT select-list ●FROM sources> ☞ EOF
                if lookahead == 'FROM':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='FROM', data=lookahead))
                    state_stack.append(19)
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='FROM')" % (lookahead_typ, repr(lookahead)))
                
            case 13:
                # <StateItem expr→SMP●> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                if ( lookahead == '='
                  or lookahead == 'FROM'
                  or lookahead_typ.value == 'EOF'
                  or lookahead == '<'
                  or lookahead == '<='
                  or lookahead == '^='
                  or lookahead == '<>'
                  or lookahead == 'GROUP'
                  or lookahead == '!='
                  or lookahead == 'OR'
                  or lookahead == ')'
                  or lookahead == 'AND'
                  or lookahead == ','
                  or lookahead == '>'
                  or lookahead == '>='
                ):
                    print("▶ REDUCE : expr → TokenType.sql_mapper_parameter ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=")
                    children=list()
                    for k in range(1):
                        tree = tree_stack.pop()
                        if tree.name == 'expr':
                            children += list(reversed(tree.children))
                        else:
                            children.append(tree)
                        state_stack.pop()
                    children.reverse()
                    tree_stack.append(ParseTree(name='expr', children=children))
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='')" % (lookahead_typ, repr(lookahead)))
                
            case 14:
                # <StateItem expr→SUM ●( expr )> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                if lookahead == '(':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='(', data=lookahead))
                    state_stack.append(20)
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='(')" % (lookahead_typ, repr(lookahead)))
                
            case 15:
                # <StateItem expr→IDT ●. IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem expr→IDT●> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                if lookahead == '.':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='.', data=lookahead))
                    state_stack.append(21)
                    continue
                if ( lookahead == '='
                  or lookahead == 'FROM'
                  or lookahead_typ.value == 'EOF'
                  or lookahead == '<'
                  or lookahead == '<='
                  or lookahead == '^='
                  or lookahead == '<>'
                  or lookahead == 'GROUP'
                  or lookahead == '!='
                  or lookahead == 'OR'
                  or lookahead == ')'
                  or lookahead == 'AND'
                  or lookahead == ','
                  or lookahead == '>'
                  or lookahead == '>='
                ):
                    print("▶ REDUCE : expr → TokenType.identifier ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=")
                    children=list()
                    for k in range(1):
                        tree = tree_stack.pop()
                        if tree.name == 'expr':
                            children += list(reversed(tree.children))
                        else:
                            children.append(tree)
                        state_stack.pop()
                    children.reverse()
                    tree_stack.append(ParseTree(name='expr', children=children))
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='.')" % (lookahead_typ, repr(lookahead)))
                
            case 16:
                # <StateItem expr→SQL●> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                if ( lookahead == '='
                  or lookahead == 'FROM'
                  or lookahead_typ.value == 'EOF'
                  or lookahead == '<'
                  or lookahead == '<='
                  or lookahead == '^='
                  or lookahead == '<>'
                  or lookahead == 'GROUP'
                  or lookahead == '!='
                  or lookahead == 'OR'
                  or lookahead == ')'
                  or lookahead == 'AND'
                  or lookahead == ','
                  or lookahead == '>'
                  or lookahead == '>='
                ):
                    print("▶ REDUCE : expr → TokenType.single_quoted_literal ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=")
                    children=list()
                    for k in range(1):
                        tree = tree_stack.pop()
                        if tree.name == 'expr':
                            children += list(reversed(tree.children))
                        else:
                            children.append(tree)
                        state_stack.pop()
                    children.reverse()
                    tree_stack.append(ParseTree(name='expr', children=children))
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='')" % (lookahead_typ, repr(lookahead)))
                
            case 17:
                # <StateItem dst→IDT . IDT●> ☞ , EOF GROUP IDT SELECT WHERE
                if ( lookahead_typ.value == 'EOF'
                  or lookahead == 'WHERE'
                  or lookahead_typ.value == 'IDT'
                  or lookahead == 'SELECT'
                  or lookahead == ','
                  or lookahead == 'GROUP'
                ):
                    print("▶ REDUCE : dst → TokenType.identifier . TokenType.identifier ☞ , EOF GROUP IDT SELECT WHERE")
                    children=list()
                    for k in range(3):
                        tree = tree_stack.pop()
                        if tree.name == 'dst':
                            children += list(reversed(tree.children))
                        else:
                            children.append(tree)
                        state_stack.pop()
                    children.reverse()
                    tree_stack.append(ParseTree(name='dst', children=children))
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='')" % (lookahead_typ, repr(lookahead)))
                
            case 18:
                # <StateItem select-list→expr , ●select-list> ☞ FROM
                # <StateItem@ select-list→●expr , select-list> ☞ FROM
                # <StateItem@ select-list→●expr> ☞ FROM
                # <StateItem@ expr→●IDT . IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SQL> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SMP> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SUM ( expr )> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                if len(tree_stack) > 0 and tree_stack[-1].name == 'expr':
                    print("▶ SHIFT : (expr)")
                    if tree_stack[-1].name == 'expr':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='expr', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='expr', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(11)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'select-list':
                    print("▶ SHIFT : (select-list)")
                    if tree_stack[-1].name == 'select-list':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='select-list', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='select-list', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(22)
                    continue
                if lookahead_typ.value == 'SMP':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SMP', data=lookahead))
                    state_stack.append(13)
                    continue
                if lookahead == 'SUM':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SUM', data=lookahead))
                    state_stack.append(14)
                    continue
                if lookahead_typ.value == 'IDT':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='IDT', data=lookahead))
                    state_stack.append(15)
                    continue
                if lookahead_typ.value == 'SQL':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SQL', data=lookahead))
                    state_stack.append(16)
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='TokenType.sql_mapper_parameter SUM TokenType.identifier TokenType.single_quoted_literal')" % (lookahead_typ, repr(lookahead)))
                
            case 19:
                # <StateItem select-query→SELECT select-list FROM ●sources groupby_clause> ☞ EOF
                # <StateItem select-query→SELECT select-list FROM ●sources where_clause groupby_clause> ☞ EOF
                # <StateItem select-query→SELECT select-list FROM ●sources where_clause> ☞ EOF
                # <StateItem select-query→SELECT select-list FROM ●sources> ☞ EOF
                # <StateItem@ sources→●source , sources> ☞ EOF GROUP WHERE
                # <StateItem@ sources→●source> ☞ EOF GROUP WHERE
                # <StateItem@ source→●dst> ☞ , EOF GROUP WHERE
                # <StateItem@ source→●dst IDT> ☞ , EOF GROUP WHERE
                # <StateItem@ dst→●IDT . IDT> ☞ , EOF GROUP IDT SELECT WHERE
                if len(tree_stack) > 0 and tree_stack[-1].name == 'sources':
                    print("▶ SHIFT : (sources)")
                    if tree_stack[-1].name == 'sources':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='sources', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='sources', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(23)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'source':
                    print("▶ SHIFT : (source)")
                    if tree_stack[-1].name == 'source':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='source', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='source', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(24)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'dst':
                    print("▶ SHIFT : (dst)")
                    if tree_stack[-1].name == 'dst':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='dst', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='dst', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(25)
                    continue
                if lookahead_typ.value == 'IDT':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='IDT', data=lookahead))
                    state_stack.append(7)
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='TokenType.identifier')" % (lookahead_typ, repr(lookahead)))
                
            case 20:
                # <StateItem expr→SUM ( ●expr )> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●IDT . IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SQL> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SMP> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SUM ( expr )> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                if len(tree_stack) > 0 and tree_stack[-1].name == 'expr':
                    print("▶ SHIFT : (expr)")
                    if tree_stack[-1].name == 'expr':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='expr', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='expr', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(26)
                    continue
                if lookahead_typ.value == 'SMP':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SMP', data=lookahead))
                    state_stack.append(13)
                    continue
                if lookahead == 'SUM':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SUM', data=lookahead))
                    state_stack.append(14)
                    continue
                if lookahead_typ.value == 'IDT':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='IDT', data=lookahead))
                    state_stack.append(15)
                    continue
                if lookahead_typ.value == 'SQL':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SQL', data=lookahead))
                    state_stack.append(16)
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='TokenType.sql_mapper_parameter SUM TokenType.identifier TokenType.single_quoted_literal')" % (lookahead_typ, repr(lookahead)))
                
            case 21:
                # <StateItem expr→IDT . ●IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                if lookahead_typ.value == 'IDT':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='IDT', data=lookahead))
                    state_stack.append(27)
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='TokenType.identifier')" % (lookahead_typ, repr(lookahead)))
                
            case 22:
                # <StateItem select-list→expr , select-list●> ☞ FROM
                if lookahead == 'FROM':
                    print("▶ REDUCE : select-list → expr , select-list ☞ FROM")
                    children=list()
                    for k in range(3):
                        tree = tree_stack.pop()
                        if tree.name == 'select-list':
                            children += list(reversed(tree.children))
                        else:
                            children.append(tree)
                        state_stack.pop()
                    children.reverse()
                    tree_stack.append(ParseTree(name='select-list', children=children))
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='')" % (lookahead_typ, repr(lookahead)))
                
            case 23:
                # <StateItem select-query→SELECT select-list FROM sources ●groupby_clause> ☞ EOF
                # <StateItem select-query→SELECT select-list FROM sources ●where_clause groupby_clause> ☞ EOF
                # <StateItem select-query→SELECT select-list FROM sources ●where_clause> ☞ EOF
                # <StateItem select-query→SELECT select-list FROM sources●> ☞ EOF
                # <StateItem@ groupby_clause→●GROUP BY groupby_clause_list> ☞ EOF
                # <StateItem@ where_clause→●WHERE condition> ☞ EOF GROUP
                if len(tree_stack) > 0 and tree_stack[-1].name == 'where_clause':
                    print("▶ SHIFT : (where_clause)")
                    if tree_stack[-1].name == 'where_clause':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='where_clause', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='where_clause', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(28)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'groupby_clause':
                    print("▶ SHIFT : (groupby_clause)")
                    if tree_stack[-1].name == 'groupby_clause':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='groupby_clause', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='groupby_clause', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(29)
                    continue
                if lookahead == 'WHERE':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='WHERE', data=lookahead))
                    state_stack.append(30)
                    continue
                if lookahead == 'GROUP':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='GROUP', data=lookahead))
                    state_stack.append(31)
                    continue
                if lookahead_typ.value == 'EOF':
                    print("▶ REDUCE : select-query → SELECT select-list FROM sources ☞ EOF")
                    children=list()
                    for k in range(4):
                        tree = tree_stack.pop()
                        if tree.name == 'select-query':
                            children += list(reversed(tree.children))
                        else:
                            children.append(tree)
                        state_stack.pop()
                    children.reverse()
                    tree_stack.append(ParseTree(name='select-query', children=children))
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='WHERE GROUP')" % (lookahead_typ, repr(lookahead)))
                
            case 24:
                # <StateItem sources→source ●, sources> ☞ EOF GROUP WHERE
                # <StateItem sources→source●> ☞ EOF GROUP WHERE
                if lookahead == ',':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name=',', data=lookahead))
                    state_stack.append(32)
                    continue
                if ( lookahead == 'WHERE'
                  or lookahead == 'GROUP'
                  or lookahead_typ.value == 'EOF'
                ):
                    print("▶ REDUCE : sources → source ☞ EOF GROUP WHERE")
                    children=list()
                    for k in range(1):
                        tree = tree_stack.pop()
                        if tree.name == 'sources':
                            children += list(reversed(tree.children))
                        else:
                            children.append(tree)
                        state_stack.pop()
                    children.reverse()
                    tree_stack.append(ParseTree(name='sources', children=children))
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected=',')" % (lookahead_typ, repr(lookahead)))
                
            case 25:
                # <StateItem source→dst ●IDT> ☞ , EOF GROUP WHERE
                # <StateItem source→dst●> ☞ , EOF GROUP WHERE
                if lookahead_typ.value == 'IDT':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='IDT', data=lookahead))
                    state_stack.append(33)
                    continue
                if ( lookahead == 'WHERE'
                  or lookahead == ','
                  or lookahead == 'GROUP'
                  or lookahead_typ.value == 'EOF'
                ):
                    print("▶ REDUCE : source → dst ☞ , EOF GROUP WHERE")
                    children=list()
                    for k in range(1):
                        tree = tree_stack.pop()
                        if tree.name == 'source':
                            children += list(reversed(tree.children))
                        else:
                            children.append(tree)
                        state_stack.pop()
                    children.reverse()
                    tree_stack.append(ParseTree(name='source', children=children))
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='TokenType.identifier')" % (lookahead_typ, repr(lookahead)))
                
            case 26:
                # <StateItem expr→SUM ( expr ●)> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                if lookahead == ')':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name=')', data=lookahead))
                    state_stack.append(34)
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected=')')" % (lookahead_typ, repr(lookahead)))
                
            case 27:
                # <StateItem expr→IDT . IDT●> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                if ( lookahead == '='
                  or lookahead == 'FROM'
                  or lookahead_typ.value == 'EOF'
                  or lookahead == '<'
                  or lookahead == '<='
                  or lookahead == '^='
                  or lookahead == '<>'
                  or lookahead == 'GROUP'
                  or lookahead == '!='
                  or lookahead == 'OR'
                  or lookahead == ')'
                  or lookahead == 'AND'
                  or lookahead == ','
                  or lookahead == '>'
                  or lookahead == '>='
                ):
                    print("▶ REDUCE : expr → TokenType.identifier . TokenType.identifier ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=")
                    children=list()
                    for k in range(3):
                        tree = tree_stack.pop()
                        if tree.name == 'expr':
                            children += list(reversed(tree.children))
                        else:
                            children.append(tree)
                        state_stack.pop()
                    children.reverse()
                    tree_stack.append(ParseTree(name='expr', children=children))
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='')" % (lookahead_typ, repr(lookahead)))
                
            case 28:
                # <StateItem select-query→SELECT select-list FROM sources where_clause ●groupby_clause> ☞ EOF
                # <StateItem select-query→SELECT select-list FROM sources where_clause●> ☞ EOF
                # <StateItem@ groupby_clause→●GROUP BY groupby_clause_list> ☞ EOF
                if len(tree_stack) > 0 and tree_stack[-1].name == 'groupby_clause':
                    print("▶ SHIFT : (groupby_clause)")
                    if tree_stack[-1].name == 'groupby_clause':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='groupby_clause', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='groupby_clause', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(35)
                    continue
                if lookahead == 'GROUP':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='GROUP', data=lookahead))
                    state_stack.append(31)
                    continue
                if lookahead_typ.value == 'EOF':
                    print("▶ REDUCE : select-query → SELECT select-list FROM sources where_clause ☞ EOF")
                    children=list()
                    for k in range(5):
                        tree = tree_stack.pop()
                        if tree.name == 'select-query':
                            children += list(reversed(tree.children))
                        else:
                            children.append(tree)
                        state_stack.pop()
                    children.reverse()
                    tree_stack.append(ParseTree(name='select-query', children=children))
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='GROUP')" % (lookahead_typ, repr(lookahead)))
                
            case 29:
                # <StateItem select-query→SELECT select-list FROM sources groupby_clause●> ☞ EOF
                if lookahead_typ.value == 'EOF':
                    print("▶ REDUCE : select-query → SELECT select-list FROM sources groupby_clause ☞ EOF")
                    children=list()
                    for k in range(5):
                        tree = tree_stack.pop()
                        if tree.name == 'select-query':
                            children += list(reversed(tree.children))
                        else:
                            children.append(tree)
                        state_stack.pop()
                    children.reverse()
                    tree_stack.append(ParseTree(name='select-query', children=children))
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='')" % (lookahead_typ, repr(lookahead)))
                
            case 30:
                # <StateItem where_clause→WHERE ●condition> ☞ EOF GROUP
                # <StateItem@ condition→●compound_condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ condition→●simple_comparison_condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●condition AND condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●condition OR condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●NOT condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●( condition )> ☞ ) AND EOF GROUP OR
                # <StateItem@ simple_comparison_condition→●expr simple_comparison_operator expr> ☞ ) AND EOF GROUP OR
                # <StateItem@ expr→●IDT . IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SQL> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SMP> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SUM ( expr )> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                if len(tree_stack) > 0 and tree_stack[-1].name == 'condition':
                    print("▶ SHIFT : (condition)")
                    if tree_stack[-1].name == 'condition':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='condition', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='condition', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(36)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'expr':
                    print("▶ SHIFT : (expr)")
                    if tree_stack[-1].name == 'expr':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='expr', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='expr', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(37)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'compound_condition':
                    print("▶ SHIFT : (compound_condition)")
                    if tree_stack[-1].name == 'compound_condition':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='compound_condition', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='compound_condition', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(38)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'simple_comparison_condition':
                    print("▶ SHIFT : (simple_comparison_condition)")
                    if tree_stack[-1].name == 'simple_comparison_condition':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='simple_comparison_condition', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='simple_comparison_condition', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(39)
                    continue
                if lookahead_typ.value == 'SMP':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SMP', data=lookahead))
                    state_stack.append(13)
                    continue
                if lookahead == 'NOT':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='NOT', data=lookahead))
                    state_stack.append(40)
                    continue
                if lookahead == 'SUM':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SUM', data=lookahead))
                    state_stack.append(14)
                    continue
                if lookahead_typ.value == 'SQL':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SQL', data=lookahead))
                    state_stack.append(16)
                    continue
                if lookahead == '(':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='(', data=lookahead))
                    state_stack.append(41)
                    continue
                if lookahead_typ.value == 'IDT':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='IDT', data=lookahead))
                    state_stack.append(15)
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='TokenType.sql_mapper_parameter NOT SUM TokenType.single_quoted_literal ( TokenType.identifier')" % (lookahead_typ, repr(lookahead)))
                
            case 31:
                # <StateItem groupby_clause→GROUP ●BY groupby_clause_list> ☞ EOF
                if lookahead == 'BY':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='BY', data=lookahead))
                    state_stack.append(42)
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='BY')" % (lookahead_typ, repr(lookahead)))
                
            case 32:
                # <StateItem sources→source , ●sources> ☞ EOF GROUP WHERE
                # <StateItem@ sources→●source , sources> ☞ EOF GROUP WHERE
                # <StateItem@ sources→●source> ☞ EOF GROUP WHERE
                # <StateItem@ source→●dst> ☞ , EOF GROUP WHERE
                # <StateItem@ source→●dst IDT> ☞ , EOF GROUP WHERE
                # <StateItem@ dst→●IDT . IDT> ☞ , EOF GROUP IDT SELECT WHERE
                if len(tree_stack) > 0 and tree_stack[-1].name == 'sources':
                    print("▶ SHIFT : (sources)")
                    if tree_stack[-1].name == 'sources':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='sources', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='sources', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(43)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'source':
                    print("▶ SHIFT : (source)")
                    if tree_stack[-1].name == 'source':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='source', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='source', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(24)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'dst':
                    print("▶ SHIFT : (dst)")
                    if tree_stack[-1].name == 'dst':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='dst', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='dst', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(25)
                    continue
                if lookahead_typ.value == 'IDT':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='IDT', data=lookahead))
                    state_stack.append(7)
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='TokenType.identifier')" % (lookahead_typ, repr(lookahead)))
                
            case 33:
                # <StateItem source→dst IDT●> ☞ , EOF GROUP WHERE
                if ( lookahead == 'WHERE'
                  or lookahead == ','
                  or lookahead == 'GROUP'
                  or lookahead_typ.value == 'EOF'
                ):
                    print("▶ REDUCE : source → dst TokenType.identifier ☞ , EOF GROUP WHERE")
                    children=list()
                    for k in range(2):
                        tree = tree_stack.pop()
                        if tree.name == 'source':
                            children += list(reversed(tree.children))
                        else:
                            children.append(tree)
                        state_stack.pop()
                    children.reverse()
                    tree_stack.append(ParseTree(name='source', children=children))
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='')" % (lookahead_typ, repr(lookahead)))
                
            case 34:
                # <StateItem expr→SUM ( expr )●> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                if ( lookahead == '='
                  or lookahead == 'FROM'
                  or lookahead_typ.value == 'EOF'
                  or lookahead == '<'
                  or lookahead == '<='
                  or lookahead == '^='
                  or lookahead == '<>'
                  or lookahead == 'GROUP'
                  or lookahead == '!='
                  or lookahead == 'OR'
                  or lookahead == ')'
                  or lookahead == 'AND'
                  or lookahead == ','
                  or lookahead == '>'
                  or lookahead == '>='
                ):
                    print("▶ REDUCE : expr → SUM ( expr ) ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=")
                    children=list()
                    for k in range(4):
                        tree = tree_stack.pop()
                        if tree.name == 'expr':
                            children += list(reversed(tree.children))
                        else:
                            children.append(tree)
                        state_stack.pop()
                    children.reverse()
                    tree_stack.append(ParseTree(name='expr', children=children))
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='')" % (lookahead_typ, repr(lookahead)))
                
            case 35:
                # <StateItem select-query→SELECT select-list FROM sources where_clause groupby_clause●> ☞ EOF
                if lookahead_typ.value == 'EOF':
                    print("▶ REDUCE : select-query → SELECT select-list FROM sources where_clause groupby_clause ☞ EOF")
                    children=list()
                    for k in range(6):
                        tree = tree_stack.pop()
                        if tree.name == 'select-query':
                            children += list(reversed(tree.children))
                        else:
                            children.append(tree)
                        state_stack.pop()
                    children.reverse()
                    tree_stack.append(ParseTree(name='select-query', children=children))
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='')" % (lookahead_typ, repr(lookahead)))
                
            case 36:
                # <StateItem compound_condition→condition ●AND condition> ☞ ) AND EOF GROUP OR
                # <StateItem compound_condition→condition ●OR condition> ☞ ) AND EOF GROUP OR
                # <StateItem where_clause→WHERE condition●> ☞ EOF GROUP
                if lookahead == 'AND':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='AND', data=lookahead))
                    state_stack.append(44)
                    continue
                if lookahead == 'OR':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='OR', data=lookahead))
                    state_stack.append(45)
                    continue
                if ( lookahead_typ.value == 'EOF'
                  or lookahead == 'GROUP'
                ):
                    print("▶ REDUCE : where_clause → WHERE condition ☞ EOF GROUP")
                    children=list()
                    for k in range(2):
                        tree = tree_stack.pop()
                        if tree.name == 'where_clause':
                            children += list(reversed(tree.children))
                        else:
                            children.append(tree)
                        state_stack.pop()
                    children.reverse()
                    tree_stack.append(ParseTree(name='where_clause', children=children))
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='AND OR')" % (lookahead_typ, repr(lookahead)))
                
            case 37:
                # <StateItem simple_comparison_condition→expr ●simple_comparison_operator expr> ☞ ) AND EOF GROUP OR
                # <StateItem@ simple_comparison_operator→●=> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●!=> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●^=> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●<>> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●>> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●<> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●>=> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●<=> ☞ IDT SMP SQL SUM
                if len(tree_stack) > 0 and tree_stack[-1].name == 'simple_comparison_operator':
                    print("▶ SHIFT : (simple_comparison_operator)")
                    if tree_stack[-1].name == 'simple_comparison_operator':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='simple_comparison_operator', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='simple_comparison_operator', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(46)
                    continue
                if lookahead == '=':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='=', data=lookahead))
                    state_stack.append(47)
                    continue
                if lookahead == '<':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='<', data=lookahead))
                    state_stack.append(48)
                    continue
                if lookahead == '<=':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='<=', data=lookahead))
                    state_stack.append(49)
                    continue
                if lookahead == '^=':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='^=', data=lookahead))
                    state_stack.append(50)
                    continue
                if lookahead == '<>':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='<>', data=lookahead))
                    state_stack.append(51)
                    continue
                if lookahead == '!=':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='!=', data=lookahead))
                    state_stack.append(52)
                    continue
                if lookahead == '>':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='>', data=lookahead))
                    state_stack.append(53)
                    continue
                if lookahead == '>=':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='>=', data=lookahead))
                    state_stack.append(54)
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='= < <= ^= <> != > >=')" % (lookahead_typ, repr(lookahead)))
                
            case 38:
                # <StateItem condition→compound_condition●> ☞ ) AND EOF GROUP OR
                if ( lookahead_typ.value == 'EOF'
                  or lookahead == ')'
                  or lookahead == 'AND'
                  or lookahead == 'GROUP'
                  or lookahead == 'OR'
                ):
                    print("▶ REDUCE : condition → compound_condition ☞ ) AND EOF GROUP OR")
                    children=list()
                    for k in range(1):
                        tree = tree_stack.pop()
                        if tree.name == 'condition':
                            children += list(reversed(tree.children))
                        else:
                            children.append(tree)
                        state_stack.pop()
                    children.reverse()
                    tree_stack.append(ParseTree(name='condition', children=children))
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='')" % (lookahead_typ, repr(lookahead)))
                
            case 39:
                # <StateItem condition→simple_comparison_condition●> ☞ ) AND EOF GROUP OR
                if ( lookahead_typ.value == 'EOF'
                  or lookahead == ')'
                  or lookahead == 'AND'
                  or lookahead == 'GROUP'
                  or lookahead == 'OR'
                ):
                    print("▶ REDUCE : condition → simple_comparison_condition ☞ ) AND EOF GROUP OR")
                    children=list()
                    for k in range(1):
                        tree = tree_stack.pop()
                        if tree.name == 'condition':
                            children += list(reversed(tree.children))
                        else:
                            children.append(tree)
                        state_stack.pop()
                    children.reverse()
                    tree_stack.append(ParseTree(name='condition', children=children))
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='')" % (lookahead_typ, repr(lookahead)))
                
            case 40:
                # <StateItem compound_condition→NOT ●condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ condition→●compound_condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ condition→●simple_comparison_condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●condition AND condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●condition OR condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●NOT condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●( condition )> ☞ ) AND EOF GROUP OR
                # <StateItem@ simple_comparison_condition→●expr simple_comparison_operator expr> ☞ ) AND EOF GROUP OR
                # <StateItem@ expr→●IDT . IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SQL> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SMP> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SUM ( expr )> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                if len(tree_stack) > 0 and tree_stack[-1].name == 'condition':
                    print("▶ SHIFT : (condition)")
                    if tree_stack[-1].name == 'condition':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='condition', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='condition', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(55)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'expr':
                    print("▶ SHIFT : (expr)")
                    if tree_stack[-1].name == 'expr':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='expr', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='expr', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(56)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'compound_condition':
                    print("▶ SHIFT : (compound_condition)")
                    if tree_stack[-1].name == 'compound_condition':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='compound_condition', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='compound_condition', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(38)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'simple_comparison_condition':
                    print("▶ SHIFT : (simple_comparison_condition)")
                    if tree_stack[-1].name == 'simple_comparison_condition':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='simple_comparison_condition', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='simple_comparison_condition', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(39)
                    continue
                if lookahead_typ.value == 'SMP':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SMP', data=lookahead))
                    state_stack.append(13)
                    continue
                if lookahead == 'NOT':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='NOT', data=lookahead))
                    state_stack.append(57)
                    continue
                if lookahead == 'SUM':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SUM', data=lookahead))
                    state_stack.append(14)
                    continue
                if lookahead_typ.value == 'SQL':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SQL', data=lookahead))
                    state_stack.append(16)
                    continue
                if lookahead == '(':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='(', data=lookahead))
                    state_stack.append(41)
                    continue
                if lookahead_typ.value == 'IDT':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='IDT', data=lookahead))
                    state_stack.append(15)
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='TokenType.sql_mapper_parameter NOT SUM TokenType.single_quoted_literal ( TokenType.identifier')" % (lookahead_typ, repr(lookahead)))
                
            case 41:
                # <StateItem compound_condition→( ●condition )> ☞ ) AND EOF GROUP OR
                # <StateItem@ condition→●compound_condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ condition→●simple_comparison_condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●condition AND condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●condition OR condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●NOT condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●( condition )> ☞ ) AND EOF GROUP OR
                # <StateItem@ simple_comparison_condition→●expr simple_comparison_operator expr> ☞ ) AND EOF GROUP OR
                # <StateItem@ expr→●IDT . IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SQL> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SMP> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SUM ( expr )> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                if len(tree_stack) > 0 and tree_stack[-1].name == 'condition':
                    print("▶ SHIFT : (condition)")
                    if tree_stack[-1].name == 'condition':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='condition', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='condition', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(58)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'expr':
                    print("▶ SHIFT : (expr)")
                    if tree_stack[-1].name == 'expr':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='expr', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='expr', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(56)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'compound_condition':
                    print("▶ SHIFT : (compound_condition)")
                    if tree_stack[-1].name == 'compound_condition':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='compound_condition', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='compound_condition', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(38)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'simple_comparison_condition':
                    print("▶ SHIFT : (simple_comparison_condition)")
                    if tree_stack[-1].name == 'simple_comparison_condition':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='simple_comparison_condition', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='simple_comparison_condition', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(39)
                    continue
                if lookahead_typ.value == 'SMP':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SMP', data=lookahead))
                    state_stack.append(13)
                    continue
                if lookahead == 'NOT':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='NOT', data=lookahead))
                    state_stack.append(57)
                    continue
                if lookahead == 'SUM':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SUM', data=lookahead))
                    state_stack.append(14)
                    continue
                if lookahead_typ.value == 'SQL':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SQL', data=lookahead))
                    state_stack.append(16)
                    continue
                if lookahead == '(':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='(', data=lookahead))
                    state_stack.append(59)
                    continue
                if lookahead_typ.value == 'IDT':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='IDT', data=lookahead))
                    state_stack.append(15)
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='TokenType.sql_mapper_parameter NOT SUM TokenType.single_quoted_literal ( TokenType.identifier')" % (lookahead_typ, repr(lookahead)))
                
            case 42:
                # <StateItem groupby_clause→GROUP BY ●groupby_clause_list> ☞ EOF
                # <StateItem@ groupby_clause_list→●expr> ☞ EOF
                # <StateItem@ groupby_clause_list→●expr , groupby_clause_list> ☞ EOF
                # <StateItem@ expr→●IDT . IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SQL> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SMP> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SUM ( expr )> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                if len(tree_stack) > 0 and tree_stack[-1].name == 'expr':
                    print("▶ SHIFT : (expr)")
                    if tree_stack[-1].name == 'expr':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='expr', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='expr', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(60)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'groupby_clause_list':
                    print("▶ SHIFT : (groupby_clause_list)")
                    if tree_stack[-1].name == 'groupby_clause_list':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='groupby_clause_list', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='groupby_clause_list', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(61)
                    continue
                if lookahead_typ.value == 'SMP':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SMP', data=lookahead))
                    state_stack.append(13)
                    continue
                if lookahead == 'SUM':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SUM', data=lookahead))
                    state_stack.append(14)
                    continue
                if lookahead_typ.value == 'IDT':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='IDT', data=lookahead))
                    state_stack.append(15)
                    continue
                if lookahead_typ.value == 'SQL':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SQL', data=lookahead))
                    state_stack.append(16)
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='TokenType.sql_mapper_parameter SUM TokenType.identifier TokenType.single_quoted_literal')" % (lookahead_typ, repr(lookahead)))
                
            case 43:
                # <StateItem sources→source , sources●> ☞ EOF GROUP WHERE
                if ( lookahead == 'WHERE'
                  or lookahead == 'GROUP'
                  or lookahead_typ.value == 'EOF'
                ):
                    print("▶ REDUCE : sources → source , sources ☞ EOF GROUP WHERE")
                    children=list()
                    for k in range(3):
                        tree = tree_stack.pop()
                        if tree.name == 'sources':
                            children += list(reversed(tree.children))
                        else:
                            children.append(tree)
                        state_stack.pop()
                    children.reverse()
                    tree_stack.append(ParseTree(name='sources', children=children))
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='')" % (lookahead_typ, repr(lookahead)))
                
            case 44:
                # <StateItem compound_condition→condition AND ●condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ condition→●compound_condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ condition→●simple_comparison_condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●condition AND condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●condition OR condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●NOT condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●( condition )> ☞ ) AND EOF GROUP OR
                # <StateItem@ simple_comparison_condition→●expr simple_comparison_operator expr> ☞ ) AND EOF GROUP OR
                # <StateItem@ expr→●IDT . IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SQL> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SMP> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SUM ( expr )> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                if len(tree_stack) > 0 and tree_stack[-1].name == 'condition':
                    print("▶ SHIFT : (condition)")
                    if tree_stack[-1].name == 'condition':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='condition', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='condition', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(62)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'expr':
                    print("▶ SHIFT : (expr)")
                    if tree_stack[-1].name == 'expr':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='expr', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='expr', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(56)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'compound_condition':
                    print("▶ SHIFT : (compound_condition)")
                    if tree_stack[-1].name == 'compound_condition':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='compound_condition', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='compound_condition', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(38)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'simple_comparison_condition':
                    print("▶ SHIFT : (simple_comparison_condition)")
                    if tree_stack[-1].name == 'simple_comparison_condition':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='simple_comparison_condition', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='simple_comparison_condition', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(39)
                    continue
                if lookahead_typ.value == 'SMP':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SMP', data=lookahead))
                    state_stack.append(13)
                    continue
                if lookahead == 'NOT':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='NOT', data=lookahead))
                    state_stack.append(57)
                    continue
                if lookahead == 'SUM':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SUM', data=lookahead))
                    state_stack.append(14)
                    continue
                if lookahead_typ.value == 'SQL':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SQL', data=lookahead))
                    state_stack.append(16)
                    continue
                if lookahead == '(':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='(', data=lookahead))
                    state_stack.append(59)
                    continue
                if lookahead_typ.value == 'IDT':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='IDT', data=lookahead))
                    state_stack.append(15)
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='TokenType.sql_mapper_parameter NOT SUM TokenType.single_quoted_literal ( TokenType.identifier')" % (lookahead_typ, repr(lookahead)))
                
            case 45:
                # <StateItem compound_condition→condition OR ●condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ condition→●compound_condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ condition→●simple_comparison_condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●condition AND condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●condition OR condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●NOT condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●( condition )> ☞ ) AND EOF GROUP OR
                # <StateItem@ simple_comparison_condition→●expr simple_comparison_operator expr> ☞ ) AND EOF GROUP OR
                # <StateItem@ expr→●IDT . IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SQL> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SMP> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SUM ( expr )> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                if len(tree_stack) > 0 and tree_stack[-1].name == 'condition':
                    print("▶ SHIFT : (condition)")
                    if tree_stack[-1].name == 'condition':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='condition', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='condition', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(63)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'expr':
                    print("▶ SHIFT : (expr)")
                    if tree_stack[-1].name == 'expr':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='expr', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='expr', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(56)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'compound_condition':
                    print("▶ SHIFT : (compound_condition)")
                    if tree_stack[-1].name == 'compound_condition':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='compound_condition', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='compound_condition', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(38)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'simple_comparison_condition':
                    print("▶ SHIFT : (simple_comparison_condition)")
                    if tree_stack[-1].name == 'simple_comparison_condition':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='simple_comparison_condition', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='simple_comparison_condition', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(39)
                    continue
                if lookahead_typ.value == 'SMP':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SMP', data=lookahead))
                    state_stack.append(13)
                    continue
                if lookahead == 'NOT':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='NOT', data=lookahead))
                    state_stack.append(57)
                    continue
                if lookahead == 'SUM':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SUM', data=lookahead))
                    state_stack.append(14)
                    continue
                if lookahead_typ.value == 'SQL':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SQL', data=lookahead))
                    state_stack.append(16)
                    continue
                if lookahead == '(':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='(', data=lookahead))
                    state_stack.append(59)
                    continue
                if lookahead_typ.value == 'IDT':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='IDT', data=lookahead))
                    state_stack.append(15)
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='TokenType.sql_mapper_parameter NOT SUM TokenType.single_quoted_literal ( TokenType.identifier')" % (lookahead_typ, repr(lookahead)))
                
            case 46:
                # <StateItem simple_comparison_condition→expr simple_comparison_operator ●expr> ☞ ) AND EOF GROUP OR
                # <StateItem@ expr→●IDT . IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SQL> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SMP> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SUM ( expr )> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                if len(tree_stack) > 0 and tree_stack[-1].name == 'expr':
                    print("▶ SHIFT : (expr)")
                    if tree_stack[-1].name == 'expr':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='expr', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='expr', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(64)
                    continue
                if lookahead_typ.value == 'SMP':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SMP', data=lookahead))
                    state_stack.append(13)
                    continue
                if lookahead == 'SUM':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SUM', data=lookahead))
                    state_stack.append(14)
                    continue
                if lookahead_typ.value == 'IDT':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='IDT', data=lookahead))
                    state_stack.append(15)
                    continue
                if lookahead_typ.value == 'SQL':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SQL', data=lookahead))
                    state_stack.append(16)
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='TokenType.sql_mapper_parameter SUM TokenType.identifier TokenType.single_quoted_literal')" % (lookahead_typ, repr(lookahead)))
                
            case 47:
                # <StateItem simple_comparison_operator→=●> ☞ IDT SMP SQL SUM
                if ( lookahead_typ.value == 'SMP'
                  or lookahead == 'SUM'
                  or lookahead_typ.value == 'IDT'
                  or lookahead_typ.value == 'SQL'
                ):
                    print("▶ REDUCE : simple_comparison_operator → = ☞ IDT SMP SQL SUM")
                    children=list()
                    for k in range(1):
                        tree = tree_stack.pop()
                        if tree.name == 'simple_comparison_operator':
                            children += list(reversed(tree.children))
                        else:
                            children.append(tree)
                        state_stack.pop()
                    children.reverse()
                    tree_stack.append(ParseTree(name='simple_comparison_operator', children=children))
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='')" % (lookahead_typ, repr(lookahead)))
                
            case 48:
                # <StateItem simple_comparison_operator→<●> ☞ IDT SMP SQL SUM
                if ( lookahead_typ.value == 'SMP'
                  or lookahead == 'SUM'
                  or lookahead_typ.value == 'IDT'
                  or lookahead_typ.value == 'SQL'
                ):
                    print("▶ REDUCE : simple_comparison_operator → < ☞ IDT SMP SQL SUM")
                    children=list()
                    for k in range(1):
                        tree = tree_stack.pop()
                        if tree.name == 'simple_comparison_operator':
                            children += list(reversed(tree.children))
                        else:
                            children.append(tree)
                        state_stack.pop()
                    children.reverse()
                    tree_stack.append(ParseTree(name='simple_comparison_operator', children=children))
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='')" % (lookahead_typ, repr(lookahead)))
                
            case 49:
                # <StateItem simple_comparison_operator→<=●> ☞ IDT SMP SQL SUM
                if ( lookahead_typ.value == 'SMP'
                  or lookahead == 'SUM'
                  or lookahead_typ.value == 'IDT'
                  or lookahead_typ.value == 'SQL'
                ):
                    print("▶ REDUCE : simple_comparison_operator → <= ☞ IDT SMP SQL SUM")
                    children=list()
                    for k in range(1):
                        tree = tree_stack.pop()
                        if tree.name == 'simple_comparison_operator':
                            children += list(reversed(tree.children))
                        else:
                            children.append(tree)
                        state_stack.pop()
                    children.reverse()
                    tree_stack.append(ParseTree(name='simple_comparison_operator', children=children))
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='')" % (lookahead_typ, repr(lookahead)))
                
            case 50:
                # <StateItem simple_comparison_operator→^=●> ☞ IDT SMP SQL SUM
                if ( lookahead_typ.value == 'SMP'
                  or lookahead == 'SUM'
                  or lookahead_typ.value == 'IDT'
                  or lookahead_typ.value == 'SQL'
                ):
                    print("▶ REDUCE : simple_comparison_operator → ^= ☞ IDT SMP SQL SUM")
                    children=list()
                    for k in range(1):
                        tree = tree_stack.pop()
                        if tree.name == 'simple_comparison_operator':
                            children += list(reversed(tree.children))
                        else:
                            children.append(tree)
                        state_stack.pop()
                    children.reverse()
                    tree_stack.append(ParseTree(name='simple_comparison_operator', children=children))
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='')" % (lookahead_typ, repr(lookahead)))
                
            case 51:
                # <StateItem simple_comparison_operator→<>●> ☞ IDT SMP SQL SUM
                if ( lookahead_typ.value == 'SMP'
                  or lookahead == 'SUM'
                  or lookahead_typ.value == 'IDT'
                  or lookahead_typ.value == 'SQL'
                ):
                    print("▶ REDUCE : simple_comparison_operator → <> ☞ IDT SMP SQL SUM")
                    children=list()
                    for k in range(1):
                        tree = tree_stack.pop()
                        if tree.name == 'simple_comparison_operator':
                            children += list(reversed(tree.children))
                        else:
                            children.append(tree)
                        state_stack.pop()
                    children.reverse()
                    tree_stack.append(ParseTree(name='simple_comparison_operator', children=children))
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='')" % (lookahead_typ, repr(lookahead)))
                
            case 52:
                # <StateItem simple_comparison_operator→!=●> ☞ IDT SMP SQL SUM
                if ( lookahead_typ.value == 'SMP'
                  or lookahead == 'SUM'
                  or lookahead_typ.value == 'IDT'
                  or lookahead_typ.value == 'SQL'
                ):
                    print("▶ REDUCE : simple_comparison_operator → != ☞ IDT SMP SQL SUM")
                    children=list()
                    for k in range(1):
                        tree = tree_stack.pop()
                        if tree.name == 'simple_comparison_operator':
                            children += list(reversed(tree.children))
                        else:
                            children.append(tree)
                        state_stack.pop()
                    children.reverse()
                    tree_stack.append(ParseTree(name='simple_comparison_operator', children=children))
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='')" % (lookahead_typ, repr(lookahead)))
                
            case 53:
                # <StateItem simple_comparison_operator→>●> ☞ IDT SMP SQL SUM
                if ( lookahead_typ.value == 'SMP'
                  or lookahead == 'SUM'
                  or lookahead_typ.value == 'IDT'
                  or lookahead_typ.value == 'SQL'
                ):
                    print("▶ REDUCE : simple_comparison_operator → > ☞ IDT SMP SQL SUM")
                    children=list()
                    for k in range(1):
                        tree = tree_stack.pop()
                        if tree.name == 'simple_comparison_operator':
                            children += list(reversed(tree.children))
                        else:
                            children.append(tree)
                        state_stack.pop()
                    children.reverse()
                    tree_stack.append(ParseTree(name='simple_comparison_operator', children=children))
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='')" % (lookahead_typ, repr(lookahead)))
                
            case 54:
                # <StateItem simple_comparison_operator→>=●> ☞ IDT SMP SQL SUM
                if ( lookahead_typ.value == 'SMP'
                  or lookahead == 'SUM'
                  or lookahead_typ.value == 'IDT'
                  or lookahead_typ.value == 'SQL'
                ):
                    print("▶ REDUCE : simple_comparison_operator → >= ☞ IDT SMP SQL SUM")
                    children=list()
                    for k in range(1):
                        tree = tree_stack.pop()
                        if tree.name == 'simple_comparison_operator':
                            children += list(reversed(tree.children))
                        else:
                            children.append(tree)
                        state_stack.pop()
                    children.reverse()
                    tree_stack.append(ParseTree(name='simple_comparison_operator', children=children))
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='')" % (lookahead_typ, repr(lookahead)))
                
            case 55:
                # <StateItem compound_condition→NOT condition●> ☞ ) AND EOF GROUP OR
                # <StateItem compound_condition→condition ●AND condition> ☞ ) AND EOF GROUP OR
                # <StateItem compound_condition→condition ●OR condition> ☞ ) AND EOF GROUP OR
                if lookahead == 'AND':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='AND', data=lookahead))
                    state_stack.append(65)
                    continue
                if lookahead == 'OR':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='OR', data=lookahead))
                    state_stack.append(66)
                    continue
                if ( lookahead_typ.value == 'EOF'
                  or lookahead == ')'
                  or lookahead == 'AND'
                  or lookahead == 'GROUP'
                  or lookahead == 'OR'
                ):
                    print("▶ REDUCE : compound_condition → NOT condition ☞ ) AND EOF GROUP OR")
                    children=list()
                    for k in range(2):
                        tree = tree_stack.pop()
                        if tree.name == 'compound_condition':
                            children += list(reversed(tree.children))
                        else:
                            children.append(tree)
                        state_stack.pop()
                    children.reverse()
                    tree_stack.append(ParseTree(name='compound_condition', children=children))
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='AND OR')" % (lookahead_typ, repr(lookahead)))
                
            case 56:
                # <StateItem simple_comparison_condition→expr ●simple_comparison_operator expr> ☞ ) AND EOF GROUP OR
                # <StateItem@ simple_comparison_operator→●=> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●!=> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●^=> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●<>> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●>> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●<> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●>=> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●<=> ☞ IDT SMP SQL SUM
                if len(tree_stack) > 0 and tree_stack[-1].name == 'simple_comparison_operator':
                    print("▶ SHIFT : (simple_comparison_operator)")
                    if tree_stack[-1].name == 'simple_comparison_operator':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='simple_comparison_operator', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='simple_comparison_operator', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(67)
                    continue
                if lookahead == '=':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='=', data=lookahead))
                    state_stack.append(47)
                    continue
                if lookahead == '<':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='<', data=lookahead))
                    state_stack.append(48)
                    continue
                if lookahead == '<=':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='<=', data=lookahead))
                    state_stack.append(49)
                    continue
                if lookahead == '^=':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='^=', data=lookahead))
                    state_stack.append(50)
                    continue
                if lookahead == '<>':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='<>', data=lookahead))
                    state_stack.append(51)
                    continue
                if lookahead == '!=':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='!=', data=lookahead))
                    state_stack.append(52)
                    continue
                if lookahead == '>':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='>', data=lookahead))
                    state_stack.append(53)
                    continue
                if lookahead == '>=':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='>=', data=lookahead))
                    state_stack.append(54)
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='= < <= ^= <> != > >=')" % (lookahead_typ, repr(lookahead)))
                
            case 57:
                # <StateItem compound_condition→NOT ●condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ condition→●compound_condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ condition→●simple_comparison_condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●condition AND condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●condition OR condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●NOT condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●( condition )> ☞ ) AND EOF GROUP OR
                # <StateItem@ simple_comparison_condition→●expr simple_comparison_operator expr> ☞ ) AND EOF GROUP OR
                # <StateItem@ expr→●IDT . IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SQL> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SMP> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SUM ( expr )> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                if len(tree_stack) > 0 and tree_stack[-1].name == 'condition':
                    print("▶ SHIFT : (condition)")
                    if tree_stack[-1].name == 'condition':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='condition', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='condition', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(55)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'expr':
                    print("▶ SHIFT : (expr)")
                    if tree_stack[-1].name == 'expr':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='expr', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='expr', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(68)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'compound_condition':
                    print("▶ SHIFT : (compound_condition)")
                    if tree_stack[-1].name == 'compound_condition':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='compound_condition', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='compound_condition', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(38)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'simple_comparison_condition':
                    print("▶ SHIFT : (simple_comparison_condition)")
                    if tree_stack[-1].name == 'simple_comparison_condition':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='simple_comparison_condition', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='simple_comparison_condition', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(39)
                    continue
                if lookahead_typ.value == 'SMP':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SMP', data=lookahead))
                    state_stack.append(13)
                    continue
                if lookahead == 'NOT':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='NOT', data=lookahead))
                    state_stack.append(69)
                    continue
                if lookahead == 'SUM':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SUM', data=lookahead))
                    state_stack.append(14)
                    continue
                if lookahead_typ.value == 'SQL':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SQL', data=lookahead))
                    state_stack.append(16)
                    continue
                if lookahead == '(':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='(', data=lookahead))
                    state_stack.append(59)
                    continue
                if lookahead_typ.value == 'IDT':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='IDT', data=lookahead))
                    state_stack.append(15)
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='TokenType.sql_mapper_parameter NOT SUM TokenType.single_quoted_literal ( TokenType.identifier')" % (lookahead_typ, repr(lookahead)))
                
            case 58:
                # <StateItem compound_condition→( condition ●)> ☞ ) AND EOF GROUP OR
                # <StateItem compound_condition→condition ●AND condition> ☞ ) AND EOF GROUP OR
                # <StateItem compound_condition→condition ●OR condition> ☞ ) AND EOF GROUP OR
                if lookahead == 'AND':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='AND', data=lookahead))
                    state_stack.append(65)
                    continue
                if lookahead == 'OR':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='OR', data=lookahead))
                    state_stack.append(66)
                    continue
                if lookahead == ')':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name=')', data=lookahead))
                    state_stack.append(70)
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='AND OR )')" % (lookahead_typ, repr(lookahead)))
                
            case 59:
                # <StateItem compound_condition→( ●condition )> ☞ ) AND EOF GROUP OR
                # <StateItem@ condition→●compound_condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ condition→●simple_comparison_condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●condition AND condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●condition OR condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●NOT condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●( condition )> ☞ ) AND EOF GROUP OR
                # <StateItem@ simple_comparison_condition→●expr simple_comparison_operator expr> ☞ ) AND EOF GROUP OR
                # <StateItem@ expr→●IDT . IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SQL> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SMP> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SUM ( expr )> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                if len(tree_stack) > 0 and tree_stack[-1].name == 'condition':
                    print("▶ SHIFT : (condition)")
                    if tree_stack[-1].name == 'condition':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='condition', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='condition', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(58)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'expr':
                    print("▶ SHIFT : (expr)")
                    if tree_stack[-1].name == 'expr':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='expr', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='expr', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(68)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'compound_condition':
                    print("▶ SHIFT : (compound_condition)")
                    if tree_stack[-1].name == 'compound_condition':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='compound_condition', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='compound_condition', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(38)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'simple_comparison_condition':
                    print("▶ SHIFT : (simple_comparison_condition)")
                    if tree_stack[-1].name == 'simple_comparison_condition':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='simple_comparison_condition', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='simple_comparison_condition', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(39)
                    continue
                if lookahead_typ.value == 'SMP':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SMP', data=lookahead))
                    state_stack.append(13)
                    continue
                if lookahead == 'NOT':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='NOT', data=lookahead))
                    state_stack.append(69)
                    continue
                if lookahead == 'SUM':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SUM', data=lookahead))
                    state_stack.append(14)
                    continue
                if lookahead_typ.value == 'SQL':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SQL', data=lookahead))
                    state_stack.append(16)
                    continue
                if lookahead == '(':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='(', data=lookahead))
                    state_stack.append(71)
                    continue
                if lookahead_typ.value == 'IDT':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='IDT', data=lookahead))
                    state_stack.append(15)
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='TokenType.sql_mapper_parameter NOT SUM TokenType.single_quoted_literal ( TokenType.identifier')" % (lookahead_typ, repr(lookahead)))
                
            case 60:
                # <StateItem groupby_clause_list→expr ●, groupby_clause_list> ☞ EOF
                # <StateItem groupby_clause_list→expr●> ☞ EOF
                if lookahead == ',':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name=',', data=lookahead))
                    state_stack.append(72)
                    continue
                if lookahead_typ.value == 'EOF':
                    print("▶ REDUCE : groupby_clause_list → expr ☞ EOF")
                    children=list()
                    for k in range(1):
                        tree = tree_stack.pop()
                        if tree.name == 'groupby_clause_list':
                            children += list(reversed(tree.children))
                        else:
                            children.append(tree)
                        state_stack.pop()
                    children.reverse()
                    tree_stack.append(ParseTree(name='groupby_clause_list', children=children))
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected=',')" % (lookahead_typ, repr(lookahead)))
                
            case 61:
                # <StateItem groupby_clause→GROUP BY groupby_clause_list●> ☞ EOF
                if lookahead_typ.value == 'EOF':
                    print("▶ REDUCE : groupby_clause → GROUP BY groupby_clause_list ☞ EOF")
                    children=list()
                    for k in range(3):
                        tree = tree_stack.pop()
                        if tree.name == 'groupby_clause':
                            children += list(reversed(tree.children))
                        else:
                            children.append(tree)
                        state_stack.pop()
                    children.reverse()
                    tree_stack.append(ParseTree(name='groupby_clause', children=children))
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='')" % (lookahead_typ, repr(lookahead)))
                
            case 62:
                # <StateItem compound_condition→condition AND condition●> ☞ ) AND EOF GROUP OR
                # <StateItem compound_condition→condition ●AND condition> ☞ ) AND EOF GROUP OR
                # <StateItem compound_condition→condition ●OR condition> ☞ ) AND EOF GROUP OR
                if lookahead == 'AND':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='AND', data=lookahead))
                    state_stack.append(65)
                    continue
                if lookahead == 'OR':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='OR', data=lookahead))
                    state_stack.append(66)
                    continue
                if ( lookahead_typ.value == 'EOF'
                  or lookahead == ')'
                  or lookahead == 'AND'
                  or lookahead == 'GROUP'
                  or lookahead == 'OR'
                ):
                    print("▶ REDUCE : compound_condition → condition AND condition ☞ ) AND EOF GROUP OR")
                    children=list()
                    for k in range(3):
                        tree = tree_stack.pop()
                        if tree.name == 'compound_condition':
                            children += list(reversed(tree.children))
                        else:
                            children.append(tree)
                        state_stack.pop()
                    children.reverse()
                    tree_stack.append(ParseTree(name='compound_condition', children=children))
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='AND OR')" % (lookahead_typ, repr(lookahead)))
                
            case 63:
                # <StateItem compound_condition→condition OR condition●> ☞ ) AND EOF GROUP OR
                # <StateItem compound_condition→condition ●AND condition> ☞ ) AND EOF GROUP OR
                # <StateItem compound_condition→condition ●OR condition> ☞ ) AND EOF GROUP OR
                if lookahead == 'AND':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='AND', data=lookahead))
                    state_stack.append(65)
                    continue
                if lookahead == 'OR':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='OR', data=lookahead))
                    state_stack.append(66)
                    continue
                if ( lookahead_typ.value == 'EOF'
                  or lookahead == ')'
                  or lookahead == 'AND'
                  or lookahead == 'GROUP'
                  or lookahead == 'OR'
                ):
                    print("▶ REDUCE : compound_condition → condition OR condition ☞ ) AND EOF GROUP OR")
                    children=list()
                    for k in range(3):
                        tree = tree_stack.pop()
                        if tree.name == 'compound_condition':
                            children += list(reversed(tree.children))
                        else:
                            children.append(tree)
                        state_stack.pop()
                    children.reverse()
                    tree_stack.append(ParseTree(name='compound_condition', children=children))
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='AND OR')" % (lookahead_typ, repr(lookahead)))
                
            case 64:
                # <StateItem simple_comparison_condition→expr simple_comparison_operator expr●> ☞ ) AND EOF GROUP OR
                if ( lookahead_typ.value == 'EOF'
                  or lookahead == ')'
                  or lookahead == 'AND'
                  or lookahead == 'GROUP'
                  or lookahead == 'OR'
                ):
                    print("▶ REDUCE : simple_comparison_condition → expr simple_comparison_operator expr ☞ ) AND EOF GROUP OR")
                    children=list()
                    for k in range(3):
                        tree = tree_stack.pop()
                        if tree.name == 'simple_comparison_condition':
                            children += list(reversed(tree.children))
                        else:
                            children.append(tree)
                        state_stack.pop()
                    children.reverse()
                    tree_stack.append(ParseTree(name='simple_comparison_condition', children=children))
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='')" % (lookahead_typ, repr(lookahead)))
                
            case 65:
                # <StateItem compound_condition→condition AND ●condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ condition→●compound_condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ condition→●simple_comparison_condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●condition AND condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●condition OR condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●NOT condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●( condition )> ☞ ) AND EOF GROUP OR
                # <StateItem@ simple_comparison_condition→●expr simple_comparison_operator expr> ☞ ) AND EOF GROUP OR
                # <StateItem@ expr→●IDT . IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SQL> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SMP> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SUM ( expr )> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                if len(tree_stack) > 0 and tree_stack[-1].name == 'condition':
                    print("▶ SHIFT : (condition)")
                    if tree_stack[-1].name == 'condition':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='condition', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='condition', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(62)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'expr':
                    print("▶ SHIFT : (expr)")
                    if tree_stack[-1].name == 'expr':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='expr', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='expr', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(68)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'compound_condition':
                    print("▶ SHIFT : (compound_condition)")
                    if tree_stack[-1].name == 'compound_condition':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='compound_condition', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='compound_condition', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(38)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'simple_comparison_condition':
                    print("▶ SHIFT : (simple_comparison_condition)")
                    if tree_stack[-1].name == 'simple_comparison_condition':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='simple_comparison_condition', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='simple_comparison_condition', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(39)
                    continue
                if lookahead_typ.value == 'SMP':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SMP', data=lookahead))
                    state_stack.append(13)
                    continue
                if lookahead == 'NOT':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='NOT', data=lookahead))
                    state_stack.append(69)
                    continue
                if lookahead == 'SUM':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SUM', data=lookahead))
                    state_stack.append(14)
                    continue
                if lookahead_typ.value == 'SQL':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SQL', data=lookahead))
                    state_stack.append(16)
                    continue
                if lookahead == '(':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='(', data=lookahead))
                    state_stack.append(71)
                    continue
                if lookahead_typ.value == 'IDT':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='IDT', data=lookahead))
                    state_stack.append(15)
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='TokenType.sql_mapper_parameter NOT SUM TokenType.single_quoted_literal ( TokenType.identifier')" % (lookahead_typ, repr(lookahead)))
                
            case 66:
                # <StateItem compound_condition→condition OR ●condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ condition→●compound_condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ condition→●simple_comparison_condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●condition AND condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●condition OR condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●NOT condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●( condition )> ☞ ) AND EOF GROUP OR
                # <StateItem@ simple_comparison_condition→●expr simple_comparison_operator expr> ☞ ) AND EOF GROUP OR
                # <StateItem@ expr→●IDT . IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SQL> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SMP> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SUM ( expr )> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                if len(tree_stack) > 0 and tree_stack[-1].name == 'condition':
                    print("▶ SHIFT : (condition)")
                    if tree_stack[-1].name == 'condition':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='condition', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='condition', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(63)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'expr':
                    print("▶ SHIFT : (expr)")
                    if tree_stack[-1].name == 'expr':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='expr', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='expr', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(68)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'compound_condition':
                    print("▶ SHIFT : (compound_condition)")
                    if tree_stack[-1].name == 'compound_condition':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='compound_condition', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='compound_condition', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(38)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'simple_comparison_condition':
                    print("▶ SHIFT : (simple_comparison_condition)")
                    if tree_stack[-1].name == 'simple_comparison_condition':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='simple_comparison_condition', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='simple_comparison_condition', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(39)
                    continue
                if lookahead_typ.value == 'SMP':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SMP', data=lookahead))
                    state_stack.append(13)
                    continue
                if lookahead == 'NOT':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='NOT', data=lookahead))
                    state_stack.append(69)
                    continue
                if lookahead == 'SUM':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SUM', data=lookahead))
                    state_stack.append(14)
                    continue
                if lookahead_typ.value == 'SQL':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SQL', data=lookahead))
                    state_stack.append(16)
                    continue
                if lookahead == '(':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='(', data=lookahead))
                    state_stack.append(71)
                    continue
                if lookahead_typ.value == 'IDT':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='IDT', data=lookahead))
                    state_stack.append(15)
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='TokenType.sql_mapper_parameter NOT SUM TokenType.single_quoted_literal ( TokenType.identifier')" % (lookahead_typ, repr(lookahead)))
                
            case 67:
                # <StateItem simple_comparison_condition→expr simple_comparison_operator ●expr> ☞ ) AND EOF GROUP OR
                # <StateItem@ expr→●IDT . IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SQL> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SMP> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SUM ( expr )> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                if len(tree_stack) > 0 and tree_stack[-1].name == 'expr':
                    print("▶ SHIFT : (expr)")
                    if tree_stack[-1].name == 'expr':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='expr', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='expr', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(64)
                    continue
                if lookahead_typ.value == 'SMP':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SMP', data=lookahead))
                    state_stack.append(13)
                    continue
                if lookahead == 'SUM':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SUM', data=lookahead))
                    state_stack.append(14)
                    continue
                if lookahead_typ.value == 'IDT':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='IDT', data=lookahead))
                    state_stack.append(15)
                    continue
                if lookahead_typ.value == 'SQL':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SQL', data=lookahead))
                    state_stack.append(16)
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='TokenType.sql_mapper_parameter SUM TokenType.identifier TokenType.single_quoted_literal')" % (lookahead_typ, repr(lookahead)))
                
            case 68:
                # <StateItem simple_comparison_condition→expr ●simple_comparison_operator expr> ☞ ) AND EOF GROUP OR
                # <StateItem@ simple_comparison_operator→●=> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●!=> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●^=> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●<>> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●>> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●<> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●>=> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●<=> ☞ IDT SMP SQL SUM
                if len(tree_stack) > 0 and tree_stack[-1].name == 'simple_comparison_operator':
                    print("▶ SHIFT : (simple_comparison_operator)")
                    if tree_stack[-1].name == 'simple_comparison_operator':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='simple_comparison_operator', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='simple_comparison_operator', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(73)
                    continue
                if lookahead == '=':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='=', data=lookahead))
                    state_stack.append(47)
                    continue
                if lookahead == '<':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='<', data=lookahead))
                    state_stack.append(48)
                    continue
                if lookahead == '<=':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='<=', data=lookahead))
                    state_stack.append(49)
                    continue
                if lookahead == '^=':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='^=', data=lookahead))
                    state_stack.append(50)
                    continue
                if lookahead == '<>':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='<>', data=lookahead))
                    state_stack.append(51)
                    continue
                if lookahead == '!=':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='!=', data=lookahead))
                    state_stack.append(52)
                    continue
                if lookahead == '>':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='>', data=lookahead))
                    state_stack.append(53)
                    continue
                if lookahead == '>=':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='>=', data=lookahead))
                    state_stack.append(54)
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='= < <= ^= <> != > >=')" % (lookahead_typ, repr(lookahead)))
                
            case 69:
                # <StateItem compound_condition→NOT ●condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ condition→●compound_condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ condition→●simple_comparison_condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●condition AND condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●condition OR condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●NOT condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●( condition )> ☞ ) AND EOF GROUP OR
                # <StateItem@ simple_comparison_condition→●expr simple_comparison_operator expr> ☞ ) AND EOF GROUP OR
                # <StateItem@ expr→●IDT . IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SQL> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SMP> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SUM ( expr )> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                if len(tree_stack) > 0 and tree_stack[-1].name == 'condition':
                    print("▶ SHIFT : (condition)")
                    if tree_stack[-1].name == 'condition':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='condition', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='condition', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(55)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'expr':
                    print("▶ SHIFT : (expr)")
                    if tree_stack[-1].name == 'expr':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='expr', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='expr', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(74)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'compound_condition':
                    print("▶ SHIFT : (compound_condition)")
                    if tree_stack[-1].name == 'compound_condition':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='compound_condition', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='compound_condition', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(38)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'simple_comparison_condition':
                    print("▶ SHIFT : (simple_comparison_condition)")
                    if tree_stack[-1].name == 'simple_comparison_condition':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='simple_comparison_condition', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='simple_comparison_condition', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(39)
                    continue
                if lookahead_typ.value == 'SMP':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SMP', data=lookahead))
                    state_stack.append(13)
                    continue
                if lookahead == 'NOT':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='NOT', data=lookahead))
                    state_stack.append(75)
                    continue
                if lookahead == 'SUM':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SUM', data=lookahead))
                    state_stack.append(14)
                    continue
                if lookahead_typ.value == 'SQL':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SQL', data=lookahead))
                    state_stack.append(16)
                    continue
                if lookahead == '(':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='(', data=lookahead))
                    state_stack.append(71)
                    continue
                if lookahead_typ.value == 'IDT':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='IDT', data=lookahead))
                    state_stack.append(15)
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='TokenType.sql_mapper_parameter NOT SUM TokenType.single_quoted_literal ( TokenType.identifier')" % (lookahead_typ, repr(lookahead)))
                
            case 70:
                # <StateItem compound_condition→( condition )●> ☞ ) AND EOF GROUP OR
                if ( lookahead_typ.value == 'EOF'
                  or lookahead == ')'
                  or lookahead == 'AND'
                  or lookahead == 'GROUP'
                  or lookahead == 'OR'
                ):
                    print("▶ REDUCE : compound_condition → ( condition ) ☞ ) AND EOF GROUP OR")
                    children=list()
                    for k in range(3):
                        tree = tree_stack.pop()
                        if tree.name == 'compound_condition':
                            children += list(reversed(tree.children))
                        else:
                            children.append(tree)
                        state_stack.pop()
                    children.reverse()
                    tree_stack.append(ParseTree(name='compound_condition', children=children))
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='')" % (lookahead_typ, repr(lookahead)))
                
            case 71:
                # <StateItem compound_condition→( ●condition )> ☞ ) AND EOF GROUP OR
                # <StateItem@ condition→●compound_condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ condition→●simple_comparison_condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●condition AND condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●condition OR condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●NOT condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●( condition )> ☞ ) AND EOF GROUP OR
                # <StateItem@ simple_comparison_condition→●expr simple_comparison_operator expr> ☞ ) AND EOF GROUP OR
                # <StateItem@ expr→●IDT . IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SQL> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SMP> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SUM ( expr )> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                if len(tree_stack) > 0 and tree_stack[-1].name == 'condition':
                    print("▶ SHIFT : (condition)")
                    if tree_stack[-1].name == 'condition':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='condition', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='condition', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(58)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'expr':
                    print("▶ SHIFT : (expr)")
                    if tree_stack[-1].name == 'expr':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='expr', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='expr', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(74)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'compound_condition':
                    print("▶ SHIFT : (compound_condition)")
                    if tree_stack[-1].name == 'compound_condition':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='compound_condition', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='compound_condition', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(38)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'simple_comparison_condition':
                    print("▶ SHIFT : (simple_comparison_condition)")
                    if tree_stack[-1].name == 'simple_comparison_condition':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='simple_comparison_condition', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='simple_comparison_condition', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(39)
                    continue
                if lookahead_typ.value == 'SMP':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SMP', data=lookahead))
                    state_stack.append(13)
                    continue
                if lookahead == 'NOT':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='NOT', data=lookahead))
                    state_stack.append(75)
                    continue
                if lookahead == 'SUM':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SUM', data=lookahead))
                    state_stack.append(14)
                    continue
                if lookahead_typ.value == 'SQL':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SQL', data=lookahead))
                    state_stack.append(16)
                    continue
                if lookahead == '(':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='(', data=lookahead))
                    state_stack.append(76)
                    continue
                if lookahead_typ.value == 'IDT':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='IDT', data=lookahead))
                    state_stack.append(15)
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='TokenType.sql_mapper_parameter NOT SUM TokenType.single_quoted_literal ( TokenType.identifier')" % (lookahead_typ, repr(lookahead)))
                
            case 72:
                # <StateItem groupby_clause_list→expr , ●groupby_clause_list> ☞ EOF
                # <StateItem@ groupby_clause_list→●expr> ☞ EOF
                # <StateItem@ groupby_clause_list→●expr , groupby_clause_list> ☞ EOF
                # <StateItem@ expr→●IDT . IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SQL> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SMP> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SUM ( expr )> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                if len(tree_stack) > 0 and tree_stack[-1].name == 'expr':
                    print("▶ SHIFT : (expr)")
                    if tree_stack[-1].name == 'expr':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='expr', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='expr', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(60)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'groupby_clause_list':
                    print("▶ SHIFT : (groupby_clause_list)")
                    if tree_stack[-1].name == 'groupby_clause_list':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='groupby_clause_list', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='groupby_clause_list', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(77)
                    continue
                if lookahead_typ.value == 'SMP':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SMP', data=lookahead))
                    state_stack.append(13)
                    continue
                if lookahead == 'SUM':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SUM', data=lookahead))
                    state_stack.append(14)
                    continue
                if lookahead_typ.value == 'IDT':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='IDT', data=lookahead))
                    state_stack.append(15)
                    continue
                if lookahead_typ.value == 'SQL':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SQL', data=lookahead))
                    state_stack.append(16)
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='TokenType.sql_mapper_parameter SUM TokenType.identifier TokenType.single_quoted_literal')" % (lookahead_typ, repr(lookahead)))
                
            case 73:
                # <StateItem simple_comparison_condition→expr simple_comparison_operator ●expr> ☞ ) AND EOF GROUP OR
                # <StateItem@ expr→●IDT . IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SQL> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SMP> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SUM ( expr )> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                if len(tree_stack) > 0 and tree_stack[-1].name == 'expr':
                    print("▶ SHIFT : (expr)")
                    if tree_stack[-1].name == 'expr':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='expr', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='expr', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(64)
                    continue
                if lookahead_typ.value == 'SMP':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SMP', data=lookahead))
                    state_stack.append(13)
                    continue
                if lookahead == 'SUM':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SUM', data=lookahead))
                    state_stack.append(14)
                    continue
                if lookahead_typ.value == 'IDT':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='IDT', data=lookahead))
                    state_stack.append(15)
                    continue
                if lookahead_typ.value == 'SQL':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SQL', data=lookahead))
                    state_stack.append(16)
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='TokenType.sql_mapper_parameter SUM TokenType.identifier TokenType.single_quoted_literal')" % (lookahead_typ, repr(lookahead)))
                
            case 74:
                # <StateItem simple_comparison_condition→expr ●simple_comparison_operator expr> ☞ ) AND EOF GROUP OR
                # <StateItem@ simple_comparison_operator→●=> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●!=> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●^=> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●<>> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●>> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●<> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●>=> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●<=> ☞ IDT SMP SQL SUM
                if len(tree_stack) > 0 and tree_stack[-1].name == 'simple_comparison_operator':
                    print("▶ SHIFT : (simple_comparison_operator)")
                    if tree_stack[-1].name == 'simple_comparison_operator':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='simple_comparison_operator', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='simple_comparison_operator', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(78)
                    continue
                if lookahead == '=':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='=', data=lookahead))
                    state_stack.append(47)
                    continue
                if lookahead == '<':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='<', data=lookahead))
                    state_stack.append(48)
                    continue
                if lookahead == '<=':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='<=', data=lookahead))
                    state_stack.append(49)
                    continue
                if lookahead == '^=':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='^=', data=lookahead))
                    state_stack.append(50)
                    continue
                if lookahead == '<>':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='<>', data=lookahead))
                    state_stack.append(51)
                    continue
                if lookahead == '!=':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='!=', data=lookahead))
                    state_stack.append(52)
                    continue
                if lookahead == '>':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='>', data=lookahead))
                    state_stack.append(53)
                    continue
                if lookahead == '>=':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='>=', data=lookahead))
                    state_stack.append(54)
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='= < <= ^= <> != > >=')" % (lookahead_typ, repr(lookahead)))
                
            case 75:
                # <StateItem compound_condition→NOT ●condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ condition→●compound_condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ condition→●simple_comparison_condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●condition AND condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●condition OR condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●NOT condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●( condition )> ☞ ) AND EOF GROUP OR
                # <StateItem@ simple_comparison_condition→●expr simple_comparison_operator expr> ☞ ) AND EOF GROUP OR
                # <StateItem@ expr→●IDT . IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SQL> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SMP> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SUM ( expr )> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                if len(tree_stack) > 0 and tree_stack[-1].name == 'condition':
                    print("▶ SHIFT : (condition)")
                    if tree_stack[-1].name == 'condition':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='condition', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='condition', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(55)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'expr':
                    print("▶ SHIFT : (expr)")
                    if tree_stack[-1].name == 'expr':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='expr', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='expr', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(79)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'compound_condition':
                    print("▶ SHIFT : (compound_condition)")
                    if tree_stack[-1].name == 'compound_condition':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='compound_condition', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='compound_condition', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(38)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'simple_comparison_condition':
                    print("▶ SHIFT : (simple_comparison_condition)")
                    if tree_stack[-1].name == 'simple_comparison_condition':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='simple_comparison_condition', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='simple_comparison_condition', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(39)
                    continue
                if lookahead_typ.value == 'SMP':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SMP', data=lookahead))
                    state_stack.append(13)
                    continue
                if lookahead == 'NOT':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='NOT', data=lookahead))
                    state_stack.append(80)
                    continue
                if lookahead == 'SUM':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SUM', data=lookahead))
                    state_stack.append(14)
                    continue
                if lookahead_typ.value == 'SQL':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SQL', data=lookahead))
                    state_stack.append(16)
                    continue
                if lookahead == '(':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='(', data=lookahead))
                    state_stack.append(76)
                    continue
                if lookahead_typ.value == 'IDT':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='IDT', data=lookahead))
                    state_stack.append(15)
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='TokenType.sql_mapper_parameter NOT SUM TokenType.single_quoted_literal ( TokenType.identifier')" % (lookahead_typ, repr(lookahead)))
                
            case 76:
                # <StateItem compound_condition→( ●condition )> ☞ ) AND EOF GROUP OR
                # <StateItem@ condition→●compound_condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ condition→●simple_comparison_condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●condition AND condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●condition OR condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●NOT condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●( condition )> ☞ ) AND EOF GROUP OR
                # <StateItem@ simple_comparison_condition→●expr simple_comparison_operator expr> ☞ ) AND EOF GROUP OR
                # <StateItem@ expr→●IDT . IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SQL> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SMP> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SUM ( expr )> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                if len(tree_stack) > 0 and tree_stack[-1].name == 'condition':
                    print("▶ SHIFT : (condition)")
                    if tree_stack[-1].name == 'condition':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='condition', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='condition', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(58)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'expr':
                    print("▶ SHIFT : (expr)")
                    if tree_stack[-1].name == 'expr':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='expr', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='expr', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(79)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'compound_condition':
                    print("▶ SHIFT : (compound_condition)")
                    if tree_stack[-1].name == 'compound_condition':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='compound_condition', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='compound_condition', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(38)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'simple_comparison_condition':
                    print("▶ SHIFT : (simple_comparison_condition)")
                    if tree_stack[-1].name == 'simple_comparison_condition':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='simple_comparison_condition', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='simple_comparison_condition', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(39)
                    continue
                if lookahead_typ.value == 'SMP':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SMP', data=lookahead))
                    state_stack.append(13)
                    continue
                if lookahead == 'NOT':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='NOT', data=lookahead))
                    state_stack.append(80)
                    continue
                if lookahead == 'SUM':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SUM', data=lookahead))
                    state_stack.append(14)
                    continue
                if lookahead_typ.value == 'SQL':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SQL', data=lookahead))
                    state_stack.append(16)
                    continue
                if lookahead == '(':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='(', data=lookahead))
                    state_stack.append(81)
                    continue
                if lookahead_typ.value == 'IDT':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='IDT', data=lookahead))
                    state_stack.append(15)
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='TokenType.sql_mapper_parameter NOT SUM TokenType.single_quoted_literal ( TokenType.identifier')" % (lookahead_typ, repr(lookahead)))
                
            case 77:
                # <StateItem groupby_clause_list→expr , groupby_clause_list●> ☞ EOF
                if lookahead_typ.value == 'EOF':
                    print("▶ REDUCE : groupby_clause_list → expr , groupby_clause_list ☞ EOF")
                    children=list()
                    for k in range(3):
                        tree = tree_stack.pop()
                        if tree.name == 'groupby_clause_list':
                            children += list(reversed(tree.children))
                        else:
                            children.append(tree)
                        state_stack.pop()
                    children.reverse()
                    tree_stack.append(ParseTree(name='groupby_clause_list', children=children))
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='')" % (lookahead_typ, repr(lookahead)))
                
            case 78:
                # <StateItem simple_comparison_condition→expr simple_comparison_operator ●expr> ☞ ) AND EOF GROUP OR
                # <StateItem@ expr→●IDT . IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SQL> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SMP> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SUM ( expr )> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                if len(tree_stack) > 0 and tree_stack[-1].name == 'expr':
                    print("▶ SHIFT : (expr)")
                    if tree_stack[-1].name == 'expr':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='expr', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='expr', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(64)
                    continue
                if lookahead_typ.value == 'SMP':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SMP', data=lookahead))
                    state_stack.append(13)
                    continue
                if lookahead == 'SUM':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SUM', data=lookahead))
                    state_stack.append(14)
                    continue
                if lookahead_typ.value == 'IDT':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='IDT', data=lookahead))
                    state_stack.append(15)
                    continue
                if lookahead_typ.value == 'SQL':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SQL', data=lookahead))
                    state_stack.append(16)
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='TokenType.sql_mapper_parameter SUM TokenType.identifier TokenType.single_quoted_literal')" % (lookahead_typ, repr(lookahead)))
                
            case 79:
                # <StateItem simple_comparison_condition→expr ●simple_comparison_operator expr> ☞ ) AND EOF GROUP OR
                # <StateItem@ simple_comparison_operator→●=> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●!=> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●^=> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●<>> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●>> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●<> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●>=> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●<=> ☞ IDT SMP SQL SUM
                if len(tree_stack) > 0 and tree_stack[-1].name == 'simple_comparison_operator':
                    print("▶ SHIFT : (simple_comparison_operator)")
                    if tree_stack[-1].name == 'simple_comparison_operator':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='simple_comparison_operator', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='simple_comparison_operator', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(82)
                    continue
                if lookahead == '=':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='=', data=lookahead))
                    state_stack.append(47)
                    continue
                if lookahead == '<':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='<', data=lookahead))
                    state_stack.append(48)
                    continue
                if lookahead == '<=':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='<=', data=lookahead))
                    state_stack.append(49)
                    continue
                if lookahead == '^=':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='^=', data=lookahead))
                    state_stack.append(50)
                    continue
                if lookahead == '<>':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='<>', data=lookahead))
                    state_stack.append(51)
                    continue
                if lookahead == '!=':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='!=', data=lookahead))
                    state_stack.append(52)
                    continue
                if lookahead == '>':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='>', data=lookahead))
                    state_stack.append(53)
                    continue
                if lookahead == '>=':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='>=', data=lookahead))
                    state_stack.append(54)
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='= < <= ^= <> != > >=')" % (lookahead_typ, repr(lookahead)))
                
            case 80:
                # <StateItem compound_condition→NOT ●condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ condition→●compound_condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ condition→●simple_comparison_condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●condition AND condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●condition OR condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●NOT condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●( condition )> ☞ ) AND EOF GROUP OR
                # <StateItem@ simple_comparison_condition→●expr simple_comparison_operator expr> ☞ ) AND EOF GROUP OR
                # <StateItem@ expr→●IDT . IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SQL> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SMP> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SUM ( expr )> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                if len(tree_stack) > 0 and tree_stack[-1].name == 'condition':
                    print("▶ SHIFT : (condition)")
                    if tree_stack[-1].name == 'condition':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='condition', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='condition', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(55)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'expr':
                    print("▶ SHIFT : (expr)")
                    if tree_stack[-1].name == 'expr':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='expr', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='expr', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(83)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'compound_condition':
                    print("▶ SHIFT : (compound_condition)")
                    if tree_stack[-1].name == 'compound_condition':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='compound_condition', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='compound_condition', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(38)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'simple_comparison_condition':
                    print("▶ SHIFT : (simple_comparison_condition)")
                    if tree_stack[-1].name == 'simple_comparison_condition':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='simple_comparison_condition', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='simple_comparison_condition', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(39)
                    continue
                if lookahead_typ.value == 'SMP':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SMP', data=lookahead))
                    state_stack.append(13)
                    continue
                if lookahead == 'NOT':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='NOT', data=lookahead))
                    state_stack.append(84)
                    continue
                if lookahead == 'SUM':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SUM', data=lookahead))
                    state_stack.append(14)
                    continue
                if lookahead_typ.value == 'SQL':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SQL', data=lookahead))
                    state_stack.append(16)
                    continue
                if lookahead == '(':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='(', data=lookahead))
                    state_stack.append(81)
                    continue
                if lookahead_typ.value == 'IDT':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='IDT', data=lookahead))
                    state_stack.append(15)
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='TokenType.sql_mapper_parameter NOT SUM TokenType.single_quoted_literal ( TokenType.identifier')" % (lookahead_typ, repr(lookahead)))
                
            case 81:
                # <StateItem compound_condition→( ●condition )> ☞ ) AND EOF GROUP OR
                # <StateItem@ condition→●compound_condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ condition→●simple_comparison_condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●condition AND condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●condition OR condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●NOT condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●( condition )> ☞ ) AND EOF GROUP OR
                # <StateItem@ simple_comparison_condition→●expr simple_comparison_operator expr> ☞ ) AND EOF GROUP OR
                # <StateItem@ expr→●IDT . IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SQL> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SMP> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SUM ( expr )> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                if len(tree_stack) > 0 and tree_stack[-1].name == 'condition':
                    print("▶ SHIFT : (condition)")
                    if tree_stack[-1].name == 'condition':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='condition', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='condition', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(58)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'expr':
                    print("▶ SHIFT : (expr)")
                    if tree_stack[-1].name == 'expr':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='expr', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='expr', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(83)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'compound_condition':
                    print("▶ SHIFT : (compound_condition)")
                    if tree_stack[-1].name == 'compound_condition':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='compound_condition', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='compound_condition', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(38)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'simple_comparison_condition':
                    print("▶ SHIFT : (simple_comparison_condition)")
                    if tree_stack[-1].name == 'simple_comparison_condition':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='simple_comparison_condition', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='simple_comparison_condition', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(39)
                    continue
                if lookahead_typ.value == 'SMP':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SMP', data=lookahead))
                    state_stack.append(13)
                    continue
                if lookahead == 'NOT':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='NOT', data=lookahead))
                    state_stack.append(84)
                    continue
                if lookahead == 'SUM':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SUM', data=lookahead))
                    state_stack.append(14)
                    continue
                if lookahead_typ.value == 'SQL':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SQL', data=lookahead))
                    state_stack.append(16)
                    continue
                if lookahead == '(':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='(', data=lookahead))
                    state_stack.append(85)
                    continue
                if lookahead_typ.value == 'IDT':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='IDT', data=lookahead))
                    state_stack.append(15)
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='TokenType.sql_mapper_parameter NOT SUM TokenType.single_quoted_literal ( TokenType.identifier')" % (lookahead_typ, repr(lookahead)))
                
            case 82:
                # <StateItem simple_comparison_condition→expr simple_comparison_operator ●expr> ☞ ) AND EOF GROUP OR
                # <StateItem@ expr→●IDT . IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SQL> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SMP> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SUM ( expr )> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                if len(tree_stack) > 0 and tree_stack[-1].name == 'expr':
                    print("▶ SHIFT : (expr)")
                    if tree_stack[-1].name == 'expr':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='expr', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='expr', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(64)
                    continue
                if lookahead_typ.value == 'SMP':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SMP', data=lookahead))
                    state_stack.append(13)
                    continue
                if lookahead == 'SUM':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SUM', data=lookahead))
                    state_stack.append(14)
                    continue
                if lookahead_typ.value == 'IDT':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='IDT', data=lookahead))
                    state_stack.append(15)
                    continue
                if lookahead_typ.value == 'SQL':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SQL', data=lookahead))
                    state_stack.append(16)
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='TokenType.sql_mapper_parameter SUM TokenType.identifier TokenType.single_quoted_literal')" % (lookahead_typ, repr(lookahead)))
                
            case 83:
                # <StateItem simple_comparison_condition→expr ●simple_comparison_operator expr> ☞ ) AND EOF GROUP OR
                # <StateItem@ simple_comparison_operator→●=> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●!=> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●^=> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●<>> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●>> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●<> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●>=> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●<=> ☞ IDT SMP SQL SUM
                if len(tree_stack) > 0 and tree_stack[-1].name == 'simple_comparison_operator':
                    print("▶ SHIFT : (simple_comparison_operator)")
                    if tree_stack[-1].name == 'simple_comparison_operator':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='simple_comparison_operator', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='simple_comparison_operator', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(86)
                    continue
                if lookahead == '=':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='=', data=lookahead))
                    state_stack.append(47)
                    continue
                if lookahead == '<':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='<', data=lookahead))
                    state_stack.append(48)
                    continue
                if lookahead == '<=':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='<=', data=lookahead))
                    state_stack.append(49)
                    continue
                if lookahead == '^=':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='^=', data=lookahead))
                    state_stack.append(50)
                    continue
                if lookahead == '<>':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='<>', data=lookahead))
                    state_stack.append(51)
                    continue
                if lookahead == '!=':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='!=', data=lookahead))
                    state_stack.append(52)
                    continue
                if lookahead == '>':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='>', data=lookahead))
                    state_stack.append(53)
                    continue
                if lookahead == '>=':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='>=', data=lookahead))
                    state_stack.append(54)
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='= < <= ^= <> != > >=')" % (lookahead_typ, repr(lookahead)))
                
            case 84:
                # <StateItem compound_condition→NOT ●condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ condition→●compound_condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ condition→●simple_comparison_condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●condition AND condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●condition OR condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●NOT condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●( condition )> ☞ ) AND EOF GROUP OR
                # <StateItem@ simple_comparison_condition→●expr simple_comparison_operator expr> ☞ ) AND EOF GROUP OR
                # <StateItem@ expr→●IDT . IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SQL> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SMP> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SUM ( expr )> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                if len(tree_stack) > 0 and tree_stack[-1].name == 'condition':
                    print("▶ SHIFT : (condition)")
                    if tree_stack[-1].name == 'condition':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='condition', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='condition', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(55)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'expr':
                    print("▶ SHIFT : (expr)")
                    if tree_stack[-1].name == 'expr':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='expr', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='expr', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(87)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'compound_condition':
                    print("▶ SHIFT : (compound_condition)")
                    if tree_stack[-1].name == 'compound_condition':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='compound_condition', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='compound_condition', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(38)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'simple_comparison_condition':
                    print("▶ SHIFT : (simple_comparison_condition)")
                    if tree_stack[-1].name == 'simple_comparison_condition':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='simple_comparison_condition', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='simple_comparison_condition', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(39)
                    continue
                if lookahead_typ.value == 'SMP':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SMP', data=lookahead))
                    state_stack.append(13)
                    continue
                if lookahead == 'NOT':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='NOT', data=lookahead))
                    state_stack.append(88)
                    continue
                if lookahead == 'SUM':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SUM', data=lookahead))
                    state_stack.append(14)
                    continue
                if lookahead_typ.value == 'SQL':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SQL', data=lookahead))
                    state_stack.append(16)
                    continue
                if lookahead == '(':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='(', data=lookahead))
                    state_stack.append(85)
                    continue
                if lookahead_typ.value == 'IDT':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='IDT', data=lookahead))
                    state_stack.append(15)
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='TokenType.sql_mapper_parameter NOT SUM TokenType.single_quoted_literal ( TokenType.identifier')" % (lookahead_typ, repr(lookahead)))
                
            case 85:
                # <StateItem compound_condition→( ●condition )> ☞ ) AND EOF GROUP OR
                # <StateItem@ condition→●compound_condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ condition→●simple_comparison_condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●condition AND condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●condition OR condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●NOT condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●( condition )> ☞ ) AND EOF GROUP OR
                # <StateItem@ simple_comparison_condition→●expr simple_comparison_operator expr> ☞ ) AND EOF GROUP OR
                # <StateItem@ expr→●IDT . IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SQL> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SMP> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SUM ( expr )> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                if len(tree_stack) > 0 and tree_stack[-1].name == 'condition':
                    print("▶ SHIFT : (condition)")
                    if tree_stack[-1].name == 'condition':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='condition', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='condition', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(58)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'expr':
                    print("▶ SHIFT : (expr)")
                    if tree_stack[-1].name == 'expr':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='expr', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='expr', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(87)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'compound_condition':
                    print("▶ SHIFT : (compound_condition)")
                    if tree_stack[-1].name == 'compound_condition':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='compound_condition', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='compound_condition', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(38)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'simple_comparison_condition':
                    print("▶ SHIFT : (simple_comparison_condition)")
                    if tree_stack[-1].name == 'simple_comparison_condition':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='simple_comparison_condition', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='simple_comparison_condition', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(39)
                    continue
                if lookahead_typ.value == 'SMP':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SMP', data=lookahead))
                    state_stack.append(13)
                    continue
                if lookahead == 'NOT':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='NOT', data=lookahead))
                    state_stack.append(88)
                    continue
                if lookahead == 'SUM':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SUM', data=lookahead))
                    state_stack.append(14)
                    continue
                if lookahead_typ.value == 'SQL':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SQL', data=lookahead))
                    state_stack.append(16)
                    continue
                if lookahead == '(':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='(', data=lookahead))
                    state_stack.append(89)
                    continue
                if lookahead_typ.value == 'IDT':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='IDT', data=lookahead))
                    state_stack.append(15)
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='TokenType.sql_mapper_parameter NOT SUM TokenType.single_quoted_literal ( TokenType.identifier')" % (lookahead_typ, repr(lookahead)))
                
            case 86:
                # <StateItem simple_comparison_condition→expr simple_comparison_operator ●expr> ☞ ) AND EOF GROUP OR
                # <StateItem@ expr→●IDT . IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SQL> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SMP> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SUM ( expr )> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                if len(tree_stack) > 0 and tree_stack[-1].name == 'expr':
                    print("▶ SHIFT : (expr)")
                    if tree_stack[-1].name == 'expr':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='expr', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='expr', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(64)
                    continue
                if lookahead_typ.value == 'SMP':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SMP', data=lookahead))
                    state_stack.append(13)
                    continue
                if lookahead == 'SUM':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SUM', data=lookahead))
                    state_stack.append(14)
                    continue
                if lookahead_typ.value == 'IDT':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='IDT', data=lookahead))
                    state_stack.append(15)
                    continue
                if lookahead_typ.value == 'SQL':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SQL', data=lookahead))
                    state_stack.append(16)
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='TokenType.sql_mapper_parameter SUM TokenType.identifier TokenType.single_quoted_literal')" % (lookahead_typ, repr(lookahead)))
                
            case 87:
                # <StateItem simple_comparison_condition→expr ●simple_comparison_operator expr> ☞ ) AND EOF GROUP OR
                # <StateItem@ simple_comparison_operator→●=> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●!=> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●^=> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●<>> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●>> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●<> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●>=> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●<=> ☞ IDT SMP SQL SUM
                if len(tree_stack) > 0 and tree_stack[-1].name == 'simple_comparison_operator':
                    print("▶ SHIFT : (simple_comparison_operator)")
                    if tree_stack[-1].name == 'simple_comparison_operator':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='simple_comparison_operator', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='simple_comparison_operator', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(90)
                    continue
                if lookahead == '=':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='=', data=lookahead))
                    state_stack.append(47)
                    continue
                if lookahead == '<':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='<', data=lookahead))
                    state_stack.append(48)
                    continue
                if lookahead == '<=':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='<=', data=lookahead))
                    state_stack.append(49)
                    continue
                if lookahead == '^=':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='^=', data=lookahead))
                    state_stack.append(50)
                    continue
                if lookahead == '<>':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='<>', data=lookahead))
                    state_stack.append(51)
                    continue
                if lookahead == '!=':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='!=', data=lookahead))
                    state_stack.append(52)
                    continue
                if lookahead == '>':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='>', data=lookahead))
                    state_stack.append(53)
                    continue
                if lookahead == '>=':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='>=', data=lookahead))
                    state_stack.append(54)
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='= < <= ^= <> != > >=')" % (lookahead_typ, repr(lookahead)))
                
            case 88:
                # <StateItem compound_condition→NOT ●condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ condition→●compound_condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ condition→●simple_comparison_condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●condition AND condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●condition OR condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●NOT condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●( condition )> ☞ ) AND EOF GROUP OR
                # <StateItem@ simple_comparison_condition→●expr simple_comparison_operator expr> ☞ ) AND EOF GROUP OR
                # <StateItem@ expr→●IDT . IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SQL> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SMP> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SUM ( expr )> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                if len(tree_stack) > 0 and tree_stack[-1].name == 'condition':
                    print("▶ SHIFT : (condition)")
                    if tree_stack[-1].name == 'condition':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='condition', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='condition', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(55)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'expr':
                    print("▶ SHIFT : (expr)")
                    if tree_stack[-1].name == 'expr':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='expr', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='expr', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(91)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'compound_condition':
                    print("▶ SHIFT : (compound_condition)")
                    if tree_stack[-1].name == 'compound_condition':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='compound_condition', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='compound_condition', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(38)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'simple_comparison_condition':
                    print("▶ SHIFT : (simple_comparison_condition)")
                    if tree_stack[-1].name == 'simple_comparison_condition':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='simple_comparison_condition', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='simple_comparison_condition', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(39)
                    continue
                if lookahead_typ.value == 'SMP':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SMP', data=lookahead))
                    state_stack.append(13)
                    continue
                if lookahead == 'NOT':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='NOT', data=lookahead))
                    state_stack.append(92)
                    continue
                if lookahead == 'SUM':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SUM', data=lookahead))
                    state_stack.append(14)
                    continue
                if lookahead_typ.value == 'SQL':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SQL', data=lookahead))
                    state_stack.append(16)
                    continue
                if lookahead == '(':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='(', data=lookahead))
                    state_stack.append(89)
                    continue
                if lookahead_typ.value == 'IDT':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='IDT', data=lookahead))
                    state_stack.append(15)
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='TokenType.sql_mapper_parameter NOT SUM TokenType.single_quoted_literal ( TokenType.identifier')" % (lookahead_typ, repr(lookahead)))
                
            case 89:
                # <StateItem compound_condition→( ●condition )> ☞ ) AND EOF GROUP OR
                # <StateItem@ condition→●compound_condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ condition→●simple_comparison_condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●condition AND condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●condition OR condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●NOT condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●( condition )> ☞ ) AND EOF GROUP OR
                # <StateItem@ simple_comparison_condition→●expr simple_comparison_operator expr> ☞ ) AND EOF GROUP OR
                # <StateItem@ expr→●IDT . IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SQL> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SMP> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SUM ( expr )> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                if len(tree_stack) > 0 and tree_stack[-1].name == 'condition':
                    print("▶ SHIFT : (condition)")
                    if tree_stack[-1].name == 'condition':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='condition', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='condition', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(58)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'expr':
                    print("▶ SHIFT : (expr)")
                    if tree_stack[-1].name == 'expr':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='expr', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='expr', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(91)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'compound_condition':
                    print("▶ SHIFT : (compound_condition)")
                    if tree_stack[-1].name == 'compound_condition':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='compound_condition', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='compound_condition', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(38)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'simple_comparison_condition':
                    print("▶ SHIFT : (simple_comparison_condition)")
                    if tree_stack[-1].name == 'simple_comparison_condition':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='simple_comparison_condition', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='simple_comparison_condition', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(39)
                    continue
                if lookahead_typ.value == 'SMP':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SMP', data=lookahead))
                    state_stack.append(13)
                    continue
                if lookahead == 'NOT':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='NOT', data=lookahead))
                    state_stack.append(92)
                    continue
                if lookahead == 'SUM':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SUM', data=lookahead))
                    state_stack.append(14)
                    continue
                if lookahead_typ.value == 'SQL':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SQL', data=lookahead))
                    state_stack.append(16)
                    continue
                if lookahead == '(':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='(', data=lookahead))
                    state_stack.append(93)
                    continue
                if lookahead_typ.value == 'IDT':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='IDT', data=lookahead))
                    state_stack.append(15)
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='TokenType.sql_mapper_parameter NOT SUM TokenType.single_quoted_literal ( TokenType.identifier')" % (lookahead_typ, repr(lookahead)))
                
            case 90:
                # <StateItem simple_comparison_condition→expr simple_comparison_operator ●expr> ☞ ) AND EOF GROUP OR
                # <StateItem@ expr→●IDT . IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SQL> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SMP> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SUM ( expr )> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                if len(tree_stack) > 0 and tree_stack[-1].name == 'expr':
                    print("▶ SHIFT : (expr)")
                    if tree_stack[-1].name == 'expr':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='expr', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='expr', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(64)
                    continue
                if lookahead_typ.value == 'SMP':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SMP', data=lookahead))
                    state_stack.append(13)
                    continue
                if lookahead == 'SUM':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SUM', data=lookahead))
                    state_stack.append(14)
                    continue
                if lookahead_typ.value == 'IDT':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='IDT', data=lookahead))
                    state_stack.append(15)
                    continue
                if lookahead_typ.value == 'SQL':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SQL', data=lookahead))
                    state_stack.append(16)
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='TokenType.sql_mapper_parameter SUM TokenType.identifier TokenType.single_quoted_literal')" % (lookahead_typ, repr(lookahead)))
                
            case 91:
                # <StateItem simple_comparison_condition→expr ●simple_comparison_operator expr> ☞ ) AND EOF GROUP OR
                # <StateItem@ simple_comparison_operator→●=> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●!=> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●^=> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●<>> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●>> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●<> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●>=> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●<=> ☞ IDT SMP SQL SUM
                if len(tree_stack) > 0 and tree_stack[-1].name == 'simple_comparison_operator':
                    print("▶ SHIFT : (simple_comparison_operator)")
                    if tree_stack[-1].name == 'simple_comparison_operator':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='simple_comparison_operator', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='simple_comparison_operator', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(94)
                    continue
                if lookahead == '=':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='=', data=lookahead))
                    state_stack.append(47)
                    continue
                if lookahead == '<':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='<', data=lookahead))
                    state_stack.append(48)
                    continue
                if lookahead == '<=':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='<=', data=lookahead))
                    state_stack.append(49)
                    continue
                if lookahead == '^=':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='^=', data=lookahead))
                    state_stack.append(50)
                    continue
                if lookahead == '<>':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='<>', data=lookahead))
                    state_stack.append(51)
                    continue
                if lookahead == '!=':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='!=', data=lookahead))
                    state_stack.append(52)
                    continue
                if lookahead == '>':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='>', data=lookahead))
                    state_stack.append(53)
                    continue
                if lookahead == '>=':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='>=', data=lookahead))
                    state_stack.append(54)
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='= < <= ^= <> != > >=')" % (lookahead_typ, repr(lookahead)))
                
            case 92:
                # <StateItem compound_condition→NOT ●condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ condition→●compound_condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ condition→●simple_comparison_condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●condition AND condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●condition OR condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●NOT condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●( condition )> ☞ ) AND EOF GROUP OR
                # <StateItem@ simple_comparison_condition→●expr simple_comparison_operator expr> ☞ ) AND EOF GROUP OR
                # <StateItem@ expr→●IDT . IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SQL> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SMP> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SUM ( expr )> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                if len(tree_stack) > 0 and tree_stack[-1].name == 'condition':
                    print("▶ SHIFT : (condition)")
                    if tree_stack[-1].name == 'condition':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='condition', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='condition', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(55)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'expr':
                    print("▶ SHIFT : (expr)")
                    if tree_stack[-1].name == 'expr':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='expr', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='expr', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(95)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'compound_condition':
                    print("▶ SHIFT : (compound_condition)")
                    if tree_stack[-1].name == 'compound_condition':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='compound_condition', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='compound_condition', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(38)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'simple_comparison_condition':
                    print("▶ SHIFT : (simple_comparison_condition)")
                    if tree_stack[-1].name == 'simple_comparison_condition':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='simple_comparison_condition', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='simple_comparison_condition', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(39)
                    continue
                if lookahead_typ.value == 'SMP':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SMP', data=lookahead))
                    state_stack.append(13)
                    continue
                if lookahead == 'NOT':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='NOT', data=lookahead))
                    state_stack.append(96)
                    continue
                if lookahead == 'SUM':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SUM', data=lookahead))
                    state_stack.append(14)
                    continue
                if lookahead_typ.value == 'SQL':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SQL', data=lookahead))
                    state_stack.append(16)
                    continue
                if lookahead == '(':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='(', data=lookahead))
                    state_stack.append(93)
                    continue
                if lookahead_typ.value == 'IDT':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='IDT', data=lookahead))
                    state_stack.append(15)
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='TokenType.sql_mapper_parameter NOT SUM TokenType.single_quoted_literal ( TokenType.identifier')" % (lookahead_typ, repr(lookahead)))
                
            case 93:
                # <StateItem compound_condition→( ●condition )> ☞ ) AND EOF GROUP OR
                # <StateItem@ condition→●compound_condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ condition→●simple_comparison_condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●condition AND condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●condition OR condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●NOT condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●( condition )> ☞ ) AND EOF GROUP OR
                # <StateItem@ simple_comparison_condition→●expr simple_comparison_operator expr> ☞ ) AND EOF GROUP OR
                # <StateItem@ expr→●IDT . IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SQL> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SMP> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SUM ( expr )> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                if len(tree_stack) > 0 and tree_stack[-1].name == 'condition':
                    print("▶ SHIFT : (condition)")
                    if tree_stack[-1].name == 'condition':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='condition', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='condition', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(58)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'expr':
                    print("▶ SHIFT : (expr)")
                    if tree_stack[-1].name == 'expr':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='expr', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='expr', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(95)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'compound_condition':
                    print("▶ SHIFT : (compound_condition)")
                    if tree_stack[-1].name == 'compound_condition':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='compound_condition', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='compound_condition', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(38)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'simple_comparison_condition':
                    print("▶ SHIFT : (simple_comparison_condition)")
                    if tree_stack[-1].name == 'simple_comparison_condition':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='simple_comparison_condition', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='simple_comparison_condition', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(39)
                    continue
                if lookahead_typ.value == 'SMP':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SMP', data=lookahead))
                    state_stack.append(13)
                    continue
                if lookahead == 'NOT':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='NOT', data=lookahead))
                    state_stack.append(96)
                    continue
                if lookahead == 'SUM':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SUM', data=lookahead))
                    state_stack.append(14)
                    continue
                if lookahead_typ.value == 'SQL':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SQL', data=lookahead))
                    state_stack.append(16)
                    continue
                if lookahead == '(':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='(', data=lookahead))
                    state_stack.append(97)
                    continue
                if lookahead_typ.value == 'IDT':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='IDT', data=lookahead))
                    state_stack.append(15)
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='TokenType.sql_mapper_parameter NOT SUM TokenType.single_quoted_literal ( TokenType.identifier')" % (lookahead_typ, repr(lookahead)))
                
            case 94:
                # <StateItem simple_comparison_condition→expr simple_comparison_operator ●expr> ☞ ) AND EOF GROUP OR
                # <StateItem@ expr→●IDT . IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SQL> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SMP> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SUM ( expr )> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                if len(tree_stack) > 0 and tree_stack[-1].name == 'expr':
                    print("▶ SHIFT : (expr)")
                    if tree_stack[-1].name == 'expr':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='expr', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='expr', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(64)
                    continue
                if lookahead_typ.value == 'SMP':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SMP', data=lookahead))
                    state_stack.append(13)
                    continue
                if lookahead == 'SUM':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SUM', data=lookahead))
                    state_stack.append(14)
                    continue
                if lookahead_typ.value == 'IDT':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='IDT', data=lookahead))
                    state_stack.append(15)
                    continue
                if lookahead_typ.value == 'SQL':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SQL', data=lookahead))
                    state_stack.append(16)
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='TokenType.sql_mapper_parameter SUM TokenType.identifier TokenType.single_quoted_literal')" % (lookahead_typ, repr(lookahead)))
                
            case 95:
                # <StateItem simple_comparison_condition→expr ●simple_comparison_operator expr> ☞ ) AND EOF GROUP OR
                # <StateItem@ simple_comparison_operator→●=> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●!=> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●^=> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●<>> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●>> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●<> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●>=> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●<=> ☞ IDT SMP SQL SUM
                if len(tree_stack) > 0 and tree_stack[-1].name == 'simple_comparison_operator':
                    print("▶ SHIFT : (simple_comparison_operator)")
                    if tree_stack[-1].name == 'simple_comparison_operator':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='simple_comparison_operator', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='simple_comparison_operator', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(98)
                    continue
                if lookahead == '=':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='=', data=lookahead))
                    state_stack.append(47)
                    continue
                if lookahead == '<':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='<', data=lookahead))
                    state_stack.append(48)
                    continue
                if lookahead == '<=':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='<=', data=lookahead))
                    state_stack.append(49)
                    continue
                if lookahead == '^=':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='^=', data=lookahead))
                    state_stack.append(50)
                    continue
                if lookahead == '<>':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='<>', data=lookahead))
                    state_stack.append(51)
                    continue
                if lookahead == '!=':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='!=', data=lookahead))
                    state_stack.append(52)
                    continue
                if lookahead == '>':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='>', data=lookahead))
                    state_stack.append(53)
                    continue
                if lookahead == '>=':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='>=', data=lookahead))
                    state_stack.append(54)
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='= < <= ^= <> != > >=')" % (lookahead_typ, repr(lookahead)))
                
            case 96:
                # <StateItem compound_condition→NOT ●condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ condition→●compound_condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ condition→●simple_comparison_condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●condition AND condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●condition OR condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●NOT condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●( condition )> ☞ ) AND EOF GROUP OR
                # <StateItem@ simple_comparison_condition→●expr simple_comparison_operator expr> ☞ ) AND EOF GROUP OR
                # <StateItem@ expr→●IDT . IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SQL> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SMP> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SUM ( expr )> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                if len(tree_stack) > 0 and tree_stack[-1].name == 'condition':
                    print("▶ SHIFT : (condition)")
                    if tree_stack[-1].name == 'condition':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='condition', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='condition', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(55)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'expr':
                    print("▶ SHIFT : (expr)")
                    if tree_stack[-1].name == 'expr':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='expr', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='expr', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(99)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'compound_condition':
                    print("▶ SHIFT : (compound_condition)")
                    if tree_stack[-1].name == 'compound_condition':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='compound_condition', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='compound_condition', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(38)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'simple_comparison_condition':
                    print("▶ SHIFT : (simple_comparison_condition)")
                    if tree_stack[-1].name == 'simple_comparison_condition':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='simple_comparison_condition', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='simple_comparison_condition', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(39)
                    continue
                if lookahead_typ.value == 'SMP':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SMP', data=lookahead))
                    state_stack.append(13)
                    continue
                if lookahead == 'NOT':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='NOT', data=lookahead))
                    state_stack.append(100)
                    continue
                if lookahead == 'SUM':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SUM', data=lookahead))
                    state_stack.append(14)
                    continue
                if lookahead_typ.value == 'SQL':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SQL', data=lookahead))
                    state_stack.append(16)
                    continue
                if lookahead == '(':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='(', data=lookahead))
                    state_stack.append(97)
                    continue
                if lookahead_typ.value == 'IDT':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='IDT', data=lookahead))
                    state_stack.append(15)
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='TokenType.sql_mapper_parameter NOT SUM TokenType.single_quoted_literal ( TokenType.identifier')" % (lookahead_typ, repr(lookahead)))
                
            case 97:
                # <StateItem compound_condition→( ●condition )> ☞ ) AND EOF GROUP OR
                # <StateItem@ condition→●compound_condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ condition→●simple_comparison_condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●condition AND condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●condition OR condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●NOT condition> ☞ ) AND EOF GROUP OR
                # <StateItem@ compound_condition→●( condition )> ☞ ) AND EOF GROUP OR
                # <StateItem@ simple_comparison_condition→●expr simple_comparison_operator expr> ☞ ) AND EOF GROUP OR
                # <StateItem@ expr→●IDT . IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SQL> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SMP> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SUM ( expr )> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                if len(tree_stack) > 0 and tree_stack[-1].name == 'condition':
                    print("▶ SHIFT : (condition)")
                    if tree_stack[-1].name == 'condition':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='condition', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='condition', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(58)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'expr':
                    print("▶ SHIFT : (expr)")
                    if tree_stack[-1].name == 'expr':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='expr', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='expr', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(99)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'compound_condition':
                    print("▶ SHIFT : (compound_condition)")
                    if tree_stack[-1].name == 'compound_condition':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='compound_condition', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='compound_condition', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(38)
                    continue
                elif len(tree_stack) > 0 and tree_stack[-1].name == 'simple_comparison_condition':
                    print("▶ SHIFT : (simple_comparison_condition)")
                    if tree_stack[-1].name == 'simple_comparison_condition':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='simple_comparison_condition', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='simple_comparison_condition', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(39)
                    continue
                if lookahead_typ.value == 'SMP':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SMP', data=lookahead))
                    state_stack.append(13)
                    continue
                if lookahead == 'NOT':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='NOT', data=lookahead))
                    state_stack.append(100)
                    continue
                if lookahead == 'SUM':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SUM', data=lookahead))
                    state_stack.append(14)
                    continue
                if lookahead_typ.value == 'SQL':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SQL', data=lookahead))
                    state_stack.append(16)
                    continue
                if lookahead == '(':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='(', data=lookahead))
                    state_stack.append(101)
                    continue
                if lookahead_typ.value == 'IDT':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='IDT', data=lookahead))
                    state_stack.append(15)
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='TokenType.sql_mapper_parameter NOT SUM TokenType.single_quoted_literal ( TokenType.identifier')" % (lookahead_typ, repr(lookahead)))
                
            case 98:
                # <StateItem simple_comparison_condition→expr simple_comparison_operator ●expr> ☞ ) AND EOF GROUP OR
                # <StateItem@ expr→●IDT . IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●IDT> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SQL> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SMP> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                # <StateItem@ expr→●SUM ( expr )> ☞ != ) , < <= <> = > >= AND EOF FROM GROUP OR ^=
                if len(tree_stack) > 0 and tree_stack[-1].name == 'expr':
                    print("▶ SHIFT : (expr)")
                    if tree_stack[-1].name == 'expr':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='expr', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='expr', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(64)
                    continue
                if lookahead_typ.value == 'SMP':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SMP', data=lookahead))
                    state_stack.append(13)
                    continue
                if lookahead == 'SUM':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SUM', data=lookahead))
                    state_stack.append(14)
                    continue
                if lookahead_typ.value == 'IDT':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='IDT', data=lookahead))
                    state_stack.append(15)
                    continue
                if lookahead_typ.value == 'SQL':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='SQL', data=lookahead))
                    state_stack.append(16)
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='TokenType.sql_mapper_parameter SUM TokenType.identifier TokenType.single_quoted_literal')" % (lookahead_typ, repr(lookahead)))
                
            case 99:
                # <StateItem simple_comparison_condition→expr ●simple_comparison_operator expr> ☞ ) AND EOF GROUP OR
                # <StateItem@ simple_comparison_operator→●=> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●!=> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●^=> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●<>> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●>> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●<> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●>=> ☞ IDT SMP SQL SUM
                # <StateItem@ simple_comparison_operator→●<=> ☞ IDT SMP SQL SUM
                if len(tree_stack) > 0 and tree_stack[-1].name == 'simple_comparison_operator':
                    print("▶ SHIFT : (simple_comparison_operator)")
                    if tree_stack[-1].name == 'simple_comparison_operator':
                        pass
                    else:
                        if tree_stack[-1].data:
                            new_tree = ParseTree(name='simple_comparison_operator', data=tree_stack[-1].data)
                        else:
                            new_tree = ParseTree(name='simple_comparison_operator', children=(tree_stack[-1],))
                        del tree_stack[-1]
                        tree_stack.append(new_tree)
                    state_stack.append(102)
                    continue
                if lookahead == '=':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='=', data=lookahead))
                    state_stack.append(47)
                    continue
                if lookahead == '<':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='<', data=lookahead))
                    state_stack.append(48)
                    continue
                if lookahead == '<=':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='<=', data=lookahead))
                    state_stack.append(49)
                    continue
                if lookahead == '^=':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='^=', data=lookahead))
                    state_stack.append(50)
                    continue
                if lookahead == '<>':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='<>', data=lookahead))
                    state_stack.append(51)
                    continue
                if lookahead == '!=':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='!=', data=lookahead))
                    state_stack.append(52)
                    continue
                if lookahead == '>':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='>', data=lookahead))
                    state_stack.append(53)
                    continue
                if lookahead == '>=':
                    print("▶ SHIFT : (%s,%s)"%(lookahead_typ, repr(lookahead)))
                    del input_tokens[0]
                    tree_stack.append(ParseTree(name='>=', data=lookahead))
                    state_stack.append(54)
                    continue
                raise NotImplementedError("Unexpected(%s;%s, expected='= < <= ^= <> != > >=')" % (lookahead_typ, repr(lookahead)))
                
            case 100:
                # <StateItem compound_condition→NOT ●condition> ☞ ) AND EOF GROUP OR
                raise NotImplementedError("Unexpected(%s;%s, expected='')" % (lookahead_typ, repr(lookahead)))
                
            case 101:
                # <StateItem compound_condition→( ●condition )> ☞ ) AND EOF GROUP OR
                raise NotImplementedError("Unexpected(%s;%s, expected='')" % (lookahead_typ, repr(lookahead)))
                
            case 102:
                # <StateItem simple_comparison_condition→expr simple_comparison_operator ●expr> ☞ ) AND EOF GROUP OR
                raise NotImplementedError("Unexpected(%s;%s, expected='')" % (lookahead_typ, repr(lookahead)))
                
