# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 23:58:07 2018

@author: Borislav
"""

"""
Implement the grammar for propositional logic with all non terminals as objects


Formula - 

    generate truth table - put it into a class
    prove theorem - for a set of formulas, if all of them are true, then the theorem is true
                    set of formulas  O   theorem, use sematic tableux to close all branches
    
    
    semantic tableux
    SAT solver - given a list of formulas find all possible combinations of atomic propositions that satisfy them 

Parser - fix the parser, some problems with recursion

CLI

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
    
    
    
left = [Negation(Atom("A"))]
right = [Negation(Atom("B"))]
    
st =  SemanticTableaux(left, right)
st.expand()
    
    
    



