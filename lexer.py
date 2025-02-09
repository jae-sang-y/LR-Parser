import enum
import re
from typing import Tuple, List, Pattern


class TokenType(enum.Enum):
    sql_mapper_parameter = 'SMP'
    multi_lines_comment = 'MLC'
    single_line_comment = 'SLC'
    single_quoted_literal = 'SQL'
    double_quoted_literal = 'DQL'
    keywords = 'KWD'
    identifier = 'IDT'
    operator = 'OPE'
    EOF = 'EOF'


expr_list: List[Tuple[TokenType, Pattern]] = [
    (TokenType.sql_mapper_parameter, re.compile("#{[^}]+}")),
    (TokenType.multi_lines_comment, re.compile(r"/\*[\S\s]+\*/")),
    (TokenType.single_line_comment, re.compile("--[^\n]+")),
    (TokenType.single_quoted_literal, re.compile("'[^']+'")),
    (TokenType.double_quoted_literal, re.compile('"[^"]+"')),
    (TokenType.keywords, re.compile(
        '(?<![a-zA-Z0-9_$])(%s)(?![a-zA-Z0-9_$])' % '|'.join([
            'ABSOLUTE', 'ACTION', 'ADD', 'ALL', 'ALLOCATE', 'ALTER', 'AND', 'ANY', 'ARE', 'AS', 'ASC', 'ASSERTION',
            'AT', 'AUTHORIZATION', 'AVG', 'BEGIN', 'BETWEEN', 'BIT', 'BIT_LENGTH', 'BOTH', 'BY', 'CASCADE', 'CASCADED',
            'CASE', 'CAST', 'CATALOG', 'CHAR', 'CHARACTER', 'CHARACTER_LENGTH', 'CHAR_', 'CHECK', 'CLOSE', 'COALESCE',
            'COLLATE', 'COLLATION', 'COLUMN', 'COMMIT', 'CONNECT', 'CONNECTION', 'CONSTRAINT', 'CONSTRAINTS',
            'CONTINUE', 'CONVERT', 'CORRESPONDING', 'COUNT', 'CREATE', 'CROSS', 'CURRENT', 'CURRENT_', 'CURRENT_DATE',
            'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'CURSOR', 'DATE', 'DAY', 'DEALLOCATE', 'DEC', 'DECIMAL', 'DECLARE',
            'DEFAULT', 'DEFERRABLE', 'DEFERRED', 'DELETE', 'DESC', 'DESCRIBE', 'DESCRIPTOR', 'DIAGNOSTICS',
            'DISCONNECT', 'DISTINCT', 'DOMAIN', 'DOUBLE', 'DROP', 'ELSE', 'END', 'ESCAPE', 'EXCEPT', 'EXCEPTION',
            'EXEC', 'EXECUTE', 'EXISTS', 'EXTERNAL', 'EXTRACT', 'FALSE', 'FETCH', 'FIRST', 'FLOAT', 'FOR', 'FOREIGN',
            'FOUND', 'FROM', 'FULL', 'GET', 'GLOBAL', 'GO', 'GOTO', 'GRANT', 'GROUP', 'HAVING', 'HOUR', 'IDENTITY',
            'IMMEDIATE', 'IN', 'INDICATOR', 'INITIALLY', 'INNER', 'INPUT', 'INSENSITIVE', 'INSERT', 'INT', 'INTEGER',
            'INTERSECT', 'INTERVAL', 'INTO', 'IS', 'ISOLATION', 'JOIN', 'KEY', 'LANGUAGE', 'LAST', 'LEADING', 'LEFT',
            'LENGTH', 'LEVEL', 'LIKE', 'LOCAL', 'LOWER', 'MATCH', 'MAX', 'MIN', 'MINUTE', 'MODULE', 'MONTH', 'NAMES',
            'NATIONAL', 'NATURAL', 'NCHAR', 'NEXT', 'NO', 'NOT', 'NULL', 'NULLIF', 'NUMERIC', 'OCTET_LENGTH', 'OF',
            'ON', 'ONLY', 'OPEN', 'OPTION', 'OR', 'ORDER', 'OUTER', 'OUTPUT', 'OVERLAPS', 'PAD', 'PARTIAL', 'POSITION',
            'PRECISION', 'PREPARE', 'PRESERVE', 'PRIMARY', 'PRIOR', 'PRIVILEGES', 'PROCEDURE', 'PUBLIC', 'READ', 'REAL',
            'REFERENCES', 'RELATIVE', 'RESTRICT', 'REVOKE', 'RIGHT', 'ROLLBACK', 'ROWS', 'SCHEMA', 'SCROLL', 'SECOND',
            'SECTION', 'SELECT', 'SESSION', 'SESSION_', 'SET', 'SIZE', 'SMALLINT', 'SOME', 'SPACE', 'SQL', 'SQLCODE',
            'SQLERROR', 'SQLSTATE', 'SUBSTRING', 'SUM', 'SYSTEM_USER', 'TABLE', 'TEMPORARY', 'THEN', 'TIME',
            'TIMESTAMP', 'TIMEZONE_', 'TIMEZONE_MINUTE', 'TO', 'TRAILING', 'TRANSACTION', 'TRANSLATE', 'TRANSLATION',
            'TRIM', 'TRUE', 'UNION', 'UNIQUE', 'UNKNOWN', 'UPDATE', 'UPPER', 'USAGE', 'USER', 'USING', 'VALUE',
            'VALUES', 'VARCHAR', 'VARYING', 'VIEW', 'WHEN', 'WHENEVER', 'WHERE', 'WITH', 'WORK', 'WRITE', 'YEAR',
            'ZONE',
        ])
    )),
    (TokenType.identifier, re.compile('[_a-zA-Z$][_a-zA-Z0-9$]*')),
    (TokenType.operator, re.compile(r'(\+|-|=|<|<=|>=|<>|!=|\.|,|\(|\))')),
]


def lex(content: str) -> List[Tuple[int, TokenType, str]]:
    tokens: List[Tuple[int, TokenType, str]] = list()

    for expr_type, expr in expr_list:
        for m in expr.finditer(content):
            if expr_type not in (TokenType.multi_lines_comment, TokenType.single_line_comment):
                tokens.append((m.start(), expr_type, m.group()))
            old_content_len = len(content)
            content = content[:m.start()] + (' ' * len(m.group())) + content[m.end():]
            new_content_len = len(content)
            assert old_content_len == new_content_len
    assert content.isspace(), content

    tokens.sort(key=lambda tup: tup[0])
    return tokens
