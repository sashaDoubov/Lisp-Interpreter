import operator as op
import inspect
import sys

import math


 ###### Type declarations
Symbol = str          # A Scheme Symbol is implemented as a Python str
List   = list         # A Scheme List is implemented as a Python list
Number = (int, float) # A Scheme Number is implemented as a Python int or float




###### Parsing

class InvalidSyntax(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
  
# formatLine combines the indented statements into one continuous line
  
def formatLines(contents):

    # new list of lines
    newContents = []
    
    for i in range(len(contents)):
        
        # if there's an indent detected
        if contents[i][0].isspace():
            
            # first line cannot be spaced in (error)
            if i == 0:
                raise InvalidSyntax("Improper Indentation")
             
            # appends it to the previous line
            previousLine = newContents[-1]
            newContents.pop()
            
            newContents .append(previousLine.rstrip('\n') + contents[i]) 
            
        else:
         
            newContents.append(contents[i])
            
    return newContents



# takes the input string and spaces out the brackets
# then splits the string apart, making a list of elements
def tokenize(str):

    elements = str.replace('('," ( ").replace(')'," ) ").split()
    #print elements
    return elements

# provides error checking for the assemble tree function
# outputs repeated lines
def parse(contents):
    tokenizedTrees = []
    
    try:
        # tries to properly format the lines
        contents = formatLines(contents)   
        
    except InvalidSyntax as e:
        
        print "\nSyntax Error on line ", 0,
        print ':\t"{}" ' .format(contents[0])
        print e.value,"\n"
        return -1

    
    for i in range(len(contents)):
    
        line = contents[i]
        
        
        try:
            # parses each line and adds it onto the line
            parsedLine = assembleTree(tokenize(line))    
            tokenizedTrees += parsedLine
            
        except InvalidSyntax as e:
        
            print "\nSyntax Error on line ", i+1,
            print ':\t"{}" ' .format(line[:-1])
            print e.value,"\n"
            return -1
            
    return tokenizedTrees
            

# performs the actual parsing operation
# ex. "(* 5 6 (+ 4 5))"
# becomes [ '*', 5, 6, [ '+', 4 , 5]]    
def assembleTree(elements):

    # bools
    leftBracket = "(" in elements
    rightBracket =  ")" in elements
    
    if (leftBracket and rightBracket):
        
        start = elements.index("(")  + 1 # the next element after the starting parentheses
        
        innerIndex = 0
        endIndex = start
        
        # the idea is to keep track of scope
        # innerIndex must be 0 at the proper closing bracket
        # every additional starting bracket adds to the inner index
        # every additional closing removes 1
        
        for i in range (start,len(elements) - 1):
            if  elements[i] == "(":
            
                innerIndex +=1
                
            elif elements[i] == ")":
            
                if innerIndex == 0:
                    break
                    
                else:
                    innerIndex -= 1
                
            endIndex += 1
          
        subStr = elements[start : endIndex]
        
        del elements[start - 1 : endIndex + 1]
        
        # recursive call on the substring, and the rest of the string
        assembleTree(subStr)
        assembleTree(elements)
        
        # converts elements to token values
        
        for i in range(len((subStr))):
            token = subStr[i]
            if type(token) != list:
                subStr[i] = atom(token)
            
        elements.insert(start - 1,subStr)
        
        return elements
        
    #xor , checks for one of the parentheses to be missing
    elif leftBracket != rightBracket:
        raise InvalidSyntax("Improper Parentheses")
    
    
# gives a value to each item in the tree
# can either be a number (int or float) or a string    
def atom(token):

    try: return int(token)
    
    except ValueError:

        try: return float(token)
    
        except ValueError:
    
            return Symbol(token)         
        
        
###### Environments

# the default symbols used in lisp

def symbolValue():
    env = Env()
    env.update(vars(math)) # sin, cos, sqrt, pi, ...
    env.update({
            # fixed up add, sub, * , / to work with multiple args
            
        '+':  lambda *x: reduce (op.add, list(x)) , 
        '-':  lambda *x: reduce (op.sub, list(x)) , 
        '*':lambda *x: reduce (op.mul, list(x)) ,
        '/': lambda *x: reduce (op.div, list(x)) , 
        '>': op.gt,
        '<':op.lt, 
        '>=':op.ge,
        '<=':op.le, 
        '=':op.eq, 
        'abs':     abs,
        'append':  op.add,  
        'apply':   apply,
        'begin':   lambda *x: x[-1],
        'car':     lambda x: x[0],
        'cdr':     lambda x: x[1:], 
        'cons':    lambda x,y: [x] + y,
        'eq?':     op.is_, 
        'equal?':  op.eq, 
        'length':  len, 
        'list':    lambda *x: list(x), 
        'list?':   lambda x: isinstance(x,list), 
        'map':     map,
        'max':     max,
        'min':     min,
        'not':     op.not_,
        'null?':   lambda x: x == [], 
        'number?': lambda x: isinstance(x, Number),   
        'procedure?': callable,
        'round':   round,
        'symbol?': lambda x: isinstance(x, Symbol),
    })
    return env

# taken from lispy    
class Env(dict):
    "An environment: a dict of {'var':val} pairs, with an outer Env."
    def __init__(self, parms=(), args=(), outer=None):
        self.update(zip(parms, args))
        self.outer = outer
    def find(self, var):
        "Find the innermost Env where var appears."
        return self if (var in self) else self.outer.find(var)
        
global_env = symbolValue()

    
 ###### Procedures
 
 # taken from lispy
class Procedure(object):
    "A user-defined Scheme procedure."
    def __init__(self, parms, body, env):
        self.parms, self.body, self.env = parms, body, env
    def __call__(self, *args): 
        return evaluate(self.body, Env(self.parms, args, self.env))
        
        

 
####### Main Interpretation (evaluation)
def evaluate(x, env = global_env):

    if type(x) == Symbol:                   # variable reference
        return env.find(x)[x]
        
    elif type(x) != List:                       # constant
        return x
     
    elif x[0] == 'if':                             # conditional
        (_, condition, conseq, alt) = x
        
        if (evaluate(condition,env)):
            return evaluate(conseq,env)
        else:
            return evaluate(alt,env)
            
    elif x[0] == 'define':                      # definition
        (_, var ,  expression) = x
        env[var] = evaluate(expression, env)
        
    elif x[0] == 'lambda':                      # procedure
        return  Procedure( x[1] , x[2] , env)
        
    elif x[0] == 'quote':                          # quote
        return x[1:]
    elif x[0] == 'set!':
        (_, var,exp) = x
        env.find(var)[var] = evaluate(exp,env)
    else:                          

        proc = evaluate(x[0], env)              # procedure call
        args = [evaluate(arg, env) for arg in x[1:]]
        return proc(*args)


###### File Operation

def openFileParse(fileName):
        with open(fileName,'r') as file:
            return parse(file.readlines())
            
                 
def interpret(lines):
    for line in lines:
    
        evaluatedValue =  evaluate(line)
        
        if evaluatedValue is not None:
            print evaluatedValue

    
def main():
    if len(sys.argv) == 2:
        fileName = sys.argv[1]
        parsed =  openFileParse(fileName)
        # optionally print the parsed contents
        #print parsed
        interpret(parsed)
    else:
        print "Invalid Command Arguments!"
     
    

   
if __name__ == '__main__':
    main()