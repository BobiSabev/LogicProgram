# -*- coding: utf-8 -*-
"""
Created on Sat Mar 17 11:22:48 2018

@author: Borislav
"""

class Parent(object):
    
    def __init__(self):
        self.parent_var = "This is parent var"
        
class Parent2(object):
    
    def __init__(self):
        self.parent_var2 = "This is the second parent"
        
        
class Child(Parent):
    
    def __init__(self):
        Parent.__init__(self)
        Parent2.__init__(self)
        
    def printParent(self):
        print(self.parent_var)
        print(self.parent_var2)
        
        


c = Child()
c.printParent()