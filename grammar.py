# -*- coding: utf-8 -*-
"""
@author: Borislav Sabev
@date: 17 Mar 2018
"""

import abc


"""
Abstract classes
"""
class LogicExpression(metaclass=abc.ABCMeta):
    """
    An abstract class for all loical expressions in the grammar to be derived from
    """

    @abc.abstractmethod
    def evaluate(self, dictionary):
        """ 
        Evaluate a logical expression given truth assignments for all automic propositions
        
        dictionary - dictionary with key being the name of the atomic proposition
                            and value - its truth assignment
        """
        pass

    'Make a string representation of the object'
    @abc.abstractproperty
    def toString(self):
        pass
    
    
class TwoArgFormula(LogicExpression, metaclass=abc.ABCMeta):
    """
    A common abstract class for all formulas with 2 arguments
    Derived from LogicExpression
    
    initialized with 2 arguments and a symbol of the given formula
    Example: A -> B, 
        arg1 = Atomic("A"), arg2 = Atomic("B"), symbol = ImplicationSymbol()
    """
    
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
    """
    A common abstract class for all formulas with 1 argument
    Derived from LogicExpression
    
    initialized with an argument and a symbol of the given formula
    Example: ~A, 
        arg1 = Atomic("A"), symbol = NegationSymbol()
    """
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
        
        
class Symbol(metaclass=abc.ABCMeta):
    """
    An abstact class for all symbols 
    
    initialized with the names of the symbol classes and their string representation
    Extends LogicExpression with the apply method, which applies a symbol to 
    evaluate or reduce a logical expression
    """
        
    @abc.abstractmethod
    def toString(self):
        pass
    
    @abc.abstractmethod
    def apply(self, args):
        """
        For a list of arguments 1 or 2 apply the symbol on them
        """
        pass
    

"""
Logical operators
"""

class Equivalence(TwoArgFormula):
    """Logical equivalence with 2 LogicExpression argument"""
    def __init__(self, arg1, arg2):
        super(Equivalence, self).__init__(arg1, arg2, EquivalenceSymbol())
        
class Implication(TwoArgFormula):
    """Logical implication with 2 LogicExpression argument"""
    def __init__(self, arg1, arg2):
        super(Implication, self).__init__(arg1, arg2, ImplicationSymbol())
          
class Conjunction(TwoArgFormula):
    """Logical conjunction with 2 LogicExpression argument"""
    def __init__(self, arg1, arg2):
        super(Conjunction, self).__init__(arg1, arg2, ConjunctionSymbol())
    
class Disjunction(TwoArgFormula):
    """Logical disjunction with 2 LogicExpression argument"""
    def __init__(self, arg1, arg2):
        super(Disjunction, self).__init__(arg1, arg2, DisjunctionSymbol())
    
class Negation(OneArgFormula):
    """Logical negation with 2 LogicExpression argument"""
    def __init__(self, arg):
        super(Negation, self).__init__(arg, NegationSymbol())
    
    
"""
Symbols
"""
class EquivalenceSymbol(Symbol):
    """
    A class that handles equivalence:
        toString - how to print it
        apply - how to be applied to 2 arguments
    """
    def toString(self):
        return '<->'
    
    def apply(self, a, b):
        return (a and b) or ((not a) and (not b))

class ImplicationSymbol(Symbol):
    """ A class that handles implication"""
    def toString(self):
        return '->'
    
    def apply(self, a, b):
        return (not a) or b
        
class ConjunctionSymbol(Symbol):
    """ A class that handles conjunction"""
    def toString(self):
        return '/\\'
    
    def apply(self, a, b):
        return a and b

class DisjunctionSymbol(Symbol):
    """ A class that handles disjunction"""
    def toString(self):
        return '\\/'
    
    def apply(self, a, b):
        return a or b

class NegationSymbol(Symbol):
    """ A class that handles negation"""
    def toString(self):
        return '~'
    
    def apply(self, a):
        return not a
        

class Atom(LogicExpression):
    """
    Atomic proposition, meant to replace letter, digit or character in the grammar
    with single string
    """
    def __init__(self, name):
        self.__name = name
    
    def toString(self):
        return self.__name
    
    def evaluate(self, dictionary):
        if dictionary is not None:
            for key, value in dictionary.items():
                if key == self.__name:
                    return value
        return None
    
    def isAtomic(e):
        """ Check if a given LogicExpression is an Atom """
        return e.__class__.__name__ == 'Atom'
    
    
    

        
        
        
        
        
        