from token import (
    Token,
    TK_ADD, TK_SUB, TK_ASSIGN, TK_LESS, TK_MORE,
    TK_L_PAREN, TK_R_PAREN, TK_L_BRACKET, TK_R_BRACKET,
    TK_FLOAT, TK_INT, TK_STRING, TK_NAME, TK_RESERVED,
    TK_SEP, TK_LINEBREAK, TK_DONE,
    RESERVED_WORDS
)

DIGITS = set('0123456789')
LETTERS = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
NAME_BITS = LETTERS.union(DIGITS).union({'_'})

class Lexer:
    def __init__(self, file_name, input_text):
        self.file_name = file_name
        self.text = input_text
        self.idx = -1  # position in the text
        self.char = None  # current character
        self.advance()

        # map single characters to token types
        self.char_handlers = {
            '+': lambda: self.make_simple_token(TK_ADD),
            '-': lambda: self.make_simple_token(TK_SUB),
            '=': lambda: self.make_simple_token(TK_ASSIGN),
            '<': lambda: self.make_simple_token(TK_LESS),
            '>': lambda: self.make_simple_token(TK_MORE),
            '(': lambda: self.make_simple_token(TK_L_PAREN),
            ')': lambda: self.make_simple_token(TK_R_PAREN),
            '[': lambda: self.make_simple_token(TK_L_BRACKET),
            ']': lambda: self.make_simple_token(TK_R_BRACKET),
            ',': lambda: self.make_simple_token(TK_SEP),
            '\n': lambda: self.make_simple_token(TK_LINEBREAK),
        }

    def advance(self):
        # move to the next character
        self.idx += 1
        self.char = self.text[self.idx] if self.idx < len(self.text) else None

    def make_simple_token(self, type):
        # create a token for a single character
        self.advance()
        return Token(type)

    def skip_whitespace(self):
        # skip spaces and tabs
        while self.char is not None and self.char in {' ', '\t'}:
            self.advance()

    def read_number_token(self):
        # read a number (int or float) from input
        start = self.idx
        dot_found = False

        while self.char is not None and (self.char in DIGITS or self.char == '.'):
            if self.char == '.':
                if dot_found:
                    break  # only one dot allowed
                dot_found = True
            self.advance()

        value = self.text[start:self.idx]  # get the number string
        return Token(TK_FLOAT, float(value)) if dot_found else Token(TK_INT, int(value))

    def read_identifier(self):
        # read an identifier (variable name/keyword)
        start = self.idx
        while self.char is not None and self.char in NAME_BITS:
            self.advance()
        name = self.text[start:self.idx]
        token_type = TK_RESERVED if name in RESERVED_WORDS else TK_NAME
        return Token(token_type, name)

    def read_string(self):
        # read a string literal (single or double quoted)
        quote_type = self.char
        self.advance()  # skip the opening quote
        string_value = ''

        while self.char is not None and self.char != quote_type:
            string_value += self.char
            self.advance()

        self.advance()  # skip the closing quote
        return Token(TK_STRING, string_value)

    def tokenize(self):
        # convert text into a list of tokens
        tokens = []

        while self.char is not None:
            self.skip_whitespace()

            if self.char is None:
                break

            if self.char in DIGITS or self.char == '.':
                # read a number token
                tokens.append(self.read_number_token())
            elif self.char in LETTERS or self.char == '_':
                # read an identifier or keyword
                tokens.append(self.read_identifier())
            elif self.char in {'"', "'"}:
                # read a string literal
                tokens.append(self.read_string())
            elif self.char in self.char_handlers:
                # use the handler to generate a token
                tokens.append(self.char_handlers[self.char]())
            else:
                # unknown character
                tokens.append(Token('UNKNOWN', self.char))
                self.advance()

        # end-of-input token
        tokens.append(Token(TK_DONE))
        return tokens
