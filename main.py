# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 23:58:07 2018

@author: Borislav
"""

"""
Implement the grammar for propositional logic with all non terminals as objects


Formula - 
    generate truth table
    prove theorem
    semantic tableux
    SAT solver   

Parser

CLI

Logical_Expression - abstact base class
    eval
    toString
    generate truth table
    
    

"""

from pyparsing import nestedExpr
 
from grammar import *
from grammar import Value



es = [Equivalence(Implication(Negation(Atom("A")), Atom("B")),Implication(Atom("A"), Atom("B"))),
      Implication(Atom("A"), Atom("B")),
      Conjunction(Atom("A"), Atom("B")),
      Disjunction(Atom("A"), Atom("B")),
      Negation(Atom("A"))]

for e in es:
    print(e.toString())
    print(e.evaluate({'A':True,'B':False}))
    
    
    



