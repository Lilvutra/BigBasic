from lexer import Lexer
from token import TK_DONE

def test_lexer(input_text):
    print(f"--- Input: {input_text} ---")
    lexer = Lexer("test_input", input_text)
    tokens = lexer.tokenize()
    for token in tokens:
        if token.type == TK_DONE:
            print("EOF")
        elif token.value is not None:
            print(f"{token.type}:{token.value}")
        else:
            print(token.type)
    print()

# Example inputs to test
test_lexer("12 + 34")
test_lexer("(5.6 - 2)")
test_lexer("123.45 + (78 - 9.0)")
test_lexer("Hello")
test_lexer(" 'Hello' ")
test_lexer("invalid$chars + 1")
test_lexer('"a string" + "another"')
test_lexer("print input arg end")
test_lexer("1hehe")
test_lexer("hehe1")


# --- Input: 12 + 34 ---
# INT:12
# PLUS
# INT:34
# EOF

# --- Input: (5.6 - 2) ---
# LPAREN
# FLOAT:5.6
# MINUS
# INT:2
# RPAREN
# EOF

# --- Input: 123.45 + (78 - 9.0) ---
# FLOAT:123.45
# PLUS
# LPAREN
# INT:78
# MINUS
# FLOAT:9.0
# RPAREN
# EOF

# --- Input: Hello ---
# IDENTIFIER:Hello
# EOF

# --- Input:  'Hello'  ---
# STRONK:Hello
# EOF

# --- Input: invalid$chars + 1 ---
# IDENTIFIER:invalid
# UNKNOWN:$
# IDENTIFIER:chars
# PLUS
# INT:1
# EOF

# --- Input: "a string" + "another" ---
# STRONK:a string
# PLUS
# STRONK:another
# EOF

# --- Input: print input arg end ---
# KEYWORD:print
# KEYWORD:input
# KEYWORD:arg
# KEYWORD:end
# EOF

# --- Input: 1hehe ---
# INT:1
# IDENTIFIER:hehe
# EOF

# --- Input: hehe1 ---
# IDENTIFIER:hehe1
# EOF