import sys
import time

import lexer

if __name__ == '__main__':
    tokens = list()
    with open('1.lex', 'r', encoding='utf-8') as read_file:
        while True:
            line = read_file.readline()
            if line:
                line = line.strip()
                typ, data = line[:3], line[4:]

                tokens.append((lexer.TokenType(typ), data))
            else:
                break
    from parser import parse

    try:
        result = parse(input_tokens=tokens)

        with open('1.tree', 'w', encoding='utf-8') as write_file:
            for tree in result:
                print(tree, file=write_file)
    except Exception as e:
        sys.stdout.flush()
        time.sleep(0.1)
        raise e
