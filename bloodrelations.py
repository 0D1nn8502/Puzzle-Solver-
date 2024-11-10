from z3 import * 
import spacy 
from spacy.matcher import Matcher 

## Some concept of gender : {A given person must have a unique gender} 
## Atomic relations : B is mother
## Then A and B are brothers -> {A and B are male and for some C, Parent(C,A) -> Parent(C,B)} 
##  

a = Bool('A')  
b = Bool('B') 
c = Bool('C') 


Female = Function('Female', BoolSort(), BoolSort()) ## Takes in a variable returns whether True if Male 
Parent = Function('Parent', BoolSort(), BoolSort(), BoolSort()) ## Parent(A,B) : True if A is a parent of B  
Sibling = Function('Sibling', BoolSort(), BoolSort(), BoolSort()) ## Sibling(A,B) : True if A and B are siblings 
Spouse = Function('Spouse', BoolSort(), BoolSort(), BoolSort())  ## Spouse(A,B) : True if A and B are married 
SameGen = Function('SameGen', BoolSort(), BoolSort(), BoolSort()) ## SameGen(A,B) : True if Spouse(A,B) or Sibling(A,B)  


solver = Solver() 



## ATOMIC RELATIONS : Spouse(), Parent(), Sibling()     
## ATOMIC PROPERTIES : Gender 

## Complexer relations 

def MotherInLaw(solver:Solver, A, B):
    C = Bool() 
    solver.add(And(Spouse(C,B), Parent(A,C), Female(a)))    


def FatherInLaw(solver:Solver, A, B): 
    C = Bool() 
    solver.add(And(Spouse(C,B), Parent(A,C), Not(Female(A))))  
    

def Aunt(solver:Solver, A, B): 
    C = Bool() 
    solver.add(And(Parent(C,B), Sibling(C,A), Female(A))) 
    


## Suppose input is given as : A mother in law of B 
## Should be able to create an implicit C s.t. Spouse(C,B) and Parent(A,C) {A is the parent of C} 
