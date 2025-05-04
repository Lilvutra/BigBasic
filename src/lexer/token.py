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
TK_BOOL         = 'BOOLEAN'    #Add tokens
TK_EQEQ         = 'EQEQ'       # ==
TK_NEQ          = 'NEQ'        # !=
TK_MUL          = 'MUL'        # *
TK_DIV          = 'DIV'        # /
TK_MOD          = 'MOD'        # %
TK_DOT          = 'DOT'        # .


#Add keywords "true", "false"
RESERVED_WORDS = [
   'rintperb',   # print
   'nputiperb',  # input
   'hingterb',   # thing
   'rgaerb',    # arg
   'ndeerb',      # end
   'ewnerb',     # new
   'if',         
   'henterb',     # then
   'lseerb',     # else
   'utifberb',   # butif
   'orferb',     # for
   'in',         
   'etlerb',     # let
   'rueterb',    # true
   'alseferb',   # false
   'ndaerb',     # and
   'or',         
   'otnerb',     # not
   'atchmerb',   # match
   'asecerb',    # case
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
