import Errors

class Scope:
    def __init__(self, outerScope):
        self.variableBindings = {}
        self.instanceBindings = {}
        self.outerScope = outerScope
        self.innerScope = None
    
    def printVariables(self):
        curr_scope = self
        count = 0
        while curr_scope != None:
            print(curr_scope.variableBindings)
            curr_scope = curr_scope.outerScope
            count += 1
    
    def removeInnerScope(self):
        self.innerScope = None

    def getOuterScope(self):
        return self.outerScope

    def addInnerScope(self, innerScope):
        self.innerScope = innerScope
    
    def assignVariable2(self, name, val):
        if name in self.variableBindings:
            self.variableBindings[name] = (val, self.variableBindings[name][1])
        elif self.outerScope!=None: return self.outerScope.assignVariable2(name, val)
        else: 
            error = Errors.InterpretingError('Undeclared Variable Error:', 'Unable to assign Var: ' + name + ', it is undeclared')
            error.ErrorCheck()
        
    def getVariable2(self, name):
        if name in self.variableBindings:
            return self.variableBindings[name]
        elif self.outerScope!=None: return self.outerScope.getVariable2(name)
        else:             
            error = Errors.InterpretingError('Undeclared Variable Error:', 'Unable to retrieve Var: ' + name + ', it is undeclared')
            error.ErrorCheck()

    def declareVariable2(self, name, thingType):
        self.variableBindings.update({name: thingType})#fix variable.value thingy?
    
    def getInstanceOrVariable2(self, name):
        if name in self.instanceBindings: 
            return self.instanceBindings[name]
        elif name in self.variableBindings:
            return self.variableBindings[name]
        elif self.outerScope!=None: return self.outerScope.getInstanceOrVariable2(name)
        else:
            self.printVariables()
            error = Errors.InterpretingError('Undeclared Instance or Variable Error:', 'Var: ' + name + ' is undeclared')
            error.ErrorCheck()

    def declareInstance2(self, name, instance):
        self.instanceBindings.update({name: instance})

    def getInstance2(self, name):
        if name in self.instanceBindings: 
            return self.instanceBindings[name]
        elif self.outerScope!=None: return self.outerScope.getInstance2(name)
        else:             
            error = Errors.InterpretingError('Undeclared Instance Error:', 'Var: ' + name + ' is undeclared')
            error.ErrorCheck()

    def assignInstance2(self, name, instance):
        if name in self.instanceBindings: 
            self.instanceBindings[name] = instance
        elif self.outerScope!=None: return self.outerScope.assignInstance2(name, instance)
        else: 
            error = Errors.InterpretingError('Undeclared Instance Error:', 'Var: ' + name + ' is undeclared')
            error.ErrorCheck()

class Environment:
    def __init__(self):
        self.global_scope = Scope(None)
        self.current_scope = self.global_scope
        self.tempScope = None
        self.classBindings = {}
        self.functionBindings = {}
        self.scopeStack = []
        self.instanceStack = []

    def printVariables(self):#for testing
        self.current_scope.printVariables()

    def openNewScope(self):
        #print('New Scope Opened')
        self.current_scope = Scope(self.current_scope)
        self.current_scope.getOuterScope().addInnerScope(self.current_scope)

    def closeScope(self):
        self.current_scope = self.current_scope.getOuterScope()
        if self.current_scope != None:
            self.current_scope.removeInnerScope()
        else:
            None
            #print('current_scope is None!')
    
    def traverseOuterScopes(self):
        tScope = self.current_scope
        print(tScope)
        while tScope != None:
            tScope = tScope.outerScope
            print(tScope)

    def assignTempScope(self):
        #print('new temp scope has been assigned')
        #tempscope should be None
        self.tempScope = self.current_scope
        self.current_scope = Scope(None)
    
    def reassignScope(self):
        #print('called reassign scope')
        #current_scope should be None
        self.current_scope = self.tempScope
        self.tempScope = None

    #def closeTempScope(self):
        #self.current_scope = self.tempScope
        #self.tempScope = None
    #close all temp scopes method?
    
    def declareFunction(self, name, func):
        self.functionBindings.update({name: func})

    def getFunction(self, name):
        if name in self.functionBindings: return self.functionBindings[name]
        #elif self.outerScope!``=None: return self.outerScope.getVariable(name)#for later implementation
        else:             
            error = Errors.InterpretingError('Undeclared Function Error:', 'Function: ' + name + ' is undeclared')
            error.ErrorCheck()

    def declareClass(self, name, classs):
        self.classBindings.update({name: classs})

    def getClass(self, name):
        if name in self.classBindings: return self.classBindings[name]
        #elif self.outerScope!``=None: return self.outerScope.getVariable(name)#for later implementation
        else:
            error = Errors.InterpretingError('Undeclared Class Error:', 'Class: ' + name + ' is undeclared')
            error.ErrorCheck()

    def declareInstance(self, name, instance):
        self.current_scope.declareInstance(name, instance)
    
    def getInstance(self, name):
        return self.current_scope.getInstance(name)

    def assignInstance(self, name, instance):
        self.current_scope.assignInstance(name, instance)
    
    def getMethod(self, methodName, className):
        methods = self.getClass(className).methods
        if methodName in methods: return methods[methodName]
        else:
            None
            #error
    
    def getClassFunction(self, functionName, className):
        functions = self.getClass(className).functions
        if functionName in functions: return functions[functionName]
        else:
            None
            #error

    def saveVarsAndInstances(self):
        vars = self.current_scope.variableBindings
        instances = self.current_scope.instanceBindings
        return vars, instances
    
    def addVarsToCurrentScope(self, vars):
        self.current_scope.variableBindings.update(vars[0])
        self.current_scope.instanceBindings.update(vars[1])
    
    def printInstanceBindings(self):
        print(self.current_scope.instanceBindings)

    def outerScopeIsNone(self):
        if self.current_scope!=None:
            return self.current_scope.getOuterScope() == None
    
    def getInstanceOrVariable(self, name):
        return self.current_scope.getInstanceOrVariable(name)
    
    def reassignScopeClasses(self):
        #is this line nessecary?
        self.current_scope = None
        self.current_scope = self.scopeStack.pop()
    
    def assignTempScopeClasses(self):
        self.scopeStack.append(self.current_scope)
        self.current_scope = Scope(None)

    def getGlobalScope(self):
        globalScopeInnerScope = self.global_scope.innerScope

    def assignTempScopeFunctions(self):
        self.scopeStack.append(self.current_scope)
        self.current_scope = Scope(None)
        self.current_scope.outerScope = self.global_scope

    def reassignScopeFunctions(self):
        self.current_scope = None
        self.current_scope = self.scopeStack.pop()
    
    def handleScopeReassignment(self):
        if self.current_scope.outerScope == self.global_scope: self.reassignScopeFunctions()
        else: self.closeScope()

    def declareVariable2(self, name, thingType):
        #declares {name, (thing, type)}
        self.current_scope.declareVariable2(name, thingType)
    
    def getVariable2(self, name):
        #returns (thing, type)
        return self.current_scope.getVariable2(name)

    def assignVariable2(self, name, thing):
        #assigns {name, (thing, type)}
        self.current_scope.assignVariable2(name, thing)
    
    def getInstanceOrVariable2(self, name):
        return self.current_scope.getInstanceOrVariable2(name)
    
    def declareInstance2(self, name, instance):
        self.current_scope.declareInstance2(name, instance)
    
    def getInstance2(self, name):
        return self.current_scope.getInstance2(name)
    
    def assignInstance2(self, name, instance):
        self.current_scope.assignInstance2(name, instance)
    
    def updateStaticVariables(self, className, vars):
        self.classBindings[className].staticVariabless.update(vars)