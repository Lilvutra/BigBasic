#from lexer.lexer import Lexer
from parser import Parser
#from runtime.interpreter import Interpreter
#from lexer.token import Token
from lexer import Lexer
from token import (
    Token,
    TK_ADD, TK_SUB, TK_ASSIGN, TK_LESS, TK_MORE,
    TK_L_PAREN, TK_R_PAREN, TK_L_BRACKET, TK_R_BRACKET,
    TK_FLOAT, TK_INT, TK_STRING, TK_NAME, TK_RESERVED,
    TK_SEP, TK_LINEBREAK, TK_DONE, TK_UNARY_INC, TK_UNARY_DEC,
    TK_ASSIGN_ADD, TK_ASSIGN_SUB,
    TK_BOOL, TK_EQEQ, TK_NEQ, TK_MUL, TK_DIV,
    TK_MOD, TK_DOT, TK_UNARY_NOT, TK_ASSIGN_ADD, 
    TK_ASSIGN_SUB, TK_UNARY_NOT, TK_UNARY_INC, TK_UNARY_DEC,
    RESERVED_WORDS
)

def main():
    #lexer = Lexer("main", "arr[1]")
    #lexer = Lexer("main", "++x" )
    #lexer = Lexer("main", "x++1" )
    #lexer = Lexer("main", "x and y" )
    #lexer = Lexer("main", "x+=1" )
    #lexer = Lexer("main", "x-=1" )
    #lexer = Lexer("main", " a and (b and c)")
    lexer = Lexer("main", " -(-b) ")
    # lexer not yet successfully implemented unary operators, -(-4) and -4 assign same NumberNode(value=4)
    # Note: x++1 supposed to return error since x++1 is not a valid expression
    
    tokens = lexer.tokenize()
    for token in tokens:
        print(token)

    parser = Parser(tokens)
    ast = parser.parse() #rn, we cant have ast yet after parsing
    print(f"ast: {ast}")
    #interpreter = Interpreter()
    #interpreter.eval_program(ast)

if __name__ == "__main__":
    main()
