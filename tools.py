# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 11:21:11 2018

@author: Borislav
"""

from pyparsing import nestedExpr
from grammar import *
    
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
        
        reduction_rules = [self.notLeft,
                          self.notRight,
                          self.disjLeft,
                          self.disjRight,
                          self.conjLeft,
                          self.conjRight]
        
        
        while not self.isComplete():
            print("Not complete")
            i_to_expand = [i for i, branch in enumerate(self.branches) if self.branchCanBeExpanded(i)]
            
            print("expand branch {}".format(i_to_expand))
            while self.branchCanBeExpanded(i_to_expand[0]):
                # apply reduction rules
                
                
                print(self.toString())
                # for all rules, if their application is successful, output the result
                for rule in reduction_rules:
                    if rule(i_to_expand[0]):
                        print(self.toString())
                
                
            
    
    'takes a list of expressions and returns their types as strings'
    def getTypes(self, exps):
        return [type(e).__name__ for e in exps]
    
    def getFirstExp(self, index, expr_class, left=True):
        if left:
            types = self.getTypes(self.left[index])
        else:
            types = self.getTypes(self.right[index])
        
        if expr_class not in types:
            return None
        
        if left:
            return self.left[index][types.index(expr_class)]
        else: 
            return self.right[index][types.index(expr_class)]
    
    
    def splitBranch(self, index):
        """
        put a second copy of the indexed branch at the end
        """
        if(index >= 0 and index < len(self.branches)):
            self.left.append(self.left[index].copy())
            self.right.append(self.right[index].copy())
            self.branches.append(self.branches[index])       
            
            
    'put the statement on the right, removing the negation'
    def notLeft(self, index):
        f = self.getFirstExp(index, 'Negation', True)
        if f is None: # no expression found
            return False
        # add the argument of f to the right side
        self.right[index].append(f.getArg())
        self.left[index].remove(f)
        return True
    
    'put the statement on the left, removing the negation'
    def notRight(self, index):
        f = self.getFirstExp(index, 'Negation', False)
        if f is None: # no expression found
            return False
        # add the argument of f to the right side
        self.left[index].append(f.getArg())
        self.right[index].remove(f)
        return True
    
    'Split the disjunction into 2 branches'
    def disjLeft(self, index):
        f = self.getFirstExp(index, 'Disjunction', True)
        if f is None:
            return False
        # remove the expanded formula
        self.left[index].remove(f)
        # split the branches, modify index and -1
        self.splitBranch(index)
        # one argument at one branch, other at the other branch
        self.left[index].append(f.getArg1())
        self.left[-1].append(f.getArg2())
        return True
    
    'Split the disjunction into 2 parts'
    def disjRight(self, index):
        f = self.getFirstExp(index, 'Disjunction', False)
        if f is None:
            return False
        # Put the two arguments and remove their disjunction
        self.right[index].append(f.getArg1())
        self.right[index].append(f.getArg2())
        self.right[index].remove(f)
        return True


    """
    Doesn't work from here on
    
    """
    
    'Split the conjunction to its arguments'
    def conjLeft(self, index):
        f = self.getFirstExp(index, 'Conjunction', True)
        if f is None:
            return False
        self.left[index].append(f.getArg1())
        self.left[index].append(f.getArg2())
        self.left[index].remove(f)
        return True
        
        
    'Split the arguments into 2 branches'
    def conjRight(self, index):
        f = self.getFirstExp(index, 'Conjunction', False)
        if f is None:
            return False
        # remove the expanded formula
        self.right[index].remove(f)
        # split the branches, modify index and -1
        self.splitBranch(index)
        # one argument at one branch, other at the other branch
        self.right[index].append(f.getArg1())
        self.right[-1].append(f.getArg2())
        return True
    
    
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
        
        