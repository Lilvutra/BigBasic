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
    TK_SEP, TK_LINEBREAK, TK_DONE,
    RESERVED_WORDS
)

def main():
    lexer = Lexer("test.src", "arr[1]")
    
    tokens = lexer.tokenize()

    parser = Parser(tokens)
    ast = parser.parse_indexing() #rn, we cant have ast yet after parsing
    print(ast)
    #interpreter = Interpreter()
    #interpreter.eval_program(ast)

if __name__ == "__main__":
    main()
