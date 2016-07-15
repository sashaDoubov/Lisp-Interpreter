# Lisp-Interpreter
This is a Lisp Interpreter written in Python.

It was based on [this](http://norvig.com/lispy.html) fantastic write-up, 
which I had to rely on heavily for procedures and environments. The parsing operation was completely my own. 


How to try it:
Place your lisp contents into the input.txt file
Run it with Python 2.7
(Note: Multi-line statements must be spaced in/indented)

Unfortunately, my idea on how to evaluate the code did not pan out, so I used the lispy approach. 


My original idea was to always find the deepest sublist, evaluate it and then recursively evaluate the rest of the function. 
This works really well for arithmetic statements, but less so for definitions (which don't have any associated value) and for procedures.


With time and further understanding of interpreters, I may revisit this code and see if I can re-write the environment (scope) and procedures.
