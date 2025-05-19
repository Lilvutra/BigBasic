from parser import *
from ast import *

class Thunk:
    def __init__(self, fn):
        self.fn = fn
        self._value = None
        self._forced = False

    def force(self):
        if not self._forced:
            self._value = self.fn()
            self._forced = True
        return self._value

    def __repr__(self):
        if self._forced:
            return f"<Thunk(value={self._value!r})>"
        else:
            return "<Thunk (unevaluated)>"

class RuntimeError(Exception):
    pass

class Interpreter:
    def __init__(self):
        # variable environment: name -> value
        self.env = {}
        # thing definitions: name -> list of arg names
        self.thing_defs = {}

    def interpret(self, program: ProgramNode):
        result = None
        for stmt in program.statements:
            result = self.eval(stmt)
        return result

    def eval(self, node):
        method = f'eval_{type(node).__name__}'
        if not hasattr(self, method):
            raise RuntimeError(f"No eval_{type(node).__name__} method")
        return getattr(self, method)(node)
    
    def _force(self, x):
        if isinstance(x, Thunk):
            return self._force(x.force())
        return x

# -------------------- EVALUATION ---------------------------------

# Program
    def eval_ProgramNode(self, node):
        return self.interpret(node)

# Assign variables
    def eval_AssignmentNode(self, node):
        old_env = self.env.copy()

        def thunk_fn():
            prev_interp = Interpreter()
            prev_interp.env = old_env
            prev_interp.thing_defs = self.thing_defs  
            return prev_interp._force(prev_interp.eval(node.value))

        self.env[node.name] = Thunk(thunk_fn)
        return self.env[node.name]
                

    def eval_IdentifierNode(self, node):
        return Thunk(lambda: (
            self._force(self.env[node.name])
            if node.name in self.env
            else (_ for _ in ()).throw(RuntimeError(f"Undefined variable: {node.name}"))
        ))
    
    def eval_ArrayNode(self, node):
        thunks = [ Thunk(lambda e=e: self._force(self.eval(e))) for e in node.elements ]
        return Thunk(lambda: [self._force(t) for t in thunks])
    
    def eval_IndexNode(self, node):
        return Thunk(lambda: self._eval_index(node))

    def _eval_index(self, node):
        collection = self._force(self.eval(node.expr))
        index = self._force(self.eval(node.index))

        if not isinstance(index, int):
            raise RuntimeError(f"Index must be integer, got {type(index).__name__}")
        if not isinstance(collection, list):
            raise RuntimeError(f"Cannot index non-list: {collection}")

        if index < 1 or index > len(collection):
            raise RuntimeError(f"Index out of bounds: {index} not in [1..{len(collection)}]")

        return collection[index - 1]
    
# Print
    def eval_PrintNode(self, node):
        val = self._force(self.eval(node.expression))
        print(val)
        return val

# If
    def eval_IfNode(self, node):
        val = self._force(self.eval(node.condition))
        # coerce any value to a boolean via truthiness
        truth = bool(val)
        if truth:
            return self._exec_branch(node.then_branch)
        if node.else_branch is not None:
            return self._exec_branch(node.else_branch)
        return None

    def _exec_branch(self, branch):
        if isinstance(branch, BlockNode):
            result = None
            for stmt in branch.statements:
                result = self.eval(stmt)
            return result
        else:
            return self.eval(branch)

# Loop
    def eval_ForNode(self, node):
        iterable = self._force(self.eval(node.iterable))
        if not isinstance(iterable, list):
            raise RuntimeError(f"Type error: orferb-in requires a list, got {type(iterable).__name__}")
        result = None
        for item in iterable:
            self.env[node.var_name] = Thunk(lambda i=item: i)
            result = self._exec_branch(node.body)
        return result

# Struct
    def eval_ThingDefNode(self, node):
        # register the type definition
        if node.name in self.thing_defs:
            raise RuntimeError(f"Redefinition of hingterb {node.name}")
        self.thing_defs[node.name] = node.args
        return None

    def eval_NewNode(self, node):
        return Thunk(lambda: self._eval_new(node))

    def _eval_new(self, node):
        args = [ self._force(self.eval(arg)) for arg in node.init_args ]
        if node.type_name not in self.thing_defs:
            raise RuntimeError(f"Unknown hingterb type: {node.type_name}")
        params = self.thing_defs[node.type_name]
        if len(args) != len(params):
            raise RuntimeError(f"{node.type_name} expects {len(params)} rgaerbs, got {len(args)}")
        obj = {'__type__': node.type_name}
        for k,v in zip(params, args):
            obj[k] = v
        return obj

    def eval_AttrAccessNode(self, node):
        return Thunk(lambda: self._eval_attr(node))

    def _eval_attr(self, node):
        obj = self._force(self.eval(node.obj))
        if not isinstance(obj, dict) or '__type__' not in obj:
            raise RuntimeError(f"Type error: accessing attribute on non-object {obj}")
        if node.attr not in obj:
            raise RuntimeError(f"Unknown attribute '{node.attr}' on {obj['__type__']}")
        return obj[node.attr]

# Pattern matching
    def eval_MatchNode(self, node):
        val = self._force(self.eval(node.expr))
        for pattern, body in node.cases:
            ok, binds = self._match_pattern(pattern, val)
            if ok:
                old_env = self.env.copy()
                for k,v in binds.items():
                    self.env[k] = Thunk(lambda x=v: x)
                result = self._exec_branch(body)
                self.env = old_env
                return result
        if node.else_branch is not None:
            return self._exec_branch(node.else_branch)
        raise RuntimeError(f"No pattern matched value: {val}")

    def _match_pattern(self, pattern, value):
        if isinstance(pattern, PatternWildcard):
            return True, {}
        if isinstance(pattern, PatternLiteral):
            return (value == pattern.value), {}
        if isinstance(pattern, PatternVar):
            return True, {pattern.name: value}
        raise RuntimeError(f"Unknown pattern type: {pattern}")
    
# -------------------- EXPRESSIONS ---------------------------------

# Literals
    def eval_NumberNode(self, node):
        return Thunk(lambda: node.value)

    def eval_StringNode(self, node):
        return Thunk(lambda: node.value)

    def eval_BooleanNode(self, node):
        return Thunk(lambda: node.value)

# Unary
    def eval_UnaryOpNode(self, node):
        return Thunk(lambda: self._eval_unary(node))

    def _eval_unary(self, node):
        val = self._force(self.eval(node.expr))

        if node.op in ('INCRE', 'DECRE'):
            if not isinstance(node.expr, IdentifierNode):
                raise RuntimeError(f"Unary '{node.op}' must be applied to a variable")

            name = node.expr.name
            if name not in self.env:
                raise RuntimeError(f"Undefined variable: {name}")

            current_val = self._force(self.env[name])
            if not isinstance(current_val, (int, float)) or isinstance(current_val, bool):
                raise RuntimeError(f"Unary '{node.op}' requires a number, got {type(current_val).__name__}")

            new_val = current_val + 1 if node.op == 'INCRE' else current_val - 1
            self.env[name] = Thunk(lambda: new_val)
            return new_val

        if node.op == 'not':
            return not bool(val)

        if node.op in ('minus', '-'):
            if not isinstance(val, (int, float)) or isinstance(val, bool):
                raise RuntimeError(f"Unary '-' requires a number, got {type(val).__name__}")
            return -val

        if node.op in ('plus', '+'):
            if not isinstance(val, (int, float)) or isinstance(val, bool):
                raise RuntimeError(f"Unary '+' requires a number, got {type(val).__name__}")
            return +val

        raise RuntimeError(f"Unknown unary operator: {node.op}")

# Binary
    def eval_BinaryOpNode(self, node):
        return Thunk(lambda: self._eval_binary(node))

    def _eval_binary(self, node):
        op = node.op

        if op == 'and':
            left = self._force(self.eval(node.left))
            if not isinstance(left, bool):
                raise RuntimeError(f"'and' requires booleans, got {type(left).__name__}")
            if not left:
                return False  # skip right
            right = self._force(self.eval(node.right))
            if not isinstance(right, bool):
                raise RuntimeError(f"'and' requires booleans, got {type(right).__name__}")
            return right

        if op == 'or':
            left = self._force(self.eval(node.left))
            if not isinstance(left, bool):
                raise RuntimeError(f"'or' requires booleans, got {type(left).__name__}")
            if left:
                return True  # skip right
            right = self._force(self.eval(node.right))
            if not isinstance(right, bool):
                raise RuntimeError(f"'or' requires booleans, got {type(right).__name__}")
            return right

        left = self._force(self.eval(node.left))
        right = self._force(self.eval(node.right))

        if isinstance(left, Thunk) or isinstance(right, Thunk):
            raise RuntimeError("Internal error: binary operands must not be thunks")

        if op in ('+', 'PLUS'):
            if not (isinstance(left, (int, float)) and not isinstance(left, bool)):
                raise RuntimeError(f"'+' requires numbers, got {type(left).__name__}")
            if not (isinstance(right, (int, float)) and not isinstance(right, bool)):
                raise RuntimeError(f"'+' requires numbers, got {type(right).__name__}")
            return left + right

        if op in ('-', 'MINUS'):
            if not (isinstance(left, (int, float)) and not isinstance(left, bool)):
                raise RuntimeError(f"'-' requires numbers, got {type(left).__name__}")
            if not (isinstance(right, (int, float)) and not isinstance(right, bool)):
                raise RuntimeError(f"'-' requires numbers, got {type(right).__name__}")
            return left - right

        if op in ('*', 'MUL'):
            if not (isinstance(left, (int, float)) and not isinstance(left, bool)):
                raise RuntimeError(f"'*' requires numbers, got {type(left).__name__}")
            if not (isinstance(right, (int, float)) and not isinstance(right, bool)):
                raise RuntimeError(f"'*' requires numbers, got {type(right).__name__}")
            return left * right

        if op in ('/', 'DIV'):
            if not (isinstance(left, (int, float)) and not isinstance(left, bool)):
                raise RuntimeError(f"'/' requires numbers, got {type(left).__name__}")
            if not (isinstance(right, (int, float)) and not isinstance(right, bool)):
                raise RuntimeError(f"'/' requires numbers, got {type(right).__name__}")
            if right == 0:
                raise RuntimeError("Division by zero")
            return left / right

        if op in ('%', 'MOD'):
            if not (isinstance(left, int) and not isinstance(left, bool)):
                raise RuntimeError(f"'%' requires integers, got {type(left).__name__}")
            if not (isinstance(right, int) and not isinstance(right, bool)):
                raise RuntimeError(f"'%' requires integers, got {type(right).__name__}")
            if right == 0:
                raise RuntimeError("Modulo by zero")
            return left % right

        raise RuntimeError(f"Unknown binary operator: {op}")


# Comparison
    def eval_ComparisonNode(self, node):
        return Thunk(lambda: self._eval_comparison(node))

    def _eval_comparison(self, node):
        left = self._force(self.eval(node.left))
        right = self._force(self.eval(node.right))
        op = node.op

        if isinstance(left, Thunk) or isinstance(right, Thunk):
            raise RuntimeError("Internal error: unforced thunk in comparison")

        if op in ('==', 'EQEQ'):
            return left == right
        if op in ('!=', 'NEQ'):
            return left != right

        if type(left) != type(right):
            raise RuntimeError(f"Cannot compare {type(left).__name__} and {type(right).__name__} with '{op}'")

        if isinstance(left, bool):
            raise RuntimeError(f"Cannot compare booleans with '{op}'")

        if isinstance(left, (int, float)):
            if op in ('<', 'LT'):
                return left < right
            if op in ('>', 'GT'):
                return left > right

        raise RuntimeError(f"Unsupported comparison operator: {op}")

