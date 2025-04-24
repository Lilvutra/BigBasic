# The BigBasic Programming Language

Inspired by Small Basic, BigBasic is children-oriented,  simple enough but incorporates more features 

# Getting Started

# A Quick Tour 

Naming 

We are looking for more interesting name ideas buds

# Type Definitions

We offer basic types:

Text = str

Number = (int, float)

List = list

# Tokens

# Pattern matching

# Nested Structs

Object Composition by composing an object by incorporating another object into it and we can directly access 
nested fields using dot notation. So OOP isn't it :)

<pre lang="markdown"><code>
thing Position
	arg x 
	arg y 
end 

thing Sleep 
	arg name 
	arg pos 
end 

pos = new Position [100,200]
s = new Sleep["Bed",pos]

print s.pos.x  ^^ Output: 100
</code></pre>


# Arrays are one-based

<pre lang="markdown"><code>

arr = [1,2,3,4,5]

print arr[1] ^^ return 1 

# Lazy evaluation


