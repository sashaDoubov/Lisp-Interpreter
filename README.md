# Lisp Interpreter
This is a Lisp Interpreter written in Python.

It was based on [this](http://norvig.com/lispy.html) fantastic write-up, 
which I had to rely on heavily for procedures and environments. The parsing operation was completely my own. 


**How to use it:**

1. Use a command line with Python 2.7 installed
2. Pass in your input file as a command line argument (ex. python interpreter.py *input.txt*)

(Note: Multi-line statements must be spaced in/indented)


My original idea for evaluation was: 
+ always find the deepest sublist,
+ evaluate it 
+ recursively evaluate the rest of the function 


This works really well for arithmetic statements, but less so for definitions (which don't have any associated value) and for procedures.

Unfortunately, my idea on how to evaluate the code did not pan out, so I used the lispy approach. 





With time and a better understanding of interpreters, I may re-visit this code and see if I can re-write the environment (scope) and procedures.
