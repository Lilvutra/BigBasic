# Check for homogenous array

from lexer import Lexer
from token import (
    Token,
    TK_ADD, TK_SUB, TK_ASSIGN, TK_LESS, TK_MORE,
    TK_L_PAREN, TK_R_PAREN, TK_L_BRACKET, TK_R_BRACKET,
    TK_FLOAT, TK_INT, TK_STRING, TK_NAME, TK_RESERVED,
    TK_SEP, TK_LINEBREAK, TK_DONE,
    RESERVED_WORDS
)

# AST Nodes
class ProgramNode:
    def __init__(self, statements):
        self.statements = statements

class AssignmentNode:
    def __init__(self, name, value):
        self.name = name
        self.value = value
    def __repr__(self):
        return f"AssignmentNode(name={self.name}, value={self.value})"

class ArrayNode:
    def __init__(self, elements):
        self.elements = elements
    def __repr__(self):
        return f"ArrayNode(elements={self.elements})"

class NumberNode:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"NumberNode(value={self.value})"
        

class StringNode:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"StringNode(value={self.value})"

class IdentifierNode:
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f"IdentifierNode(name={self.name})"

class IndexNode:
    def __init__(self, name, index):
        self.name = name
        self.index = index
    def __repr__(self):
        return f"IndexNode(name={self.name}, index={self.index})"


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = -1
        self.current_token = None
        self.advance()

    def advance(self):
        self.position += 1
        if self.position < len(self.tokens):
            self.current_token = self.tokens[self.position]
        else:
            self.current_token = None

    def peek(self, offset=1):
        pos = self.position + offset
        if pos < len(self.tokens):
            return self.tokens[pos]
        else:
            return None

    def check(self, expected_type):
        return self.current_token and self.current_token.type == expected_type

    def expect(self, expected_type):
        if self.current_token is None:
            raise Exception("Unexpected end of input")
        if self.current_token.type != expected_type:
            raise Exception(f"Expected {expected_type}, got {self.current_token.type}")
        token = self.current_token
        self.advance()
        print(f"Expecting token: {token}")
        return token

    def parse_expression(self):
        tok = self.current_token
        print(f"Parsing expression: {tok}")

        if tok.type == TK_L_BRACKET:
            return self.parse_array()
        elif tok.type == TK_NAME and self.peek().type == TK_L_BRACKET:
            return self.parse_indexing()
        elif tok.type == TK_NAME:
            return self.parse_variable_reference()
        elif tok.type in (TK_INT, TK_FLOAT, TK_STRING):
            return self.parse_literal()
        else:
            raise Exception(f"Unexpected token in expression: {tok}")

    def parse_variable(self):
        name_token = self.expect(TK_NAME)
        self.expect(TK_ASSIGN)
        value = self.parse_expression()
        return AssignmentNode(name_token.value, value)

    def parse_variable_reference(self):
        name = self.expect(TK_NAME).value
        return IdentifierNode(name)

    def parse_literal(self):
        tok = self.current_token
        if tok.type == TK_INT:
            self.advance()
            return NumberNode(int(tok.value))
        elif tok.type == TK_FLOAT:
            self.advance()
            return NumberNode(float(tok.value))
        elif tok.type == TK_STRING:
            self.advance()
            return StringNode(tok.value)
        else:
            raise Exception(f"Invalid literal: {tok}")

    def parse_array(self):
        # arr = [1, 2, 3]
        name = self.expect(TK_NAME).value
        self.expect(TK_ASSIGN)
        self.expect(TK_L_BRACKET)

        elements = []
        if self.current_token.type != TK_R_BRACKET:
            while True:
                elements.append(self.parse_expression())
                if self.current_token.type == TK_SEP:
                    self.advance()
                elif self.current_token.type == TK_R_BRACKET:
                    break
                else:
                    raise Exception(f"Expected ',' or ']', got {self.current_token}")

        self.expect(TK_R_BRACKET)
        return AssignmentNode(name, ArrayNode(elements))

    def parse_indexing(self):
        name = self.expect(TK_NAME).value
        self.expect(TK_L_BRACKET)
        index_expr = self.parse_expression()
        self.expect(TK_R_BRACKET)
        return IndexNode(name, index_expr)
