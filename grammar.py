# -*- coding: utf-8 -*-
"""
Created on Sat Mar 17 00:13:11 2018

@author: Borislav
"""

import abc


"""
Abstract classes
"""


class LogicExpression(metaclass=abc.ABCMeta):
    'Abstract class for all logical expressions in the grammar'
    
    'Evaluate a logical expression given truth values for all automic propositions'
    @abc.abstractmethod
    def evaluate(self, dictionary):
        pass

    'Make a string representation of the object'
    @abc.abstractproperty
    def toString(self):
        pass
    
    
class TwoArgFormula(LogicExpression, metaclass=abc.ABCMeta):
    
    def __init__(self, arg1, arg2, symbol):
        self.__arg1 = arg1
        self.__arg2 = arg2
        self.__symbol = symbol
        
    def getArg1(self):
        return self.__arg1
    
    def getArg2(self):
        return self.__arg2
    
    def getSymbol(self):
        return self.__symbol
    
    def toString(self):
        return "({} {} {})".format(self.getArg1().toString(),
                                   self.getSymbol().toString(),
                                   self.getArg2().toString())
    
    def evaluate(self, dictionary):
        return self.getSymbol().apply(self.getArg1().evaluate(dictionary), 
                                     self.getArg2().evaluate(dictionary))
        
    
class OneArgFormula(LogicExpression, metaclass=abc.ABCMeta):
    
    def __init__(self, arg, symbol):
        self.__arg = arg
        self.__symbol = symbol
        
    def getArg(self):
        return self.__arg
    
    def getSymbol(self):
        return self.__symbol
    
    def toString(self):
        return "({} {})".format(self.getSymbol().toString(),
                                self.getArg().toString())
    
    def evaluate(self, dictionary):
        return self.getSymbol().apply(self.getArg().evaluate(dictionary))
        
class NoArgFormula(LogicExpression, metaclass=abc.ABCMeta):

    def __init__(self, arg):
        self.arg = arg
        
    def getArg(self):
        return self.arg
    
    
class Symbol(LogicExpression, metaclass=abc.ABCMeta):
    
    def __init__(self):
        self.symbols = {
                        'EquivalenceSymbol' : '<->',
                        'ImplicationSymbol' : '->',
                        'ConjunctionSymbol' : '/\\',
                        'DisjunctionSymbol' : '\\/',
                        'NegationSymbol'    : '~'
                        }
    def toString(self):
        return self.symbols[self.__class__.__name__]
    
    def getSymbols():
        return self.symbols
    
    def evaluate(self, dictionary):
        pass
    
    @abc.abstractmethod
    def apply(self, args):
        pass
    

"""

Logical operators

"""


class Equivalence(TwoArgFormula):
    
    def __init__(self, arg1, arg2):
        super(Equivalence, self).__init__(arg1, arg2, EquivalenceSymbol())
        
class Implication(TwoArgFormula):
    
    def __init__(self, arg1, arg2):
        super(Implication, self).__init__(arg1, arg2, ImplicationSymbol())
          
    
class Conjunction(TwoArgFormula):
    
    def __init__(self, arg1, arg2):
        super(Conjunction, self).__init__(arg1, arg2, ConjunctionSymbol())
    
    
class Disjunction(TwoArgFormula):
    
    def __init__(self, arg1, arg2):
        super(Disjunction, self).__init__(arg1, arg2, DisjunctionSymbol())
    
    
class Negation(OneArgFormula):
    
    def __init__(self, arg):
        super(Negation, self).__init__(arg, NegationSymbol())
    
    
"""
Symbols

"""
class EquivalenceSymbol(Symbol):
    
    def apply(self, a, b):
        return (a and b) or ((not a) and (not b))

class ImplicationSymbol(Symbol):
    
    def apply(self, a, b):
        return (not a) or b
        
class ConjunctionSymbol(Symbol):
    
    def apply(self, a, b):
        return a and b

class DisjunctionSymbol(Symbol):
    
    def apply(self, a, b):
        return a or b

class NegationSymbol(Symbol):
    
    def apply(self, a):
        return not a



' atom or (formula)'
class Value(LogicExpression):
    
    def __init__(self, arg):
        if(type(arg) == str):
            self.letter = arg
            self.isTerminal = True
        else:
            self.formula = arg
            self.isTerminal = False
    
    def toString(self):
        if(self.isTerminal):
            return self.letter
        else:
            return self.formula.toString()
        
        
"atomic proposition - meant to replace letter, subsequent char and so on by just one string"
class Atom(LogicExpression):
    
    def __init__(self, name):
        self.name = name
    
    def toString(self):
        return self.name
    
    def evaluate(self, dictionary):
        if dictionary is not None:
            for key, value in dictionary.items():
                if key == self.name:
                    return value
        return None
    
    def isAtomic(e):
        return e.__class__.__name__ == 'Atom'
    
    
    
from pyparsing import nestedExpr
    
class Parser:
    
    def __init__(self):
        self.input = input("> ")
        if ( not (self.input[0] == "(") or not (self.input[-1] != ")") ):
            self.input = "(" + self.input + ")" # surround with brackets for the function to work
        
        self.EQUIV = '<->'
        self.IMP = '->'
        self.CONJ = '/\\'
        self.DISJ = '\\/'
        self.NEG = '~'
        
      
    def parseBrackets(self):
        return nestedExpr('(',')').parseString(self.input).asList()[0]
    
    def splitBySymbol(self, exp, symb, right_associative=True):
        i = -1
        if symb in exp:
            
            if right_associative:
                i = len(exp) - exp[::-1].index(symb)
            else:
                i = exp.index(symb)
                
        if i == -1: # if no match was found return 0
            return 0
        print(exp[:i])
        print(exp[i:])
        # if there is match return the splitted expression accross the symbol
        return exp[:i], exp[(i+1):]
        
    def parseFormula(self, exp=None):
        
        if exp is None:
            exp = self.parseBrackets()
    
        if type(exp) == str:
            return Atom(exp)
    
    
        exp_2_part = self.splitBySymbol(exp, self.EQUIV, False)
        if exp_2_part:
            return Equivalence(self.parseFormula(exp_2_part[0]), 
                               self.parseFormula(exp_2_part[1]))
        
        exp_2_part = self.splitBySymbol(exp, self.IMP)
        if exp_2_part:
            return Implication(self.parseFormula(exp_2_part[0]), 
                               self.parseFormula(exp_2_part[1]))
        
        exp_2_part = self.splitBySymbol(exp, self.CONJ)
        if exp_2_part:
            return Conjunction(self.parseFormula(exp_2_part[0]), 
                               self.parseFormula(exp_2_part[1]))
        
        exp_2_part = self.splitBySymbol(exp, self.DISJ)
        if exp_2_part:
            return Disjunction(self.parseFormula(exp_2_part[0]), 
                               self.parseFormula(exp_2_part[1]))
        
        """
        exp_2_part = self.splitBySymbol(exp, self.NEG, False)
        if exp_2_part:
            return exp_2_part[0] +  exp_2_part[1])
        """
        
        
        
        """
        Hangle Neg and brackets
        
        """
        
        if type(exp) == list and len(exp) == 1:
            return self.parseFormula(exp[0])
        
        return None
    
from enum import Enum

class Branch(Enum):
    TO_EXPAND = 1
    OPEN = 2
    CLOSED = 3  

class SemanticTableaux:
    """
    A class for managing a semantic tebleaux of a set of formulas
    
    left and right are lists of valid expression
    on the left are meant to be true
    on the right are meant to be false
    branches are either open or closed
    
    putting set of formulas on the left and a theorem on the right and
    closing all branches proves the theorem holds
    """
    
    def __init__(self, left, right):
        self.left = [left]
        self.right = [right]
        self.branches = [Branch.TO_EXPAND]

    """
        Reduction rules, 5 operator x 2 sides = 10 functions 
    """
    
    def expand(self):
        
        while not self.isComplete():
            i_to_expand = [i for i, branch in enumerate(self.branches) if self.branchCanBeExpanded(i)]
            while self.branchCanBeExpanded(i_to_expand[0]):
                # apply reduction rules
                print(self.toString())
                self.notLeft(i_to_expand[0])
                print(self.toString())
                self.notRight(i_to_expand[0])
        
        
        pass
    
    'takes a list of expressions and returns their types as strings'
    def getTypes(exps):
        return [type(e).__name__ for e in exps]
    
    'put the statement on the right, removing the negation'
    def notLeft(self, index):
        types = SemanticTableaux.getTypes(self.left[index])
        if 'Negation' not in types:
            return False # there is no negation so return that it is unsuccesful
        f = self.left[index][types.index('Negation')] # get the formula
        # add the argument of f to the right side
        self.right[index].append(f.getArg())
        self.left[index].remove(f)
        return True
    
    'put the statement on the left, removing the negation'
    def notRight(self, index):
        pass
    
    'Split the disjunction into 2 branches'
    def disjLeft(self, index):
        pass
    
    'Split the disjunction into 2 parts'
    def disjRight(self, index):
        pass
    
    'Split the conjunction to its arguments'
    def conjLeft(self, index):
        pass
    
    'Split the arguments into 2 branches'
    def conjRight(self, index):
        pass
    
    
    'Split to 2 branches, either arg1 on the right, or arg2 on the left'
    def impLeft(self, index):
        pass
    
    'Put arg1 to the left, keep arg2 on the right'
    def impRight(self, index):
        pass
    
    
    'Split into 2 branches, keeping the arguments on the same side'
    def equivLeft(self, index):
        pass
    
    'Split into 2 branches, keeping the arguments on a different side'
    def equivRight(self, index):
        pass
    
    
    'A branch is closed if the same formula occurs on the left and on the right.'
    def branchIsClosed(self, index):
        if(index >= 0 and index < len(self.branches)):
            l = self.left[index]
            r = self.right[index]
            for f_l in l:
                for f_r in r:
                    if f_l.toString() == f_r.toString():
                        self.branches[index] = Branch.CLOSED
                        return True
        return False
    
    'A branch is open if there are no more logical operators and the branch is not closed.'
    def branchIsOpen(self, index):
        # If not valid index
        if(index < 0 or index >= len(self.branches)):
            return False
        
        # If closed
        if self.branchIsClosed(index):
            return False
        
        # If there is a non-atomic formula
        for l,r in zip(self.left[index], self.right[index]):
            if not Atom.isAtomic(l) or not Atom.isAtomic(r):
                return False
        
        self.branches[index] = Branch.OPEN
        return True
        
    
    'If a branch is not closed or open, then it can be expanded'
    def branchCanBeExpanded(self, index):
        return not(self.branchIsClosed(index) or self.branchIsOpen(index)) 
    
    'A tableau is called complete if for all branches is false that they CanBeExpanded'
    def isComplete(self):
        for i, branch in enumerate(self.branches):
            if self.branchCanBeExpanded(i):
                return False
        return True
    
    'A tableau is called closed if it is complete and each branch is closed.'
    def isClosed(self):
        if not self.isComplete():
            return False
        for i, branch in enumerate(self.branches):
            if not self.branchIsClosed(i):
                return False
        return True
    
    'A tableau is called open if it is complete and there is at least one open branch.'
    def isOpen(self):
        if not self.isComplete():
            return False
        for i, branch in enumerate(self.branches):
            if self.branchIsOpen(i):
                return True
        return False
    
    
    def toString(self):
        s = ''
        for formulas_left, formulas_right in zip(self.left, self.right):
            for l in formulas_left:
                s += l.toString() + (", " if not l == formulas_left[-1] else "")
            s += '\t 0 \t'
            for r in formulas_right:
                s += r.toString() + (", " if not r == formulas_right[-1] else "")
            s += "\t\t"
        return s
                



        
            
"""
Generating truth tables .....

"""            

def unlist(exp, l=[]):
    if exp not in l:
        l += [exp]
        
    if type(exp) is Atom:
        return l
    
    if issubclass(type(exp), OneArgFormula):
        unlist(exp.getArg(), l)
        
    
    if(issubclass(type(exp), TwoArgFormula)):
        unlist(exp.getArg1(), l)
        unlist(exp.getArg2(), l) 
    
    return l

def order(exps):
    exp_and_str = []
    # Copy only the expressions that are different
    for e in exps:
        if e.toString() not in [string[0] for string in exp_and_str]:
            exp_and_str.append((e.toString(), e))
    # Order by the length of the string
    exp_and_str.sort(key=lambda tup: len(tup[0])) 
    return exp_and_str    
    
"""
x = unlist(es[0])
print(x)
x_o = order(x)
print(x_o)
"""

def build_dicts(exps):
    # Extract all atomic expression
    atomic = [exp for exp in exps if type(exp[1]) is Atom]
    dicts = []
    # Make a list of dictionaries where atomic expression name is the key
    for i in range(2**len(atomic)):
        # generate truth values
        val = list(bin(i)[2:])
        val = ['0']*(len(atomic)-len(val)) + val
        val = [bool(int(e)) for e in val]
        # create a dictionary of keys
        d = {key[0]:value for key, value in zip(atomic, val)}
        dicts.append(d)
    # and the value is all possible truth table combinations
    return dicts

"""
dicts = build_dicts(x_o)


for e in x_o:
    print(e[0], end="\t")
for d in dicts:
    for e in x_o:
        print(e[1].evaluate(d), end="\t\t\t")
    print()


            
        
        
"""        
        
        
        
        
        
        
        
        