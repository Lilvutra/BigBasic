^^ demo

^^ Struct
thing Position
  arg x
  arg y
end

thing Person
  arg name
  arg pos
end

pos1   = new Position [10,20]
person = new Person ["tnqn",pos1]
print person.pos.x    ^^ 10
print person.pos.y    ^^ 20

^^  Variables, Arrays 
arr = [1,2,3,4,5]
print arr[1]          ^^ 1
print arr[5]          ^^ 5

^^ Arithmetic & Comparisons 
a = 1 + 2 * 3         ^^ 7
b = (a - 4) / 2       ^^ 1.5
print a               ^^ 7
print b               ^^ 1.5

print a > 5           ^^ True
print a < 10 and b == 1.5
print not false
print true or false

^^  Condition
if a > 5 then
  print "a>5"
butif a == 7 then print "a==7"
else
  print "other"
end

^^ Loop 
for i in [1,2,3]
  print "i ="
  print i
end

for j in [4,5,6] print j

^^ Pattern matching 
match b
case 1.5 then print "half"
case _   then print "other"
end

^^ Lazy evaluation 
y = 1 / 0             ^^ no error yet
print arr[3]         ^^ forces only arr[3], prints 3
print y              ^^ now forces y → runtime error: Divide by zero
