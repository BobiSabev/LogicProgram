# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 23:58:07 2018

@author: Borislav
"""

"""
Grammar:
    - possibly extend to Predicate logic

Tools:
    Parser - fix the parser, some problems with recursion
    SemanticTableux - finish the reduction rules and update for the grammar changes
    Truth tables - collect the functions into a class
    
CLI:
    - make a user interface offering interaction with the program
    
    write forumlas (and rememeber them) - use Parser   
    prove theorem - use the SemanticTableux
    SAT solver - use the SemanticTableux or the truth table

"""

from pyparsing import nestedExpr
 
from grammar import *



es = [Equivalence(Implication(Negation(Atom("A")), Atom("B")),Implication(Atom("A"), Atom("B"))),
      Implication(Atom("A"), Atom("B")),
      Conjunction(Atom("A"), Atom("B")),
      Disjunction(Atom("A"), Atom("B")),
      Negation(Atom("A"))]

for e in es:
    print(e.toString())
    print(e.evaluate({'A':True,'B':False}))
    

#left = [Negation(Atom("A"))]
#right = [Negation(Atom("B"))]   
"""  
left = [Disjunction(Atom("A"), Atom("B"))]
right = [Disjunction(Atom("A"), Atom("B"))]
    
st2 =  SemanticTableaux(left, right)
st2.expand()
    
    
""" 



