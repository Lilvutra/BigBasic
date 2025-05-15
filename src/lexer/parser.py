from token import (
    Token,
    TK_ADD, TK_SUB, TK_ASSIGN, TK_LESS, TK_MORE,
    TK_L_PAREN, TK_R_PAREN, TK_L_BRACKET, TK_R_BRACKET,
    TK_FLOAT, TK_INT, TK_STRING, TK_NAME, TK_RESERVED,
    TK_SEP, TK_LINEBREAK, TK_DONE, TK_BOOL, TK_EQEQ, TK_NEQ,
    TK_MUL, TK_DIV, TK_MOD, TK_DOT,
    RESERVED_WORDS
)

# AST Nodes
class ProgramNode:
    def __init__(self, statements):
        self.statements = statements
    def __repr__(self):
        return f"ProgramNode(statements={self.statements})"

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

class PrintNode:
    def __init__(self, expression):
        self.expression = expression
    def __repr__(self):
        return f"PrintNode(expression={self.expression})"

class IfNode:
    def __init__(self, condition, then_branch, else_branch=None):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch
    def __repr__(self):
        return f"IfNode(condition={self.condition}, then={self.then_branch}, else={self.else_branch})"

class ComparisonNode:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
    def __repr__(self):
        return f"ComparisonNode({self.left} {self.op} {self.right})"

class BooleanNode:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"BooleanNode(value={self.value})"

class UnaryOpNode:
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr
    def __repr__(self):
        return f"UnaryOpNode(op={self.op}, expr={self.expr})"

class BinaryOpNode:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
    def __repr__(self):
        return f"BinaryOpNode({self.left} {self.op} {self.right})"

class BlockNode:
    def __init__(self, statements):
        self.statements = statements
    def __repr__(self):
        return f"BlockNode(statements={self.statements})"
    
class ForNode:
    def __init__(self, var_name, iterable, body):
        self.var_name = var_name
        self.iterable = iterable
        self.body = body
    def __repr__(self):
        return f"ForNode(var={self.var_name}, iterable={self.iterable}, body={self.body})"

class ThingDefNode:
    def __init__(self, name, args):
        self.name = name      
        self.args = args        
    def __repr__(self):
        return f"ThingDefNode(name={self.name}, args={self.args})"

class NewNode:
    def __init__(self, type_name, init_args):
        self.type_name = type_name  
        self.init_args = init_args  
    def __repr__(self):
        return f"NewNode(type={self.type_name}, init_args={self.init_args})"

class AttrAccessNode:
    def __init__(self, obj, attr):
        self.obj = obj          
        self.attr = attr        
    def __repr__(self):
        return f"AttrAccessNode(obj={self.obj}, attr={self.attr})"

class PatternLiteral:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"PatternLiteral({self.value})"

class PatternVar:
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f"PatternVar({self.name})"

class PatternWildcard:
    def __repr__(self):
        return "PatternWildcard()"

class MatchNode:
    def __init__(self, expr, cases, else_branch=None):
        # cases: list of (pattern, body_node)
        self.expr = expr
        self.cases = cases
        self.else_branch = else_branch
    def __repr__(self):
        return f"MatchNode(expr={self.expr}, cases={self.cases}, else={self.else_branch})"

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = -1
        self.current_token = None
        self.advance()

    def advance(self):
        self.position += 1
        self.current_token = self.tokens[self.position] if self.position < len(self.tokens) else None

    def peek(self, offset=1):
        pos = self.position + offset
        return self.tokens[pos] if pos < len(self.tokens) else None

    def check(self, expected_type):
        return self.current_token and self.current_token.type == expected_type

    def expect(self, expected_type):
        if not self.current_token:
            raise Exception("Unexpected end of input")
        if self.current_token.type != expected_type:
            raise Exception(f"Expected {expected_type}, got {self.current_token.type}")
        token = self.current_token
        self.advance()
        return token

    def parse(self):
        statements = []
        while self.current_token and self.current_token.type != TK_DONE:
            if self.check(TK_LINEBREAK):
                self.advance()
                continue
            if self.check(TK_RESERVED) and self.current_token.value == 'hingterb':
                stmt = self.parse_thing_def()
            elif self.check(TK_RESERVED) and self.current_token.value == 'rintperb':
                stmt = self.parse_print()
            elif self.check(TK_RESERVED) and self.current_token.value in ('if', 'utifberb'):
                stmt = self.parse_if()
            elif self.check(TK_RESERVED) and self.current_token.value == 'atchmerb':
                stmt = self.parse_match()
            elif self.check(TK_RESERVED) and self.current_token.value == 'orferb':
                stmt = self.parse_for()
            elif self.check(TK_NAME) and self.peek().type == TK_ASSIGN:
                stmt = self.parse_variable()
            else:
                stmt = self.parse_expression()
            statements.append(stmt)
            while self.check(TK_LINEBREAK):
                self.advance()
        return ProgramNode(statements)

    def parse_variable(self):
        name = self.expect(TK_NAME).value
        self.expect(TK_ASSIGN)
        value = self.parse_array_expression() if self.check(TK_L_BRACKET) else self.parse_expression()
        return AssignmentNode(name, value)

    def parse_expression(self):
        return self.parse_or()

    def parse_or(self):
        left = self.parse_and()
        while self.check(TK_RESERVED) and self.current_token.value == 'or':
            op = self.current_token.value
            self.advance()
            right = self.parse_and()
            left = BinaryOpNode(left, op, right)
        return left

    def parse_and(self):
        left = self.parse_not()
        while self.check(TK_RESERVED) and self.current_token.value == 'ndaerb':
            op = 'and'
            self.advance()
            right = self.parse_not()
            left = BinaryOpNode(left, op, right)
        return left

    def parse_not(self):
        if self.check(TK_RESERVED) and self.current_token.value == 'otnerb':
            op = 'not'
            self.advance()
            expr = self.parse_not()
            return UnaryOpNode(op, expr)
        return self.parse_comparison()

    def parse_comparison(self):
        left = self.parse_add_sub()

        while (self.check(TK_LESS) or self.check(TK_MORE)
               or self.check(TK_EQEQ) or self.check(TK_NEQ)):
            op_tok = self.current_token
            self.advance()
            right = self.parse_comparison()
            left = ComparisonNode(left, op_tok.value or op_tok.type, right)

        return left


    def parse_literal(self):
        tok = self.current_token
        if tok.type == TK_INT:
            self.advance()
            return NumberNode(int(tok.value))
        if tok.type == TK_FLOAT:
            self.advance()
            return NumberNode(float(tok.value))
        if tok.type == TK_STRING:
            self.advance()
            return StringNode(tok.value)
        if tok.type == TK_BOOL:
            self.advance()
            return BooleanNode(tok.value)
        raise Exception(f"Invalid literal: {tok}")

    def parse_array_expression(self):
        self.expect(TK_L_BRACKET)
        elements = []

        while not self.check(TK_R_BRACKET):
            while self.check(TK_LINEBREAK):
                self.advance()

            elements.append(self.parse_expression())

            while self.check(TK_LINEBREAK):
                self.advance()  

            if self.check(TK_SEP):
                self.advance()
            elif self.check(TK_R_BRACKET):
                break
            else:
                raise Exception(f"Expected ',' or ']', got {self.current_token}")

        self.expect(TK_R_BRACKET)
        return ArrayNode(elements)


    def parse_indexing(self):
        name = self.expect(TK_NAME).value
        self.expect(TK_L_BRACKET)
        idx = self.parse_expression()
        self.expect(TK_R_BRACKET)
        return IndexNode(name, idx)

    def parse_print(self):
        self.expect(TK_RESERVED)
        expr = self.parse_expression()
        return PrintNode(expr)

    def parse_if(self):
        # initial 'if' or 'butif' keyword
        self.advance()
        return self._parse_if_branch()

    def _parse_if_branch(self, require_end=True):
        condition = self.parse_expression()

        if not (self.check(TK_RESERVED) and self.current_token.value == 'henterb'):
            raise Exception(f"Expected 'henterb', got {self.current_token}")
        self.advance()

        # enforce block-style only
        if not self.check(TK_LINEBREAK):
            raise Exception("Expected newline after 'henterb' in 'if'")

        self.advance()  # skip newline
        then_branch = self.parse_block()

        while self.check(TK_LINEBREAK):
            self.advance()

        else_branch = None
        if self.check(TK_RESERVED) and self.current_token.value in ('utifberb', 'lseerb'):
            kind = self.current_token.value
            self.advance()
            while self.check(TK_LINEBREAK):
                self.advance()
            if kind == 'utifberb':
                # nested 'elif'—do _not_ require its own 'ndeerb'
                else_branch = self._parse_if_branch(require_end=False)
            else:
                else_branch = self.parse_block()

        while self.check(TK_LINEBREAK):
            self.advance()

        # finally, close the block if we're the outermost if
        if require_end:
            if not (self.check(TK_RESERVED) and self.current_token.value == 'ndeerb'):
                raise Exception("Expected 'ndeerb' to close 'if' block")
            self.advance()
            while self.check(TK_LINEBREAK):
                self.advance()

        return IfNode(condition, then_branch, else_branch)


    def parse_statement(self):
        while self.check(TK_LINEBREAK):
            self.advance()
        if self.check(TK_RESERVED) and self.current_token.value == 'hingterb':
            return self.parse_thing_def()
        if self.check(TK_RESERVED) and self.current_token.value == 'rintperb':
            return self.parse_print()
        if self.check(TK_RESERVED) and self.current_token.value in ('if', 'utifberb'):
            return self.parse_if()
        if self.check(TK_RESERVED) and self.current_token.value == 'atchmerb':
            return self.parse_match()
        if self.check(TK_RESERVED) and self.current_token.value == 'orferb':
            return self.parse_for()
        if self.check(TK_NAME) and self.peek().type == TK_ASSIGN:
            return self.parse_variable()
        return self.parse_expression()
    
    def parse_block(self):
        # assumes we just saw a linebreak before the block
        statements = []
        # skip leading blank lines
        while self.check(TK_LINEBREAK):
            self.advance()
        while (self.current_token and
               not (self.check(TK_RESERVED) and self.current_token.value in ('utifberb', 'lseerb', 'ndeerb')) and
               self.current_token.type != TK_DONE):
            statements.append(self.parse_statement())
            while self.check(TK_LINEBREAK):
                self.advance()
        return BlockNode(statements)
    
    def parse_primary(self):
        node = None
        # Handle unary minus or plus
        if self.check(TK_SUB) or self.check(TK_ADD):
            op = 'MINUS' if self.check(TK_SUB) else 'PLUS'
            self.advance()
            expr = self.parse_primary()
            return UnaryOpNode(op.lower(), expr)  # 'minus' or 'plus'
        # new TypeName [args]
        if self.check(TK_RESERVED) and self.current_token.value == 'ewnerb':
            self.advance()
            type_name = self.expect(TK_NAME).value
            init_args = self.parse_array_expression().elements
            node = NewNode(type_name, init_args)

        elif self.check(TK_L_PAREN):
            self.advance()
            node = self.parse_expression()
            self.expect(TK_R_PAREN)

        elif self.check(TK_L_BRACKET):
            node = self.parse_array_expression()

        elif self.check(TK_NAME) and self.peek() and self.peek().type == TK_L_BRACKET:
            node = self.parse_indexing()

        elif self.check(TK_NAME):
            name = self.current_token.value
            self.advance()
            node = IdentifierNode(name)

        elif self.check(TK_INT) or self.check(TK_FLOAT) or self.check(TK_STRING) or self.check(TK_BOOL):
            node = self.parse_literal()

        else:
            raise Exception(f"Unexpected token in primary: {self.current_token}")

        return self._maybe_parse_attr(node)

    
    def parse_add_sub(self):
        left = self.parse_mul_div()
        # left‐associative + and -
        while self.check(TK_ADD) or self.check(TK_SUB):
            op = self.current_token.value or self.current_token.type
            self.advance()
            right = self.parse_mul_div()
            left = BinaryOpNode(left, op, right)
        return left

    def parse_mul_div(self):
        left = self.parse_primary()
        # left‐associative *, /, %
        while self.check(TK_MUL) or self.check(TK_DIV) or self.check(TK_MOD):  # ADDED TK_MOD
            op = self.current_token.value or self.current_token.type
            self.advance()
            right = self.parse_primary()
            left = BinaryOpNode(left, op, right)
        return left
    
    def parse_for(self):
        # consume 'for'
        self.expect(TK_RESERVED)  # 'orferb'
        # loop variable
        var_name = self.expect(TK_NAME).value
        # consume 'in'
        if not (self.check(TK_RESERVED) and self.current_token.value == 'in'):
            raise Exception(f"Expected 'in', got {self.current_token}")
        self.advance()
        # iterable expression
        iterable = self.parse_expression()

        # ─────── enforce block‐only ───────
        if not self.check(TK_LINEBREAK):
            raise Exception("Expected newline after 'in <iterable>' in for‐loop")
        self.advance()  # skip newline

        body = self.parse_block()

        if not (self.check(TK_RESERVED) and self.current_token.value == 'ndeerb'):
            raise Exception("Expected 'ndeerb' to close 'orferb' block")
        self.advance()

        while self.check(TK_LINEBREAK):
            self.advance()
        # ────────────────────────────────────

        return ForNode(var_name, iterable, body)


    def parse_thing_def(self):
        self.expect(TK_RESERVED)      
        name = self.expect(TK_NAME).value
        while self.check(TK_LINEBREAK):
            self.advance()
        args = []
        while self.check(TK_RESERVED) and self.current_token.value == 'rgaerb':
            self.advance()               # skip 'arg'
            arg_name = self.expect(TK_NAME).value
            args.append(arg_name)
            while self.check(TK_LINEBREAK):
                self.advance()
        if not (self.check(TK_RESERVED) and self.current_token.value == 'ndeerb'):
            raise Exception(f"Expected 'ndeerb', got {self.current_token}")
        self.advance()  # consume 'end'

        return ThingDefNode(name, args)
    
    def _maybe_parse_attr(self, node):
        while self.check(TK_DOT):
            self.advance()
            field = self.expect(TK_NAME).value
            node = AttrAccessNode(node, field)
        return node

    def parse_pattern(self):
        # literal patterns
        if self.check(TK_INT) or self.check(TK_FLOAT) \
           or self.check(TK_STRING) or self.check(TK_BOOL):
            lit = self.parse_literal()  # yields NumberNode, StringNode, or BooleanNode
            return PatternLiteral(lit.value)

        # wildcard _
        if self.check(TK_NAME) and self.current_token.value == '_':
            self.advance()
            return PatternWildcard()

        # variable binding
        if self.check(TK_NAME):
            name = self.current_token.value
            self.advance()
            return PatternVar(name)

        raise Exception(f"Unexpected token in pattern: {self.current_token}")
    
    def parse_match(self):
        self.expect(TK_RESERVED)           # 'match'
        expr = self.parse_expression()
        while self.check(TK_LINEBREAK):
            self.advance()
        cases = []
        if not self.check(TK_RESERVED) or self.current_token.value != 'asecerb':
            raise Exception("Expected at least one 'asecerb' case in 'atchmerb'")
        while self.check(TK_RESERVED) and self.current_token.value == 'asecerb':
            self.advance()                 # skip 'case'
            pattern = self.parse_pattern()
            if not (self.check(TK_RESERVED) and self.current_token.value == 'henterb'):
                raise Exception(f"Expected 'henterb' in case, got {self.current_token}")
            self.advance()

            while self.check(TK_LINEBREAK):
                self.advance()

            if self.check(TK_LINEBREAK):
                body = self.parse_block()
            else:
                body = self.parse_statement()
            cases.append((pattern, body))

            while self.check(TK_LINEBREAK):
                self.advance()

        else_branch = None
        if self.check(TK_RESERVED) and self.current_token.value == 'lseerb':
            self.advance()
            while self.check(TK_LINEBREAK):
                self.advance()

            if self.check(TK_LINEBREAK):
                body = self.parse_block()
            else:
                raise Exception("Expected newline after 'henterb' in case clause")


        if not (self.check(TK_RESERVED) and self.current_token.value == 'ndeerb'):
            raise Exception("Expected 'ndeerb' to close 'atchmerb' block")
        self.advance()


        return MatchNode(expr, cases, else_branch)




