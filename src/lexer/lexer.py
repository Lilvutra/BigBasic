from token import (
    Token,
    TK_ADD, TK_SUB, TK_ASSIGN, TK_LESS, TK_MORE,
    TK_L_PAREN, TK_R_PAREN, TK_L_BRACKET, TK_R_BRACKET,
    TK_FLOAT, TK_INT, TK_STRING, TK_NAME, TK_RESERVED,
    TK_SEP, TK_LINEBREAK, TK_DONE, TK_BOOL, TK_EQEQ, TK_NEQ,
    TK_MUL, TK_DIV, TK_MOD, TK_DOT,
    RESERVED_WORDS
)

DIGITS = set('0123456789')
LETTERS = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
NAME_BITS = LETTERS.union(DIGITS).union({'_'})

class Lexer:
    def __init__(self, file_name, input_text):
        self.file_name = file_name
        self.text = input_text
        self.idx = -1
        self.char = None
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
            '*': lambda: self.make_simple_token(TK_MUL),
            '/': lambda: self.make_simple_token(TK_DIV),
            '%': lambda: self.make_simple_token(TK_MOD),
            '.': lambda: self.make_simple_token(TK_DOT),
        }

    def advance(self):
        self.idx += 1
        self.char = self.text[self.idx] if self.idx < len(self.text) else None

    def make_simple_token(self, type):
        self.advance()
        return Token(type)

    def skip_whitespace(self):
        while self.char is not None and self.char in {' ', '\t'}:
            self.advance()

    def read_number_token(self):
        start = self.idx
        dot_count = 0

        # count dots
        while self.char is not None and (self.char in DIGITS or self.char == '.'):
            if self.char == '.':
                dot_count += 1
            self.advance()

        value = self.text[start:self.idx]

        # more than one dot > invalid
        if dot_count > 1:
            return Token('INVALID_NUMBER', value)

        try:
            if dot_count == 1:
                return Token(TK_FLOAT, float(value))
            else:
                return Token(TK_INT, int(value))
        except ValueError:
            return Token('INVALID_NUMBER', value)
        
    def read_identifier(self):
        start = self.idx
        while self.char is not None and self.char in NAME_BITS:
            self.advance()
        name = self.text[start:self.idx]
        # boolean literals
        if name == 'rueterb' or name == 'alseferb':
            return Token(TK_BOOL, name == 'rueterb')
        # identifiers vs keywords
        token_type = TK_RESERVED if name in RESERVED_WORDS else TK_NAME
        return Token(token_type, name)

    def read_string(self):
        quote_type = self.char
        self.advance()
        string_value = ''
        while self.char is not None and self.char != quote_type:
            string_value += self.char
            self.advance()
        self.advance()  # skip closing quote
        return Token(TK_STRING, string_value)
    
    def peek(self):
        next_idx = self.idx + 1
        return self.text[next_idx] if next_idx < len(self.text) else None

    def skip_comment(self):
        while self.char is not None and self.char != '\n':
            self.advance()

    def tokenize(self):
        tokens = []
        while self.char is not None:
            self.skip_whitespace()
            if self.char is None:
                break

            if self.char == '=' and self.peek() == '=':
                self.advance(); self.advance()
                tokens.append(Token(TK_EQEQ, '=='))
                continue
            if self.char == '!' and self.peek() == '=':
                self.advance(); self.advance()
                tokens.append(Token(TK_NEQ, '!='))
                continue

            if self.char in DIGITS or (
                self.char == '.' and self.peek() is not None and self.peek() in DIGITS
            ):
                tokens.append(self.read_number_token())
                continue
            elif self.char == '.':
                tokens.append(Token(TK_DOT))
                self.advance()
                continue

            elif self.char == '^' and self.peek() == '^':
                self.advance(); self.advance()
                self.skip_comment()
                continue
            elif self.char in LETTERS or self.char == '_':
                tokens.append(self.read_identifier())
                continue
            elif self.char in {'"', "'"}:
                tokens.append(self.read_string())
                continue
            elif self.char in self.char_handlers:
                tokens.append(self.char_handlers[self.char]())
                continue
            else:
                tokens.append(Token('UNKNOWN', self.char))
                self.advance()

        tokens.append(Token(TK_DONE))
        return tokens

