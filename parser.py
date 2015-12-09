__author__ = 'andreasbotero'
import sys

tokens = []
synch = [';', 'EOF']
syntax_er = []
new_list_file = {}
# list_file = open('list_file', 'w')
lex_analysis_listing_file = open('list_file', 'r')


def add_tokens():
    with open('write_it.txt', 'r') as token_file:
        next(token_file)
        for line in token_file:
            tokens.append(line.replace(' ', '').split('|'))
            # for item in tokens:
            #     print item
    last_line = 0
    for line in lex_analysis_listing_file:
        if line[0].isdigit():
            new_list_file[line.split('\t')[0]] = [line]
            last_line = int(line.split('\t')[0])
        else:
            new_list_file[str(last_line)].append(line)


# def add_syntax_errors():
#     if not syntax_er:
#         with open('list_file', 'r') as list_f:
#             for line in list_f:
#                 temp_list.append(line)
#         for i in temp_list:
#             print i


def get_line_number():
    token = tokens[0]
    return token[0]


def peek_token():
    token = tokens[0]
    # line_number = token[0]
    conversion = {
        '14REV': token[1],
        '10ID': 'id',
        'COMMA': token[1],
        'CLOSE-PAR': token[1],
        'TERMINATE': token[1],
        'OPEN-PAR': token[1],
        'colon': token[1],
        '11INT': 'integer',
        'SINGOP': 'assignop',
        'DOT': token[1],
        'ADDOP': 'addop',
        'MULOP': 'mulop',
        'RELOP': 'relop',
        'D-DOT': token[1],
        'EOF': '$',
        '13REAL': 'real',
        '99LEXERR': 'LEXERR',
        'OPEN-BRA': token[1],
        'CLOSE-BRA': token[1]
    }
    return conversion[token[2]]


def get_token():
    try:
        return tokens.pop(0)
    except IndexError:
        return False


def finish():
    print 'PARSE COMPLETE'
    write_new_listing_file()
    sys.exit(0)


def match(expect_token):
    if expect_token == 'num':
        expected_tokens = ['integer', 'real']
        peek = peek_token()
        if peek in expected_tokens:
            if peek != '$':
                get_token()
            else:
                finish()
        else:
            syntax_error(peek, expected_tokens)
    else:
        peek = peek_token()
        if peek == expect_token and peek != '$':
            get_token()
        elif peek == expect_token and peek == '$':
            finish()
        elif peek != expect_token:
            syntax_error(peek, expect_token)


def parse():
    add_tokens()
    prg()
    match('$')
    write_new_listing_file()


def write_new_listing_file():
    new_file = open('final_listing_file.txt', 'w')
    for key in sorted(new_list_file):
        for line in new_list_file[key]:
            new_file.write(line + '\n')
    new_file.close()


def syntax_error(given_token, *expected):
    line_number = get_line_number()

    error = "Syntax Error: in line " + line_number + " Expecting %s" % (expected,) + "received " + str(given_token)
    # syntax_er.append(error)
    new_list_file[line_number].append(error)

    print "Syntax Error: in line " + line_number + " Expecting %s" % (expected,) + "received " + str(given_token)
    token = peek_token()
    while token not in synch:
        get_token()
        if len(tokens) != 0:
            token = peek_token()
        else:
            finish()


def prg():
    token = peek_token()
    if token == 'program':
        match('program')
        match('id')
        match('(')
        idlist()
        match(')')
        match(';')
        prg_()
    else:
        syntax_error(token, 'program')


def prg_():
    token = peek_token()
    if token == 'begin':
        compstate()
        match('.')
    elif token == 'function':
        subprgdeclarations()
        compstate()
        match('.')
    elif token == 'var':
        declarations()
        prg__()
    else:
        syntax_error(token, 'begin', 'function', 'var')


def prg__():
    token = peek_token()
    if token == 'begin':
        compstate()
        match('.')
    elif token == 'function':
        subprgdeclarations()
        compstate()
        match('.')
    else:
        syntax_error(token, 'begin', 'function')


def idlist():
    token = peek_token()
    if token == 'id':
        match('id')
        idlist_()
    else:
        syntax_error(token, 'id')


def idlist_():
    token = peek_token()
    if token == ')':
        pass
    elif token == ',':
        match(',')
        match('id')
        idlist_()
    else:
        syntax_error(token, ')', ',')


def declarations():
    token = peek_token()
    if token == 'var':
        match('var')
        match('id')
        match(':')
        type_()
        match(';')
        declarations_()
    else:
        syntax_error(token, 'var')


def declarations_():
    token = peek_token()
    if token == 'begin':
        pass
    elif token == 'function':
        pass
    elif token == 'var':
        match('var')
        match('id')
        match(':')
        type_()
        match(';')
        declarations_()
    else:
        syntax_error(token, 'begin', 'function', 'var')


def type_():
    token = peek_token()
    if token == 'array':
        match('array')
        match('[')
        match('num')
        match('..')
        match('num')
        match(']')
        match('of')
        standtype()
    elif token == 'integer':
        standtype()
    elif token == 'real':
        standtype()
    else:
        syntax_error(token, 'array', 'integer', 'real')


def standtype():
    token = peek_token()
    if token == 'integer':
        match('integer')
    elif token == 'real':
        match('real')
    else:
        syntax_error(token, 'integer', 'real')


def subprgdeclarations():
    token = peek_token()
    if token == 'function':
        subprgdeclaration()
        match(';')
        subprgdeclarations_()
    else:
        syntax_error(token, 'function')


def subprgdeclarations_():
    token = peek_token()
    if token == 'begin':
        pass
    elif token == 'function':
        subprgdeclaration()
        match(';')
        subprgdeclarations_()
    else:
        syntax_error(token, 'begin', 'function')


def subprgdeclaration():
    token = peek_token()
    if token == 'function':
        subprghead()
        subprgdeclaration_()
    else:
        syntax_error(token, 'function')


def subprgdeclaration_():
    token = peek_token()
    if token == 'begin':
        compstate()
    elif token == 'function':
        declarations()
        subprgdeclaration__()
    elif token == 'var':
        declarations()
        subprgdeclaration__()
    else:
        syntax_error(token, 'begin', 'function', 'var')


def subprgdeclaration__():
    token = peek_token()
    if token == 'begin':
        compstate()
    elif token == 'function':
        subprgdeclarations()
        compstate()
    else:
        syntax_error(token, 'begin', 'function')


def subprghead():
    token = peek_token()
    if token == 'function':
        match('function')
        match('id')
        subprghead_()
    else:
        syntax_error(token, 'function')


def subprghead_():
    token = peek_token()
    if token == '(':
        arguments()
        match(':')
        standtype()
        match(';')
    elif token == ':':
        match(':')
        standtype()
        match(';')
    else:
        syntax_error(token, '(', ':')


def arguments():
    token = peek_token()
    if token == '(':
        match('(')
        paramlist()
        match(')')
    else:
        syntax_error(token, '(')


def paramlist():
    token = peek_token()
    if token == 'id':
        match('id')
        match(':')
        type_()
        paramlist_()
    else:
        syntax_error(token, 'id')


def paramlist_():
    token = peek_token()
    if token == ')':
        pass
    elif token == ';':
        match(';')
        match('id')
        match(':')
        type_()
        paramlist_()
    else:
        syntax_error(token, '(', ';')


def compstate():
    token = peek_token()
    if token == 'begin':
        match('begin')
        compstate_()
    else:
        syntax_error(token, 'begin')


def compstate_():
    token = peek_token()
    if token == 'begin':
        optionalstate()
        match('end')
    elif token == 'end':
        match('end')
    elif token == 'id':
        optionalstate()
        match('end')
    elif token == 'if':
        optionalstate()
        match('end')
    elif token == 'while':
        optionalstate()
        match('end')
    else:
        syntax_error(token, 'begin', 'end', 'id', 'if', 'while')


def optionalstate():
    token = peek_token()
    if token == 'begin':
        statementlist()
    elif token == 'id':
        statementlist()
    elif token == 'if':
        statementlist()
    elif token == 'while':
        statementlist()
    else:
        syntax_error(token, 'begin', 'id', 'if', 'while')


def statementlist():
    token = peek_token()
    if token == 'begin':
        statement()
        statementlist_()
    elif token == 'id':
        statement()
        statementlist_()
    elif token == 'if':
        statement()
        statementlist_()
    else:
        syntax_error(token, 'begin', 'id', 'if')


def statementlist_():
    token = peek_token()
    if token == ';':
        match(';')
        statement()
        statementlist_()
    elif token == 'end':
        pass
    else:
        syntax_error(token, ';', 'end')


def statement():
    token = peek_token()
    if token == 'begin':
        compstate()
    elif token == 'id':
        variable()
        match('assignop')
        expression()
    elif token == 'if':
        match('if')
        expression()
        match('then')
        statement()
        statement_()
    elif token == 'while':
        match('while')
        expression()
        match('do')
        statement()
    else:
        syntax_error(token, 'begin', 'id', 'assignop', 'if', 'while')


def statement_():
    token = peek_token()
    if token == ';':
        pass
    elif token == 'else':
        match('else')
        statement_()
    elif token == 'end':
        pass
    else:
        syntax_error(token, ';', 'else', 'end')


def variable():
    token = peek_token()
    if token == 'id':
        match('id')
        variable_()
    else:
        syntax_error(token, 'id')


def variable_():
    token = peek_token()
    if token == '[':
        match('[')
        expression()
        match(']')
    elif token == 'assignop':
        pass
    else:
        syntax_error(token, '[', 'assignop')


def expresslist():
    token = peek_token()
    if token == '(':
        expression()
        expresslist_()
    elif token == '+':
        expression()
        expresslist_()
    elif token == '-':
        expression()
        expresslist_()
    elif token == 'id':
        expression()
        expresslist_()
    elif token == 'not':
        expression()
        expresslist_()
    elif token == 'num':
        expression()
        expresslist_()
    else:
        syntax_error(token, '(', '+', '-', 'id', 'not', 'num')


def expresslist_():
    token = peek_token()
    if token == ')':
        pass
    elif token == ',':
        match(',')
        expression()
        expresslist_()
    else:
        syntax_error(token, ')', ',')


def expression():
    token = peek_token()
    if token == '(' or token == '+' or token == '-' or token == 'id' or token == 'not' or token == 'real' or token == 'integer':
        simpexpression()
        expression_()
    else:
        syntax_error(token, '(', '+', '-', 'id', 'not', 'num')


def expression_():
    token = peek_token()
    if token == ')':
        pass
    elif token == ',':
        pass
    elif token == ';':
        pass
    elif token == ']':
        pass
    elif token == 'do':
        pass
    elif token == 'else':
        pass
    elif token == 'end':
        pass
    elif token == 'relop':
        match('relop')
        simpexpression()
    elif token == 'then':
        pass
    else:
        syntax_error(token, ')', ',', ';', ']', 'do', 'else', 'end', 'relop', 'then')


def simpexpression():
    token = peek_token()
    if token == '(':
        term()
        simpexpression_()
    elif token == '+':
        sign()
        term()
        simpexpression_()
    elif token == '-':
        sign()
        term()
        simpexpression_()
    elif token == 'id':
        term()
        simpexpression_()
    elif token == 'not':
        term()
        simpexpression_()
    elif token == 'real' or token == 'integer':
        term()
        simpexpression_()
    else:
        syntax_error(token, '(', '+', '-', 'id', 'not', 'num')


def simpexpression_():
    token = peek_token()
    if token == ')':
        pass
    elif token == ',':
        pass
    elif token == ';':
        pass
    elif token == ']':
        pass
    elif token == 'addop':
        match('addop')
        term()
        simpexpression_()
    elif token == 'do':
        pass
    elif token == 'end':
        pass
    elif token == 'relop':
        pass
    elif token == 'then':
        pass
    else:
        syntax_error(token, ')', ',', ';', ']', 'addop', 'do', 'end', 'relop', 'then')


def term():
    token = peek_token()
    if token == '(':
        factor()
        term_()
    elif token == 'id':
        factor()
        term_()
    elif token == 'not':
        factor()
        term_()
    elif token == 'integer' or token == 'real':
        factor()
        term_()
    else:
        syntax_error('(', 'id', 'not', 'num')


def term_():
    token = peek_token()
    if token == ')':
        pass
    elif token == ',':
        pass
    elif token == ';':
        pass
    elif token == ']':
        pass
    elif token == 'addop':
        pass
    elif token == 'do':
        pass
    elif token == 'else':
        pass
    elif token == 'end':
        pass
    elif token == 'mulop':
        match('mulop')
        factor()
        term_()
    elif token == 'relop':
        pass
    elif token == 'then':
        pass
    else:
        syntax_error(token, ')', ',', ';', ']', 'addop', 'do', 'else', 'end', 'mulop', 'relop', 'then')


def factor():
    token = peek_token()
    if token == 'id':
        match('id')
        factor_()
    elif token == 'not':
        match('not')
        factor()
    elif token == 'integer' or token == 'real':
        match('num')
    else:
        syntax_error(token, 'id', 'not', 'num')


def factor_():
    token = peek_token()
    if token == '(':
        match('(')
        expresslist()
        match(')')
    elif token == ')':
        pass
    elif token == ',':
        pass
    elif token == ';':
        pass
    elif token == '[':
        match('[')
        expression()
        match(']')
    elif token == ']':
        pass
    elif token == 'addop':
        pass
    elif token == 'do':
        pass
    elif token == 'else':
        pass
    elif token == 'end':
        pass
    elif token == 'mulop':
        pass
    elif token == 'relop':
        pass
    elif token == 'then':
        pass
    else:
        syntax_error(token, '(', ')', ',', ';', '[', ']', 'addop', 'do', 'else', 'end', 'mulop', 'relop', 'then')


def sign():
    token = peek_token()
    if token == '+':
        match('+')
    elif token == '-':
        match('-')
    else:
        syntax_error(token, '+', '-')
