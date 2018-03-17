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
    

x = unlist(es[0])
print(x)
x_o = order(x)
print(x_o)


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


dicts = build_dicts(x_o)


for e in x_o:
    print(e[0], end="\t")
for d in dicts:
    for e in x_o:
        print(e[1].evaluate(d), end="\t\t\t")
    print()


            
        
        
        
        
        
        
        
        
        
        
        