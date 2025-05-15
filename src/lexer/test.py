# (unchanged imports)
from parser import Parser
from lexer import Lexer
from interpreter import Interpreter
from interpreter import RuntimeError as InterpreterError

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
rintperb arr[1]
^^ another comment
rintperb 1 ^^ last comment
         """),

        ("Simple Comparisons",
         """
rintperb 5 < 10
rintperb 10 > 42

         """),

        ("Boolean & Equality",
         """
rintperb rueterb
rintperb alseferb
rintperb 1 == 1
rintperb 2 != 3
         """),
        
        ("Literals",
         """
a = 5
rintperb a 
rintperb a != 6
_private123 = 20
rintperb 6 + 1.0
rintperb _private123
rintperb "gud"
rintperb 5 ^^add
rintperb -5 ^^add
rintperb "Ferb"
^^my_dict = {"name": "Alice", "age": 25}
^^rintperb my_dict
count = 0
count = "hmm"
rintperb count
lazyDiv = 1/0
rintperb lazyDiv
         """),


("truthy test", 
         """
x = 5
if otnerb 5 henterb
  rintperb "haha"
utifberb 2 < 1 henterb 
  rintperb "B"
lseerb 
  rintperb "C"
ndeerb

         """),   
        
   
        
        ("Unary ops", 
         """
^^ Still hasnt passed unary ops test
a = 5
b = -10
c = True
d = ++a
e = 6

rintperb a
rintperb b 
rintperb e
rintperb d
         """),

 

        ("Logical Operators",
         """
rintperb otnerb alseferb
rintperb rueterb ndaerb alseferb
rintperb rueterb or alseferb
         """),

        ("Parentheses Grouping",
         """
rintperb (1 < 2) ndaerb (2 < 3)
rintperb otnerb (3 > 2)
         """),

        ("Chained butif / else",
         """
if 1 < 0 henterb 
    rintperb "A"
utifberb 2 < 1 henterb 
    rintperb "B"
lseerb 
    rintperb "C"
ndeerb
         """),

        ("Multi-statement Block",
         """
if 1 < 2 henterb
  rintperb "OK"
  x = [1,2]
  rintperb x[1]
lseerb
  rintperb "NO"
ndeerb
         """),

        ("Arithmetic",
         """
rintperb 1 + 1
rintperb 2 - 3 + 5
rintperb (4 + 6) - (2 + 2)
         """),

        ("Multiplicative",
         """
rintperb 2 * 3
rintperb 10 / 2
rintperb 7 % 4          
rintperb 5 + 2 * 3
rintperb (2 + 3) * 4
         """),

        ("For loops", 
         """
^^ Single-statement for
orferb i in [1,2,3] 
  rintperb i
ndeerb

^^ Block-style for
orferb j in [4,5,6]
  rintperb j
ndeerb
         """),

        ("Thing & New",
         """
hingterb Position
  rgaerb x
  rgaerb y
ndeerb
pos = ewnerb Position [100,200]
rintperb pos.x
         """),

        ("Pattern Matching",
         """
x = 1
atchmerb x
asecerb 1 henterb rintperb "one"
asecerb rueterb henterb rintperb "TRUE"
asecerb _ henterb rintperb "other"
ndeerb

atchmerb x
asecerb 1 henterb rintperb "first"
asecerb _ henterb rintperb "nope"
ndeerb
         """),

        ("Array Indexing",
         """
arr = [10,20,30]
rintperb arr[1]    ^^ should print 10
rintperb arr[3]    ^^ should print 30
         """
        ),

        ("Lazy Evaluation",
         """
^^ We bind y to a division-by-zero thunk,
^^ but we never force it until the last line.

y = 1 / 0        ^^ this creates a Thunk, no error yet
x = [10,20,30]   ^^ also lazy, but elements are simple

rintperb x[3]       ^^ forces only x[3] → prints 30, no error
rintperb y          ^^ now forces y → should raise "Divide by zero"
         """),

        ("Error: Type Mismatch",
         """
rintperb 1 + "a"
         """),

        ("Error: Divide by Zero",
         """
rintperb 1 / 0
         """),

        ("Error: Index Out of Bounds",
         """
x = [10,20,30]
rintperb x[0]    ^^ 0 is invalid (one-based)
rintperb x[4]    ^^ only 1–3 are valid
         """),

        ("Error: Non-boolean in if",
         """
if 123 henterb 
  rintperb "oops" ndeerb
         """),

        ("Error: Non-list in for",
         """
orferb i in 42 
  rintperb i
ndeerb
         """),

        ("Error: Undefined Variable",
         """
rintperb missingVar
         """),
        
        ("IDK", 
         """ 
orferb i in [1,2,3]
  rintperb i++
ndeerb
         """)
    ]

    for name, code in tests:
        run_test(name, code)

if __name__ == "__main__":
    main()
