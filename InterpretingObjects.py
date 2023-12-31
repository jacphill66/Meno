class ReturnError(Exception):
    def __init__(self, value):
        self.value = value
        self.type = type(self.value)

class ClassInstance:
    def __init__(self, className, vars):
        self.className = className
        self.vars = vars

class FunctionDeclaration:
    def __init__(self, type, name, params, statments):
        self.type = type
        self.name = name
        self.params = params
        self.statments = statments

class MethodDeclaration:
    def __init__(self, type, name, params, statments):
        self.type = type
        self.name = name
        self.params = params
        self.statments = statments

class StaticMethodDeclaration:
    def __init__(self, className, type, name, params, statments):
        self.className = className
        self.type = type
        self.name = name
        self.params = params
        self.statments = statments
    
class ClassDeclaration:
    def __init__(self, name, constructor, methods, instanceVariables, staticMethods, staticVariables):
        self.name = name
        self.constructor = constructor
        self.methods = methods
        self.staticMethods = staticMethods
        self.instanceVariables = instanceVariables
        self.staticMethods = staticMethods
        #self.staticVariables = staticVariables
        self.staticVariabless = {}