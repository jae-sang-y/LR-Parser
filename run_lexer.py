import lexer

if __name__ == '__main__':
    print('hihi3')
    with open('1.sql', 'r', encoding='utf-8') as read_file:
        content = read_file.read()

    tokens = lexer.lex(content)
    with open('1.lex', 'w', encoding='utf-8') as write_file:
        for pos, token_type, token_data in tokens:
            print(token_type.value, token_data, file=write_file)
        print(lexer.TokenType.EOF.value, file=write_file)
