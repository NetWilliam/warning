
# -----------------------------------------------------------------------------
# calc.py
#
# A simple calculator with variables -- all in one file.
# -----------------------------------------------------------------------------

tokens = (
    'NAME','NUMBER',
    'PLUS','MINUS','TIMES','DIVIDE','EQUALS',
    'LPAREN','RPAREN','GT','GE','LT','LE','NE'
    )

# Tokens

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_EQUALS  = r'='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_NAME    = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_GT      = r'>'
t_GE      = r'>='
t_LT      = r'<'
t_LE      = r'<='
t_NE      = r'!='
#t_NOT     = r'!'

def t_NUMBER(t):
    r'\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

# Ignored characters
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
# Build the lexer
import ply.lex as lex
lexer = lex.lex()

# Parsing rules

precedence = (
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE'),
    ('right','UMINUS'),
    )

# dictionary of names
names = { }
result = None

def p_statement_assign(t):
    'statement : NAME EQUALS expression'
    names[t[1]] = t[3]

def p_statement_expr(t):
    'statement : expression'
    #print(t[1])
    global result
    result = t[1]

#def p_statement_end(t):
#    'statement : $end'
#    print(t[1])
#    return t[1]

def p_expression_compare(t):
    '''expression : expression GT expression
                  | expression GE expression
                  | expression LT expression
                  | expression LE expression
                  | expression NE expression
    '''
    if t[2] == '>' : t[0] = t[1] > t[3]
    elif t[2] == '>=' : t[0] = t[1] >= t[3]
    elif t[2] == '<' : t[0] = t[1] < t[3]
    elif t[2] == '<=' : t[0] = t[1] <= t[3]
    elif t[2] == '!=' : t[0] = t[1] != t[3]


def p_expression_binop(t):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    if t[2] == '+'  : t[0] = t[1] + t[3]
    elif t[2] == '-': t[0] = t[1] - t[3]
    elif t[2] == '*': t[0] = t[1] * t[3]
    elif t[2] == '/': t[0] = t[1] / t[3]

def p_expression_uminus(t):
    'expression : MINUS expression %prec UMINUS'
    t[0] = -t[2]

def p_expression_group(t):
    'expression : LPAREN expression RPAREN'
    t[0] = t[2]

def p_expression_number(t):
    'expression : NUMBER'
    t[0] = t[1]

def p_expression_name(t):
    'expression : NAME'
    try:
        t[0] = names[t[1]]
    except LookupError:
        print("Undefined name '%s'" % t[1])
        t[0] = 0

def p_error(t):
    print("Syntax error at '%s'" % t.value)

import ply.yacc as yacc
parser = yacc.yacc()

if __name__ == "__main__":
    while True:
        try:
            s = raw_input('calc > ')   # Use raw_input on Python 2
        except EOFError:
            break
        #print "parse output:", parser.parse(s, debug=1)
        parser.parse(s)
        print "parse output:", result
