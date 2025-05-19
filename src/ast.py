# AST Nodes
class ProgramNode:
    def __init__(self, statements):
        self.statements = statements
    def __repr__(self):
        return f"ProgramNode(statements={self.statements})"

# Block
class BlockNode:
    def __init__(self, statements):
        self.statements = statements
    def __repr__(self):
        return f"BlockNode(statements={self.statements})"
    
# Variable assignments
class AssignmentNode:
    def __init__(self, name, value):
        self.name = name
        self.value = value
    def __repr__(self):
        return f"AssignmentNode(name={self.name}, value={self.value})"

class IdentifierNode:
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f"IdentifierNode(name={self.name})"

# Literals
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

class BooleanNode:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"BooleanNode(value={self.value})"

# Array
class ArrayNode:
    def __init__(self, elements):
        self.elements = elements
    def __repr__(self):
        return f"ArrayNode(elements={self.elements})"
    
class IndexNode:
    def __init__(self, expr, index):
        self.expr = expr
        self.index = index
    def __repr__(self):
        return f"IndexNode(expr={self.expr}, index={self.index})"

# Print
class PrintNode:
    def __init__(self, expression):
        self.expression = expression
    def __repr__(self):
        return f"PrintNode(expression={self.expression})"

# If  
class IfNode:
    def __init__(self, condition, then_branch, else_branch=None):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch
    def __repr__(self):
        return f"IfNode(condition={self.condition}, then={self.then_branch}, else={self.else_branch})"

# Loop
class ForNode:
    def __init__(self, var_name, iterable, body):
        self.var_name = var_name
        self.iterable = iterable
        self.body = body
    def __repr__(self):
        return f"ForNode(var={self.var_name}, iterable={self.iterable}, body={self.body})"

# Struct
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

# Expression

## Unary
class UnaryOpNode:
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr
    def __repr__(self):
        return f"UnaryOpNode(op={self.op}, expr={self.expr})"

## Binary
class BinaryOpNode:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
    def __repr__(self):
        return f"BinaryOpNode({self.left} {self.op} {self.right})"

## Comparison
class ComparisonNode:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
    def __repr__(self):
        return f"ComparisonNode({self.left} {self.op} {self.right})"

# Pattern Matching
class MatchNode:
    def __init__(self, expr, cases, else_branch=None):
        # cases: list of (pattern, body_node)
        self.expr = expr
        self.cases = cases
        self.else_branch = else_branch
    def __repr__(self):
        return f"MatchNode(expr={self.expr}, cases={self.cases}, else={self.else_branch})"

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


