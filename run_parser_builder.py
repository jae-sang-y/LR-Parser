from typing import Tuple, List

import lexer
from parser_builder import ParserBuilder

if __name__ == '__main__':
    IDT = lexer.TokenType.identifier
    SMP = lexer.TokenType.sql_mapper_parameter
    DQL = lexer.TokenType.double_quoted_literal
    SQL = lexer.TokenType.single_quoted_literal
    data: List[Tuple[str, List]] = [
        ('query', ['insert_statement']),
        ('insert_statement', ['INSERT', 'INTO', 'dst', 'select-query']),
        ('select-query', ['SELECT', 'select-list', 'FROM', 'sources']),
        ('select-query', ['SELECT', 'select-list', 'FROM', 'sources', 'where_clause']),
        ('select-query', ['SELECT', 'select-list', 'FROM', 'sources', 'groupby_clause']),
        ('select-query', ['SELECT', 'select-list', 'FROM', 'sources', 'where_clause', 'groupby_clause']),
        ('sources', ['source', ',', 'sources']),
        ('sources', ['source', ]),
        ('source', ['dst']),
        ('source', ['dst', IDT]),
        ('where_clause', ['WHERE', 'condition']),
        ('condition', ['compound_condition']),
        ('condition', ['simple_comparison_condition']),
        ('compound_condition', ['condition', 'AND', 'condition']),
        ('compound_condition', ['condition', 'OR', 'condition']),
        ('compound_condition', ['NOT', 'condition']),
        ('compound_condition', ['(', 'condition', ')']),
        ('simple_comparison_condition', ['expr', 'simple_comparison_operator', 'expr']),
        ('simple_comparison_operator', ['=']),
        ('simple_comparison_operator', ['!=']),
        ('simple_comparison_operator', ['^=']),
        ('simple_comparison_operator', ['<>']),
        ('simple_comparison_operator', ['>']),
        ('simple_comparison_operator', ['<']),
        ('simple_comparison_operator', ['>=']),
        ('simple_comparison_operator', ['<=']),
        ('expr', [IDT, '.', IDT]),
        ('expr', [IDT]),
        ('expr', [SQL]),
        ('expr', [SMP]),
        ('expr', ['SUM', '(', 'expr', ')']),
        ('groupby_clause', ['GROUP', 'BY', 'groupby_clause_list']),
        ('groupby_clause_list', ['expr']),
        ('groupby_clause_list', ['expr', ',', 'groupby_clause_list']),
        ('select-list', ['expr', ',', 'select-list']),
        ('select-list', ['expr']),
        ('dst', [IDT, '.', IDT]),
    ]
    pb = ParserBuilder()
    pb.build(data)
