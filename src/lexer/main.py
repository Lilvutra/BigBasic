from parser import Parser
from lexer import Lexer
from interpreter import Interpreter
from interpreter import RuntimeError as InterpreterError

from token import (
    Token,
    TK_ADD, TK_SUB, TK_ASSIGN, TK_LESS, TK_MORE,
    TK_L_PAREN, TK_R_PAREN, TK_L_BRACKET, TK_R_BRACKET,
    TK_FLOAT, TK_INT, TK_STRING, TK_NAME, TK_RESERVED,
    TK_SEP, TK_LINEBREAK, TK_DONE, TK_BOOL, TK_EQEQ, TK_NEQ,
    TK_MUL, TK_DIV, TK_MOD,
    RESERVED_WORDS
)

def run_test(name, code):
    print(f"\n---- {name} ----")
    print("Code:")
    print(code.strip())
    lexer = Lexer("test.src", code)
    tokens = lexer.tokenize()
    interpreter = Interpreter()

    print("\nTokens:")
    for t in tokens:
        print(t)

    parser = Parser(tokens)
    ast = parser.parse()
    print("\nAST:")
    print(ast)
    print("\n--- EXECUTING ---")
    try:
       interpreter.interpret(ast)
    except Exception as e:
       print(f"Runtime error: {e}")    
    print("\n" + "="*40)

def main():
    tests = [
        ("Comments",
         """
^^ This is a full-line comment
arr = [1, 2, 3] ^^ inline comment
print arr[1]
^^ another comment
print 1 ^^ last comment
         """),

        ("Simple Comparisons",
         """
print 5 < 10
print 10 > 42
         """),

        ("Boolean & Equality",
         """
print true
print false
print 1 == 1
print 2 != 3
         """),

        ("Logical Operators",
         """
print not false
print true and false
print true or false
         """),

        ("Parentheses Grouping",
         """
print (1 < 2) and (2 < 3)
print not (3 > 2)
         """),

        ("Chained butif / else",
         """
if 1 < 0 then print "A"
butif 2 < 1 then print "B"
else print "C"
         """),

        ("Multi-statement Block",
         """
if 1 < 2 then
  print "OK"
  x = [1,2]
  print x[1]
else
  print "NO"
end
         """),

        ("Arithmetic",
"""
print 1 + 1
print 2 - 3 + 5
print (4 + 6) - (2 + 2)
"""),

        ("Multiplicative",
"""
print 2 * 3
print 10 / 2
print 7 % 4          
print 5 + 2 * 3
print (2 + 3) * 4
"""),

        ("For loops", 
     """
^^ Single-statement for
for i in [1,2,3] print i

^^ Block-style for
for j in [4,5,6]
  print j
end
"""),

        ("Thing & New",
"""
thing Position
  arg x
  arg y
end
pos = new Position [100,200]
print pos.x
"""),

        ("Pattern Matching",
"""
x = 1
match x
case 1 then print "one"
case true then print "TRUE"
case _ then print "other"
end

match x
case 1 then print "first"
case _ then print "nope"
end
"""),

        ("Array Indexing",
"""
arr = [10,20,30]
print arr[1]    ^^ should print 10
print arr[3]    ^^ should print 30
"""
        ),

        ("Lazy Evaluation",
"""
^^ We bind y to a division-by-zero thunk,
^^ but we never force it until the last line.

y = 1 / 0        ^^ this creates a Thunk, no error yet
x = [10,20,30]   ^^ also lazy, but elements are simple

print x[3]       ^^ forces only x[3] → prints 30, no error
print y          ^^ now forces y → should raise "Divide by zero"
"""),

        ("Error: Type Mismatch",
"""
print 1 + "a"
"""),

        ("Error: Divide by Zero",
"""
print 1 / 0
"""),

        ("Error: Index Out of Bounds",
"""
x = [10,20,30]
print x[0]    ^^ 0 is invalid (one-based)
print x[4]    ^^ only 1–3 are valid
"""),

        ("Error: Non-boolean in if",
"""
if 123 then print "oops" end
"""),

        ("Error: Non-list in for",
"""
for i in 42 print i
"""),

        ("Error: Undefined Variable",
"""
print missingVar
"""),
    ]

    for name, code in tests:
        run_test(name, code)

if __name__ == "__main__":
    main()
