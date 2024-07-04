from node import *

tokens = (
    'VAR',
    'VAL',
    #'ARGS',
    'IF',
    'ELSE',
    'WHILE',
    'FUN',
    #'MAIN',
    'TINT',
    'TFLOAT',
    'TSTRING',
    'TBOOLEAN',  
    'TCHAR',
    'TVOID',
    'TRUE',
    'FALSE',

    'PRINT_INT',
    'PRINT_FLOAT',
    'PRINT_ARRAYINT',
    'PRINT_ARRAYINT2',
    'PRINT_STRING',
    'PRINT_CHAR',
    'PRINT_BOOLEAN',

    'COMMENT', 'NAME',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'REMAINDER', 'UMINUS',
    'EQUALS', 'NOTEQUALS', 'GE', 'GT', 'LE', 'LT', 'AND', 'OR', 'NOT',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'LBRACKET', 'RBRACKET',
    'ASSIGN', 'DECLARE', 'EXPONENT', 'SEMICOLON', 'COMMA',
    'FLOAT', 'INT', 'STRING', 'CHAR', 'VOID',
)

reserved_keywords = {
	'var':		'VAR',
    'val':		'VAL',
#    'args':		'ARGS',
	
	'if':		'IF',
	'else':		'ELSE',
	'while':	'WHILE',
	
	'function':	'FUN',
#    'main':		'MAIN',
    
	'float':	'TFLOAT',
	'int':		'TINT',
	'string':	'TSTRING',
	'boolean':	'TBOOLEAN',  
	'char':		'TCHAR',
	'void':		'TVOID',
     
	'true':		'TRUE',
	'false':	'FALSE',
     
    'print_int':        'PRINT_INT',
    'print_float':      'PRINT_FLOAT',
    'print_arrayint':   'PRINT_ARRAYINT',
    'print_arrayint2':  'PRINT_ARRAYINT2',
    'print_string':     'PRINT_STRING',
    'print_char':       'PRINT_CHAR',
    'print_boolean':    'PRINT_BOOLEAN',
}


# Tokens

# Expressões regulares

t_CHAR = r'\'[^\']*\''
t_STRING = r'\"[^"]*\"'

# Operadores
t_PLUS      = r'\+'
t_MINUS     = r'-'
t_TIMES     = r'\*'
t_DIVIDE    = r'/'
t_REMAINDER = r'%'

t_EQUALS    = r'='
t_NOTEQUALS = r'!='
t_GE        = r'>='
t_GT        = r'>'
t_LE        = r'<='
t_LT        = r'<'
t_AND       = r'\&\&'
t_OR        = r'\|\|'
t_NOT       = r'!'

# Delimitadores
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_LBRACE    = r'\{'
t_RBRACE    = r'\}'
t_LBRACKET  = r'\['
t_RBRACKET  = r'\]'

t_ASSIGN    = r'\:\='
t_DECLARE   = r':'
t_EXPONENT  = r'\^'
t_SEMICOLON = r';'
t_COMMA     = r','



# Reserved keywords
t_VAR       = r'var'
t_VAL       = r'val'
# t_ARGS      = r'args'
t_IF        = r'if'
t_ELSE      = r'else'
t_WHILE     = r'while'
t_FUN       = r'function'
# t_MAIN      = r'main'
t_TFLOAT    = r'float'
t_TINT      = r'int'
t_TSTRING   = r'string'
t_TBOOLEAN  = r'boolean'
t_TCHAR     = r'char'
t_TVOID     = r'void'
t_TRUE      = r'true'
t_FALSE     = r'false'

t_PRINT_INT = r'print_int'
t_PRINT_FLOAT = r'print_float'
t_PRINT_ARRAYINT = r'print_arrayint'
t_PRINT_ARRAYINT2 = r'print_arrayint2'
t_PRINT_STRING = r'print_string'
t_PRINT_CHAR = r'print_char'
t_PRINT_BOOLEAN = r'print_boolean'



def t_FLOAT(t):
    r'(\-)?([0-9])*[.][0-9]+' 
    return t

def t_INT(t):
    r'(\-)?[0-9]+((_)?[0-9]+)*'
    return t

def t_NAME(t):
	r"[a-zA-Z_][a-zA-Z0-9_]*"
	if t.value.lower() in reserved_keywords:
		t.type = reserved_keywords[t.value.lower()]
	return t


def t_COMMENT(t):
    r'\#.*?(?=\n)'
    pass

t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
# Parsing rules

precedence = (
    ('right', 'UMINUS'),
    ('right', 'EXPONENT'),
    ('left', 'TIMES', 'DIVIDE', 'REMAINDER'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'GE', 'GT', 'LE', 'LT'),
    ('left', 'EQUALS', 'NOTEQUALS'),
    ('left', 'AND'),
    ('left', 'OR'),
)


def p_program(t):
    '''program : function_declarations
               | global_declarations function_declarations
    '''
    if len(t) == 2:
        t[0] = Program([], t[1])
    else:
        t[0] = Program(t[1], t[2])
     

def p_global_declarations(t):
    """global_declarations : global_declarations global_declaration
                           | global_declaration
                           |
    """
    if len(t) == 3:
        t[0] = t[1] + [t[2]]
    elif len(t) == 2:
        t[0] = [t[1]]
    else:
        t[0] = []

def p_global_declaration(t):
    """global_declaration : variable_decl
                          | function_init
    """
    t[0] = t[1]


def p_function_init(t):
    """function_init : FUN name LPAREN parameter_list RPAREN return_type SEMICOLON
    """
    t[0] = FunctionDecl(t[2], t[4], t[6])


def p_function_declarations(t):
    """function_declarations : function_declarations function_decl
                             | function_decl
    """
    if len(t) == 3:
        t[0] = t[1] + [t[2]]
    else:
        t[0] = [t[1]]



def p_function_decl(t):
    """function_decl : FUN name LPAREN parameter_list RPAREN return_type body
    """
    t[0] = FunctionDecl(t[2], t[4], t[6], t[7])

def p_return_type(t):
    """return_type : DECLARE type_or_arraytype
                   |
    """
    if len(t) > 1:
        t[0] = t[2]


def p_variable_decl(t):
    """variable_decl : modifier name DECLARE type_or_arraytype ASSIGN expression SEMICOLON
    """
    t[0] = VariableDecl(t[1], t[2], t[4], t[6])

def p_modifier(t):
    """modifier : VAR
                | VAL
    """
    t[0] = t[1]



def p_body(t):
    """body : LBRACE statement_list RBRACE
    """
    t[0] = t[2]


def p_statement_list(t):
    """statement_list : statement_list statement
                      | statement
    """
    if len(t) == 3:
        t[0] = t[1] + [t[2]]
    else:
        t[0] = [t[1]]



def p_statement(t):
    """statement : if
    		 	 | while
                 | variable_decl
                 | assignment
                 | function_call_inline SEMICOLON
                 | print SEMICOLON
                 |
    """
    if len(t) > 1:
        t[0] = t[1]


def p_if(t):
    """if : IF expression body else
    """
    t[0] = If(t[2], t[3], t[4])

def p_else(t):
    """else : ELSE body
            |
    """
    if len(t) > 1:
        t[0] = Else(t[2])

def p_while_statement(t):
    """while : WHILE expression body
    """
    t[0] = WhileStatement(t[2], t[3])



def p_type_or_arraytype(t):
    """type_or_arraytype : type
                         | LBRACKET type RBRACKET
                         | LBRACKET LBRACKET type RBRACKET RBRACKET
    """
    if len(t) == 2:
        t[0] = t[1]
    elif len(t) == 4:
        t[0] = ArrayType(t[2])
    else:
        t[0] = ArrayType2(t[3])


def p_type(t):
    """type : TVOID
            | TINT
            | TSTRING
            | TBOOLEAN
            | TCHAR
            | TFLOAT
    """
    t[0] = Type(t[1].lower())


def p_function_call_inline(t):
	""" function_call_inline : name LPAREN argument_list RPAREN
    """
	t[0] = FunctionCallInline(t[1], t[3])

def p_print(t):
    """ print : print_type LPAREN value RPAREN
    """
    t[0] = Print(t[1], t[3])

def p_print_type(t):
    """ print_type : PRINT_INT
                   | PRINT_FLOAT
                   | PRINT_ARRAYINT
                   | PRINT_ARRAYINT2
                   | PRINT_STRING
                   | PRINT_CHAR
                   | PRINT_BOOLEAN
    """
    t[0] = t[1]



def p_parameter_list(t):
    """parameter_list : parameter COMMA parameter_list
                      | parameter
                      |
    """
    if len(t) == 2:
        t[0] = [t[1]] 
    elif len(t) == 4:
        t[0] = [t[1]] + t[3]

def p_argument_list(t):
    """argument_list : argument COMMA argument_list
    				 | argument
    				 |
    """
    if len(t) == 2:
        t[0] = [t[1]]
    elif len(t) == 4:
        t[0] = [t[1]] + t[3]


def p_parameter(t):
    """parameter : modifier name DECLARE type_or_arraytype
    """
    t[0] = Parameter(t[1], t[2], t[4])

def p_argument(t):
    """argument : expression
    """
    t[0] = t[1]



def p_expression(t):
	"""expression : expression and_or expression_m
	              | expression_m
	"""
	if len(t) == 2:
		t[0] = t[1]
	else:
		t[0] = Expression(t[2],t[1],t[3])

def p_expression_m(t):
    """expression_m : expression_s
                    | MINUS expression_m
                    | expression_m sign expression_s
    """
    if len(t) == 2:
        t[0] = t[1]
    elif len(t) == 3:
        t[0] = Uminus(t[2])
    else:
        t[0] = Expression(t[2], t[1], t[3])


	
def p_expression_s(t):
	""" expression_s : value 
	                 | expression_s psign value
    """
	if len(t) == 2:
		t[0] = t[1]
	else:
		t[0] = Expression(t[2],t[1],t[3])

def p_and_or(t):
	""" and_or : AND
	           | OR
    """
	t[0] = AndOr(t[1])

def p_psign(t):
	"""psign : TIMES
	         | DIVIDE
    """
	t[0] = Sign(t[1])


def p_sign(t):
	"""sign : PLUS
            | MINUS
            | EXPONENT
            | REMAINDER
            | EQUALS
            | NOTEQUALS
            | GE
            | GT
            | LE
            | LT
	"""
	t[0] = Sign(t[1])



def p_value(t):
    """value : name
             | boolean
             | int
             | float
             | string
             | char
             | void
             | function_call_inline
             | array_call_inline
             | NOT name
             | LPAREN expression RPAREN
	"""
    if len(t) == 2:
        t[0] = Value(t[1])
    elif len(t) == 3:
        t[0] = NotValue(t[2])
    else:
        t[0] = Parenteses(t[2])


def p_assignment(t):
    """assignment : array_call_or_name ASSIGN expression SEMICOLON
    """
    t[0] = Assignment(t[1], t[3])

def p_array_call_or_name(t):
    """array_call_or_name : name
                          | array_call_inline
    """
    t[0] = t[1]

def p_array_call_inline(t):
    """array_call_inline : name LBRACKET value RBRACKET
    				     | name LBRACKET value RBRACKET LBRACKET value RBRACKET
    """
    if len(t) == 5:
        t[0] = ArrayCallInline(t[1], t[3])
    else:
        t[0] = ArrayCallInline(t[1], t[3], t[6])
     

def p_name(t):
    """name : NAME"""
    t[0] = Name(t[1])

def p_boolean(t):
	""" boolean : TRUE
                | FALSE
    """
	t[0] = Boolean(t[1])
	
def p_int(t):
	""" int : INT """
	t[0] = Int(t[1])
     
def p_float(t):
	""" float : FLOAT """
	t[0] = Float(t[1])     

def p_string(t):
	""" string : STRING """
	t[0] = String(t[1])

def p_char(t):
	""" char : CHAR """
	t[0] = Char(t[1])
     
def p_void(t):
	""" void : VOID """
	t[0] = Void(t[1])
     


     
def p_error(t):
    if t:
        raise SyntaxError("Erro de sintaxe no token '" + str(t.value) + "'")
    else:
        raise SyntaxError("Erro de sintaxe: fim inesperado de entrada")



##################################################################

import ply.yacc as yacc
from typechecker import verify, Context as TypeCheckerContext
from compilador import compilador, Context as CompilerContext
import json
import ply.lex as lex
import sys
import os


lexer = lex.lex()
parser = yacc.yacc(debug=True)

def compile_file(filename, tree_flag=False):

    filename_without_path = os.path.splitext(os.path.basename(filename))[0]

    try:
        with open(filename, 'r') as file:
            content = file.read()

        # Parse
        result = parser.parse(content)
        ast_json = result.to_json()
        ast = json.loads(ast_json)

        # Flag tree
        if tree_flag:
            print("AST for file " + filename_without_path  + ".pl :")
            print(ast_json)
            return

        # Typechecking
        #print("Iniciando verificação...")
        verify(TypeCheckerContext(), ast)
        #print("Verificação concluída: sem erros detectados.")

        # Compile
        codigo_llvm = compilador(ast)
        #print(codigo_llvm)

        # LLVM to a file
        with open("code.ll", "w") as f:
            f.write(codigo_llvm)
        
        import subprocess

        subprocess.run(["llc", "-filetype=obj", "code.ll"])
        subprocess.run(["llc", "-filetype=obj", "functions.ll"])
        subprocess.run(["clang", "-o", filename_without_path, "code.o", "functions.o"])

    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    except SyntaxError as e:
        print(f"Parsing error: {e}")
    except TypeError as e:
        print(f"Verification error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")







if __name__ == "__main__":
    
    tree_flag = False
    if "--tree" in sys.argv:
        tree_flag = True
        sys.argv.remove("--tree")
    
    filename = sys.argv[1]
    compile_file(filename, tree_flag)