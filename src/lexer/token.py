
# Token Types 
TK_STRING       = 'STRONK'     # string
TK_INT          = 'INT'        # interger
TK_FLOAT        = 'FLOAT'      # float
TK_NAME         = 'IDENTIFIER' # IloveCow, CS201, etc
TK_RESERVED     = 'KEYWORD'    # print, input, new, arg, end, if, then
TK_ADD          = 'PLUS'       # +
TK_SUB          = 'MINUS'      # -
TK_ASSIGN       = 'EQ'         # =
TK_LESS         = 'LT'         # <
TK_MORE         = 'GT'         # >
TK_L_PAREN      = 'LPAREN'     # (
TK_R_PAREN      = 'RPAREN'     # )
TK_L_BRACKET    = 'LSQUARE'    # [
TK_R_BRACKET    = 'RSQUARE'    # ]
TK_SEP          = 'COMMA'      # ,
TK_LINEBREAK    = 'NEWLINE'    # \n
TK_DONE         = 'EOF'        # End of File

RESERVED_WORDS = [
  'print', 'input', 'thing', 'arg', 'end', 'new', 
  'if', 'then', 'else', 'for', 'in', 'let'
]


class Token:
    def __init__(self, type, value=None, begin=None, finish=None):
        # type of the token (TK_NUMERIC, TK_ADD...)
        self.type = type
        # value of the token (42, "hi")
        self.value = value

    def equals(self, type, value):
        # check if kind and data match this token
        return self.type == type and self.value == value

    def __repr__(self):
        # print
        if self.value is not None:
            return f'{self.type}:{self.value}'
        return f'{self.type}'
