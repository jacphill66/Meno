import EnvironmentAndScope, Errors, InterpretingObjects

class Interpreter:

    def __init__(self, statments):
        self.statments = statments
        self.environment = EnvironmentAndScope.Environment()

    def interpret(self):
        for statment in self.statments:
            if statment != None: statment.accept(self)
    
    def interpretStatment(self, statment):
        if statment != None: return statment[0].accept(self)

#######################################################################################################
#Control Flow Interpreting
#######################################################################################################

    #used for evaluating if, else and while statments
    def executeControlFlowStatments(self, controlFlowStatments):
        if controlFlowStatments != None:
            for statment in controlFlowStatments:
                try:
                    statment.accept(self)
                except InterpretingObjects.ReturnError as error:
                    self.environment.closeScope()
                    error2 = InterpretingObjects.ReturnError(error.value)
                    raise error2
    
    #evaluates if and else statment pairs
    def visitIfElseStatment(self, ifElseStatment):
        ifStatment = ifElseStatment.ifStatment
        elseStatments = ifElseStatment.elseStatments
        cond = ifStatment.cond.accept(self)
        self.checkType(cond, bool)
        if cond:
            ifStatment.accept(self)
        else:
            self.environment.openNewScope()
            self.executeControlFlowStatments(elseStatments)
            self.environment.closeScope()
    
    #evaluates if statments
    def visitIfStatment(self, ifStament):
        condition = ifStament.cond.accept(self)
        self.checkType(condition, bool)
        if condition:
            self.environment.openNewScope()
            self.executeControlFlowStatments(ifStament.statments)
            self.environment.closeScope()
    
    #evaluates while statments
    def visitWhileStatment(self, whileStatment):
        condition = whileStatment.cond.accept(self)
        self.checkType(condition, bool)
        scopeOpened = False
        isWhileCalled = False
        while(condition):
            if not scopeOpened: self.environment.openNewScope()
            self.executeControlFlowStatments(whileStatment.statments)
            condition = whileStatment.cond.accept(self)
            scopeOpened = True
        if isWhileCalled: self.environment.closeScope()

#######################################################################################################
#Expression Interpreting
#######################################################################################################

    #evaluates literal floats
    def visitLiteralFloat(self, literalFloat):
        return float(literalFloat.value)

    #evaluates literal integers
    def visitLiteralInteger(self, literalInteger):
        return int(literalInteger.value)
    
    #evaluates literal strings
    def visitLiteralString(self, literalString):
        return str(literalString.value)

    #evaluates literal booleans
    def visitLiteralBoolean(self, literalBoolean):
        return bool(literalBoolean.value)

    #expression helper method (this is really just for type checking)
    def handleBinOp(self, binOp, types):
        left = binOp.left.accept(self)
        self.checkTypeList(types, left)
        right = binOp.right.accept(self)
        self.checkTypeList(types, right)
        return left, right

    #evaluates multiplication expressions
    def visitMultiplicationExpression(self, expression):     
        vals = self.handleBinOp(expression, ['FLOATTYPE', 'INTEGERTYPE'])
        return vals[0]*vals[1]

    #evaluates division expressions
    def visitDivisionExpression(self, expression):
        vals = self.handleBinOp(expression, ['FLOATTYPE', 'INTEGERTYPE'])
        return vals[0]/vals[1]
    
    #evaluates or expressions
    def visitOrExpression(self, expression):
        vals = self.handleBinOp(expression, ['BOOLEANTYPE'])
        return vals[0] or vals[1]

    #evaluates and expressions
    def visitAndExpression(self, expression):
        vals = self.handleBinOp(expression, ['BOOLEANTYPE'])
        return vals[0] and vals[1]
    
    #evaluates mod expressions
    def visitModExpression(self, expression):
        vals = self.handleBinOp(expression, ['FLOATTYPE', 'INTEGERTYPE'])
        return vals[0] % vals[1]

    #evaluates addition expressions
    def visitAdditionExpression(self, expression):
        vals = self.handleBinOp(expression, ['FLOATTYPE', 'INTEGERTYPE'])
        return vals[0] + vals[1]

    #evlautes subtraction expresions
    def visitSubtractionExpression(self, expression):
        vals = self.handleBinOp(expression, ['FLOATTYPE', 'INTEGERTYPE'])
        return vals[0] - vals[1]

    #evaluates equivalence expressions
    def visitEquivalenceExpression(self, expression):
        vals = self.handleBinOp(expression, ['BOOLEANTYPE', 'FLOATTYPE', 'INTEGERTYPE', 'STRINGTYPE'])
        return vals[0] == vals[1]

    #evaluates greater than comparison expressions
    def visitGreaterComparisonExpression(self, expression):
        vals = self.handleBinOp(expression, ['FLOATTYPE', 'INTEGERTYPE'])
        return vals[0] > vals[1]        
    
    #evaluates less than comparison expressions
    def visitLessComparisonExpression(self, expression):
        vals = self.handleBinOp(expression, ['FLOATTYPE', 'INTEGERTYPE'])
        return vals[0] < vals[1]

    #evalutes function declarations
    def visitFunctionDeclaration(self, functionDeclaration):
        self.environment.declareFunction(functionDeclaration.name, 
        InterpretingObjects.FunctionDeclaration(functionDeclaration.type, 
        functionDeclaration.name, 
        functionDeclaration.params, 
        functionDeclaration.statments))

    #evaluates unary expressions
    def visitUnaryOp(self, unaryOp):
        op = unaryOp.op.name
        right = unaryOp.right.accept(self)
        self.checkType(right, bool)
        if op == 'NOT': return not right
    
    #evaluates expression statments
    def visitExpressionStatment(self, expressionStatment):
        #if expressionStatment.exprAST != None: 
        return expressionStatment.exprAST.accept(self)

#######################################################################################################
#Variable And Array Interpreting
#######################################################################################################

    #evaluates variable refrences
    def visitVariableRefrenceStatment(self, variableRefrence):
        instanceOrVariable = self.environment.getInstanceOrVariable2(variableRefrence.name)[0]
        self.checkIfInitialized(variableRefrence.name)
        return instanceOrVariable
    
    #evaluates variable declarations
    def visitVariableDeclarationStatment(self, variableDeclaration):
        val = variableDeclaration.value
        if val!=None: val = val.accept(self)
        type = getattr(self, 'handle'+variableDeclaration.type)()
        if val!=None: self.checkType(val, type)
        self.environment.declareVariable2(variableDeclaration.name, (val, type))

    #evaluates variable assignments
    def visitVariableAssignmentStatment(self, variableAssignment):
        val = variableAssignment.value.accept(self)
        if isinstance(val, InterpretingObjects.ClassInstance):
            instanceName = self.environment.getInstance2(variableAssignment.name)[1]
            self.checkType2(instanceName, val.className)
            self.environment.assignInstance2(variableAssignment.name, (val, val.className))
        elif isinstance(val, list):
            arr1 = self.environment.getVariable2(variableAssignment.name)
            self.checkType(arr1[0], list)
            arr2 = self.environment.getVariable2(variableAssignment.value.name)
            self.checkType2(arr1[1], arr2[1])
            self.environment.assignVariable2(variableAssignment.name, arr2[0])
        else:
            var = self.environment.getVariable2(variableAssignment.name)
            type = var[1]
            self.checkType(val, type)
            self.environment.assignVariable2(variableAssignment.name, val)

    #evaluates array declarations
    def visitArrayDeclaration(self, arrayDeclaration):
        type = getattr(self, 'handle'+arrayDeclaration.type)()
        self.environment.declareVariable2(arrayDeclaration.name, (arrayDeclaration.value, type))
        if arrayDeclaration.thing != None: arrayDeclaration.thing.accept(self)
    
    #array array assignment helper
    def arrayArrayAssignmentHelper(self, name1, name2):
        arr = self.environment.getVariable2(name1)
        self.checkType(arr[0], list)
        arr2 = self.environment.getVariable2(name2)
        self.checkType(arr[0], list)
        if arr[1] != arr2[1]:
            error = Errors.InterpretingError('Array Type Error', name2 + '\'s type does not match: ' + name1)
            error.ErrorCheck()
        self.environment.assignVariable2(name1, arr2[0])
    
    #evaluates an array array assignment (an array being assigned to another array)
    def visitArrayArrayAssignment(self, arrayArrayAssignment):
        self.arrayArrayAssignmentHelper(arrayArrayAssignment.name1, arrayArrayAssignment.name2)

    #assigns an empty array to an array
    def visitEmptyArrayAssignment(self, emptyArrayAssignment):
        arr = self.environment.getVariable2(emptyArrayAssignment.name)
        self.checkType(arr[0], list)
        lst = []
        count = 0
        size = emptyArrayAssignment.size.accept(self)
        self.checkType(size, int)
        while count < size:
            count += 1
            lst.append(None)
        self.environment.assignVariable2(emptyArrayAssignment.name, lst)
    
    #assigns something to an array index
    def visitArrayIndexAssignment(self, assignArrayIndex):
        arr = self.environment.getVariable2(assignArrayIndex.name)
        lst = arr[0]
        self.checkType(lst, list)
        index = assignArrayIndex.index.accept(self)
        self.checkType(index, int)
        element = assignArrayIndex.element.accept(self)
        self.checkType(element, arr[1])
        arr[0][index] = element
        self.environment.assignVariable2(assignArrayIndex.name, arr[0])

#######################################################################################################
#Function Interpreting
#######################################################################################################
    
    #evaluates statments (for functions)
    def evaluateStatments(self, statments, type):
        for statment in statments:
            try:
                statment.accept(self)
            except InterpretingObjects.ReturnError as error:
                if type in ['INTEGERTYPE', 'FLOATTYPE', 'STRINGTYPE', 'BOOLEANTYPE', 'NILTYPE']:
                    if error.value != None:
                        self.checkType2(getattr(self, 'handle' + type)(), error.type)
                    else:
                        self.checkType2(error.type, None)
                    return error.value
    
    #adds a functions params (with the args assigned) to the current scope
    def declareParams(self, params):
        count = 0
        while count < len(params):
            if isinstance(params[count].value, InterpretingObjects.ClassInstance): 
                self.environment.declareInstance2(params[count].name, (params[count].value, params[count].value.className))
            else: self.environment.declareVariable2(params[count].name, (params[count].value, params[count].type))
            count += 1
    
    #evaluates parameters and returns them as a list
    def setParams(self, params, args):
        self.checkNumber(params, args)
        count = 0
        while count < len(params):
            #if params[count].type in ['INTEGERTYPE', 'FLOATTYPE', 'BOOLEANTYPE', 'STRINGTYPE']:
            params[count].value = args[count].accept(self)
            if not isinstance(params[count].value, InterpretingObjects.ClassInstance):
                if getattr(self, 'handle' + params[count].type)() != type(params[count].value):
                    error = Errors.InterpretingError('Param Arg Type Mistmatch', 'Param: ' +str(params[count].name)+ '\'s Type does not match Arg: ' + str(params[count].value) + '\'s Type')
                    error.ErrorCheck()
            else: self.checkType2(params[count].type, params[count].value.className)
            count +=1
        return params
    
    #evaluates a param, old code, probably not nessecary
    def visitParam(self, param):
        return param.name

    #evaluates function calls
    def visitFunctionCall(self, functionCall):
        func = self.environment.getFunction(functionCall.name)
        params = self.setParams(func.params, functionCall.args)
        self.environment.assignTempScopeFunctions()
        self.declareParams(params)
        val = self.evaluateStatments(func.statments, func.type)
        self.environment.handleScopeReassignment()
        return val

    #evalautes substring function calls
    def visitSubstringStatment(self, substringStatment):
        string = self.environment.getVariable2(substringStatment.name)[0]
        self.checkType(string, str)
        startIndex = substringStatment.startIndex.accept(self)
        self.checkType(startIndex, int)
        self.indexCheck(startIndex, len(string))
        endIndex = substringStatment.endIndex.accept(self)
        self.checkType(endIndex, int)
        self.indexCheck(endIndex, len(string))
        return string[startIndex:endIndex]

    #evaluates string insert function calls
    def visitStringInsert(self, stringAssignment):
        index = stringAssignment.index.accept(self)
        self.checkType(index, int)
        initialString = self.environment.getVariable2(stringAssignment.name)[0]
        stringToInsert = stringAssignment.string.accept(self)
        self.checkType(stringToInsert, str)
        finalString = initialString
        self.indexCheck(index, len(initialString))
        if index == len(initialString):
            finalString = initialString + stringToInsert
        else:
            finalString = initialString[0:index] + stringToInsert + initialString[index:len(initialString)]
        return finalString
    
    #evaluates len function calls
    def visitLen(self, string):
        stringOrArray = self.environment.getVariable2(string.name)[0]
        if not(isinstance(stringOrArray, list) or isinstance(stringOrArray, str)):
            error = Errors.InterpretingError('Indexing Error','Only strings and arrays are indexable')
            error.ErrorCheck()
        self.checkIfInitialized(stringOrArray)
        return len(stringOrArray)

    #evaluates get function calls
    def visitGet(self, string):
        stringOrArray = self.environment.getVariable2(string.name)[0]
        index = string.index.accept(self)
        self.checkType(index, int)
        self.indexCheck(index+1, len(stringOrArray))
        return stringOrArray[index]

#######################################################################################################
#Class and Method Interpreting
#######################################################################################################
    
    #evaluates a "class function call" basically, a static method. Not yet fully implemeneted.
    def classFunctionCall(self, functionCall):
        func = self.environment.getClassFunction(functionCall.name)
        classs = self.environment.getClass(functionCall.className)
        params = self.setParams(func.params, functionCall.args)
        self.environment.assignTempScopeFunctions()
        self.declareParams(params)
        val = self.evaluateStatments(func.statments, func.type)
        self.environment.handleScopeReassignment()
        return val

    #evaluates a class declaration
    def visitClassDeclaration(self, classDeclaration):
        self.environment.declareClass(classDeclaration.name,         
        InterpretingObjects.ClassDeclaration(
        classDeclaration.name, 
        classDeclaration.constructor, 
        classDeclaration.methods, 
        classDeclaration.instanceVariables, 
        classDeclaration.staticMethods))

    #evaluates static variables not yet implemented
    def handleStaticVariables(self, staticVariables):
        for var in staticVariables:
            var.accept(self)

    #evaluates instance variables, static variables not yet implemented
    def handleInstanceAndStaticVariables(self, instanceVariables, staticVariables):
        for var in instanceVariables:
            var.accept(self)

    #handles constructor args
    def handleConstructorArgs(self, params):
        self.declareParams(params)

    #handles constructor statments
    def handleConstructorStatments(self, constructor):
        for statment in constructor.statments:
            statment.accept(self)
    
    #instantiates instances
    def constructInstance(self, instance, classs):
        constructor = classs.constructor
        instanceVariables = classs.instanceVariables
        staticVariables = classs.staticVariables
        params = self.setParams(constructor.params, instance.args)
        self.environment.assignTempScopeClasses()
        #handleStaticVariables
        #self.environment.openNewScope()
        self.handleInstanceAndStaticVariables(instanceVariables, staticVariables)
        self.environment.openNewScope()
        self.handleConstructorArgs(params)
        self.handleConstructorStatments(constructor)
        self.environment.closeScope()
        argsAndInstances = self.environment.saveVarsAndInstances()
        #self.environment.closeScope()
        #self.environment.updateStaticVariables()
        self.environment.reassignScopeClasses()
        return argsAndInstances

    #helps with assigning and declaring instances
    def assignmentAndDeclarationHelper(self, classInstance):
        if classInstance.instance != None:
            vars = self.constructInstance(classInstance.instance, self.environment.getClass(classInstance.instance.className))
            classInstance.instance.vars = vars
            return InterpretingObjects.ClassInstance(classInstance.instance.className, vars)
        else: return None

    #evaluates instance declarations
    def visitInstanceDeclarationStatment(self, classInstance):
        if isinstance(classInstance.instance, str):
            instance = self.environment.getInstance2(classInstance.instance)[0]
            self.checkType2(classInstance.className, instance.className)
            self.environment.declareInstance2(classInstance.name, (instance, classInstance.className))
        else:
            instance = self.assignmentAndDeclarationHelper(classInstance)
            if classInstance.instance != None: self.checkType2(classInstance.className, instance.className)
            self.environment.declareInstance2(classInstance.name, (instance, classInstance.className))
    
    #evaluates instance assignments
    def visitInstanceAssignmentStatment(self, classInstance):
        instance = self.assignmentAndDeclarationHelper(classInstance)
        self.checkType2(instance.className, self.environment.getInstance2(classInstance.name)[1])
        self.environment.assignInstance(classInstance.name, (instance, classInstance.className))

    #evaluates instance method calls
    def visitInstanceMethod2(self, instanceMethod):
        #add the classes static variables to the current scope
        if instanceMethod.instance == None: None
        elif isinstance(instanceMethod.instance, str): instance = self.environment.getInstance2(instanceMethod.instance)[0]
        else: instance = instanceMethod.instance.accept(self)
        className = instance.className
        method = self.environment.getMethod(instanceMethod.methodCall, className)
        params = self.setParams(method.params, instanceMethod.args)
        self.environment.assignTempScopeClasses()
        self.environment.addVarsToCurrentScope(instance.vars)
        val = self.executeMethod(params, method.statments, method.type)
        if self.environment.outerScopeIsNone():
            vars = self.environment.saveVarsAndInstances()
            instance.vars = vars
        self.environment.closeScope()
        if self.environment.current_scope == None:
            self.environment.reassignScopeClasses()
        self.checkMethodReturn(val, method.type)
        return val

    #checks the type of the returned value matches the type of the method
    def checkMethodReturn(self, val, methodType):
        #add to functions?
        if val == None: return
        if isinstance(val, InterpretingObjects.ClassInstance): 
            if val.className == methodType: return
        if type(val) == getattr(self, 'handle'+methodType)(): return
        error = Errors.InterpretingError('Type Error:', 'Var: ' + str(type(val)) + ' should be: ' + str(methodType))
        error.ErrorCheck()

    #evaluates a class instance
    def visitClassInstance(self, classInstance):
        classs = self.environment.getClass(classInstance.className)
        vars = self.constructInstance(classInstance, classs)
        return InterpretingObjects.ClassInstance(classInstance.className, vars)

    def visitMethodCall(self, methodCall):
        None
    
    #evaluates a this refrence statment
    def visitThisRefrenceStatment(self, this):
        #implement
        this.thing.accept(self)

    #executes a method (helper method)
    def executeMethod(self, params, statments, type):
        self.declareParams(params)
        val = self.evaluateStatments2(statments, type)
        return val
    
    #evaluates a methods statments
    def evaluateStatments2(self, statments, type):
        for statment in statments:
            try:
                statment.accept(self)
            except InterpretingObjects.ReturnError as error:
                return error.value

#######################################################################################################
#Miscellaneous Interpreting Methods
#######################################################################################################

    def visitEndStatment(self, EndStatment):
        return None
    
    #evaluates a return statment
    #note this code is my own but the idea of throwing an error is from Robert Nystrom in his book: Crafting Interpreters
    #https://craftinginterpreters.com/contents.html
    def visitReturnStatment(self, returnStatment):
        result = returnStatment.value.accept(self)
        error = InterpretingObjects.ReturnError(result)
        raise error
    
    #evaluates a print statment
    def visitPrintStatment(self, printStmnt):
        val = printStmnt.value.accept(self)
        print(val)

#######################################################################################################
#Error Checking Methods
#######################################################################################################
    #checks if a type is in a list of acceptable types
    def checkTypeList(self, allowedTypes, val):
        b = False
        for type in allowedTypes:
            if isinstance(val, getattr(self, 'handle'+type)()):
                b = True
                break
        if not b:
            print('val')
            print(val)
            error = Errors.InterpretingError('c', 'c')
            error.ErrorCheck()
    
    #checks if a types are the same
    def checkType2(self, type1, type2):
        if type1 != type2:
            error = Errors.InterpretingError('Type Error:', 'Var: ' + str(type1) + ' should be: ' + str(type2))
            error.ErrorCheck()

    #checks if a var is of a certain type
    def checkType(self, var, type):
        if not isinstance(var, type):
            error = Errors.InterpretingError('Type Error:', 'Var: ' + str(var) + ' should be: ' + str(type))
            error.ErrorCheck()

    #checks if two lists are the same size (for things like args and params)
    def checkNumber(self, list1, list2):
        if len(list1) != len(list2):
            error = Errors.InterpretingError('Mistmatching Number of Args and Params:', str(list1))
            error.ErrorCheck()

    #checks if a variable is initialized
    def checkIfInitialized(self, var):
        if(var == None):
            error = Errors.InterpretingError('Uninitialized Variable:', str(var))
            error.ErrorCheck()
    
    #checks if an index is within bounds
    def indexCheck(self, index, len):
        if index > len and index >= 0:
            error = Errors.InterpretingError('Index Out Of Bounds:', index)
            error.ErrorCheck()

#######################################################################################################
#Handling Methods
#######################################################################################################

    #helper methods for type checking
    def handleFLOATTYPE(self):
        return float
    def handleINTEGERTYPE(self):
        return int
    def handleBOOLEANTYPE(self):
        return bool
    def handleSTRINGTYPE(self):
        return str
    def handleNAME(self):
        return ''
    def handleNILTYPE(self):
        error = Errors.InterpretingError('Nil Functions Cannot Return Values', '')
        error.ErrorCheck()