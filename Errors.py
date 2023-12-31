#Add specific errors:
#Uninitialized Variable Error
#Undeclared Error: Undeclared Variables, Methods, Functions, Classs
#Type Error: Variables, Methods, Functions, Params and Args
#Index Error: Strings, Arrays
#Token Error
#Parse Error (Syntax Error)
import abc
from abc import ABC, abstractmethod
class Error(ABC):
    def __init__():
        pass

    def accept(self, visitor):
        pass

    def __repr__(self):
        pass

    def ErrorCheck(self):
        print(self)
        exit()

class LexError(Error):
    def __init__(self, name, message):
        self.name = name
        self.message = message
    
    def __repr__(self):
        return f'Lex Error: {self.name} {self.message}'
    
    def ErrorCheck(self):
        print(self)
        exit()

class ParseError(Error):
    def __init__(self, name, message):
        self.name = name
        self.message = message
    
    def __repr__(self):
        return f'Parse Error: {self.name} {self.message}'
    
    def ErrorCheck(self):
        print(self)
        exit()

class InterpretingError(Error):
    def __init__(self, name, message):
        self.name = name
        self.message = message
    
    def __repr__(self):
        return f'Interpreting Error: {self.name} {self.message}'
    
    def ErrorCheck(self):
        print(self)
        exit()
