import ParsingObjects, InterpretingObjects, Errors

class Parse:
    def __init__(self, tokens):
        self.statments = []
        self.tokens = tokens
        self.token_index = 0
        self.current_token = self.tokens[self.token_index]
    
    def advance(self):
        self.token_index +=1
        if self.token_index < len(self.tokens): 
            self.current_token = self.tokens[self.token_index]
        else: self.current_token = None

    def parse(self):
        statment_names = ['CLASS', 'FUNC', 'PRINT', 'INTEGERTYPE', 'NILTYPE', 'STRINGTYPE', 'FLOATTYPE', 'BOOLEANTYPE', 'NAME', 'IF', 'WHILE', 'END']
        while self.current_token != None:
            self.statments.append(self.parseStatment(statment_names))
        return self.statments

    def parseStatment(self, allowedTokens):
        if self.current_token.name in allowedTokens: 
            return getattr(self, 'parse' + self.current_token.name + 'Statment')()
        elif self.current_token.name != 'END':
            return self.parseExpressionStatment()
        else: 
            error = Errors.ParseError('Parsing Error', 'Unable To Parse Statment')
            error.ErrorCheck()   

#######################################################################################################
#Control Flow Parsing
#######################################################################################################

    def parseIFStatment(self):#parse if else statment
        self.checkAndAdvance('IF')
        cond = self.expression()
        self.checkAndAdvance('COLON')
        statments = []
        control_flow_statment_names = ['PRINT', 'INTEGERTYPE', 'STRINGTYPE', 'FLOATTYPE', 'BOOLEANTYPE', 'NAME', 'IF', 'WHILE', 'END', 'RETURN'] 
        while self.current_token.name != 'END':
            statments.append(self.parseStatment(control_flow_statment_names))
        self.checkAndAdvance('END')
        if self.current_token.name == 'ELSE': return self.parseIfElseStatment(ParsingObjects.IfStatment(cond, statments))
        else: return ParsingObjects.IfStatment(cond, statments)

    def parseIfElseStatment(self, ifStatment):
        self.checkAndAdvance('ELSE')
        self.checkAndAdvance('COLON')
        elseStatments = []
        control_flow_statment_names = ['PRINT', 'INTEGERTYPE', 'STRINGTYPE', 'FLOATTYPE', 'BOOLEANTYPE', 'NAME', 'IF', 'WHILE', 'END', 'RETURN'] 
        while self.current_token.name != 'END':
            elseStatments.append(self.parseStatment(control_flow_statment_names))
        self.checkAndAdvance('END')
        return ParsingObjects.IfElseStatment(ifStatment, elseStatments)

    def parseWHILEStatment(self):
        self.checkAndAdvance('WHILE')
        cond = self.expression()
        self.checkAndAdvance('COLON')
        statments = []
        control_flow_statment_names = ['PRINT', 'INTEGERTYPE', 'STRINGTYPE', 'FLOATTYPE', 'BOOLEANTYPE', 'NAME', 'IF', 'WHILE', 'END', 'RETURN']         
        while self.current_token.name != 'END':
            statments.append(self.parseStatment(control_flow_statment_names))
        self.checkAndAdvance('END')
        return ParsingObjects.WhileStatment(cond, statments)

#######################################################################################################
#Class Parsing
#######################################################################################################

    #Parses a class declaration
    def parseCLASSStatment(self):
        self.checkAndAdvance('CLASS')
        name = self.current_token.value
        self.checkAndAdvance('NAME')
        self.checkAndAdvance('COLON')
        methods = {}
        staticMethods = {}
        constructor = None
        instanceVariables = []
        staticVariables = {}
        #classVariables = {}
        #class_statment_names = ['NEW', 'THIS', 'PRINT', 'INTEGERTYPE', 'STRINGTYPE', 'FLOATTYPE', 'BOOLEANTYPE', 'NAME', 'IF', 'WHILE', 'END']
        while self.current_token.name != 'END':
            if self.current_token.name == 'STATIC': 
                if self.lookAhead(2) == 'LPAREN':
                    method = self.parseStaticMethod(name)
                    staticMethods.update({method.name: method})
                else:
                    self.checkAndAdvance('STATIC')
                    None
            elif self.current_token.name == 'METHOD':
                method = self.parseMethodDeclaration()
                methods.update({method.name: method})
            elif self.current_token.name == 'NAME' and self.lookAhead(1).name == 'LPAREN': constructor = self.parseConstructor() 
            elif self.current_token.name in ['NAME', 'FLOATTYPE', 'INTEGERTYPE', 'STRINGTYPE', 'BOOLEANTYPE']:
                instanceVar = self.parseVariableDeclaration()
                instanceVariables.append(instanceVar)
               #if isinstance(instanceVar, ParsingObjects.InstanceDeclarationStatment):
                    #instanceVariables.append(instanceVar)
                #else:
                    #instanceVariables.append(instanceVar)
            else:
                print(self.current_token)
                return Errors.ParseError('Syntax Error', 'Unable To Parse Class Statment').ErrorCheck()
        self.checkAndAdvance('END')
        return ParsingObjects.ClassDeclaration(name, constructor, methods, instanceVariables, staticMethods, staticVariables)

    def parseClassFunction(self, className):
        self.checkAndAdvance('FUNC')
        type = self.current_token.name
        self.checkAndAdvanceList(['INTEGERTYPE', 'STRINGTYPE', 'BOOLEANTYPE', 'FLOATTYPE', 'NILTYPE', 'NAME'])
        name = self.current_token.value
        self.checkAndAdvance('NAME')
        params = self.parseParams()
        statments = []
        function_statment_names = ['PRINT', 'INTEGERTYPE', 'STRINGTYPE', 'FLOATTYPE', 'BOOLEANTYPE', 'NAME', 'IF', 'WHILE', 'END', 'RETURN']
        while self.current_token.name != 'END':
            statments.append(self.parseStatment(function_statment_names))
        self.checkAndAdvance('END')
        return ParsingObjects.FunctionDeclaration(type, name, params, statments, className) 

    def parseMethodDeclaration(self):
        self.checkAndAdvance('METHOD')
        type = self.current_token.value
        #check this, type could be Name
        self.checkAndAdvanceList(['INTEGERTYPE', 'FLOATTYPE', 'STRINGTYPE', 'BOOLEANTYPE', 'NILTYPE', 'NAME'])
        name = self.current_token.value
        self.checkAndAdvance('NAME')
        params = self.parseParams()
        statments = []
        method_statment_names = ['THIS', 'PRINT', 'INTEGERTYPE', 'STRINGTYPE', 'FLOATTYPE', 'BOOLEANTYPE', 'NAME', 'IF', 'WHILE', 'END', 'RETURN']
        while self.current_token.name != 'END':
            statments.append(self.parseStatment(method_statment_names))
        self.checkAndAdvance('END')
        return InterpretingObjects.MethodDeclaration(type, name, params, statments)
    
    def parseInstanceMethod(self):
        #name.method1().method2(). ... .methodn()
        #instanceName = self.current_token.value
        instance = self.current_token.value
        methodName = None
        args = None
        self.checkAndAdvance('NAME')
        while self.current_token.name == 'DOT':
            self.checkAndAdvance('DOT')
            methodName = self.current_token.value
            self.checkAndAdvance('NAME')
            args = self.parseArguments()
            instance = ParsingObjects.InstanceMethodCall2(instance, methodName, args)
        return instance

    def parseMethodCall(self):
        methodName = self.current_token.value
        self.checkAndAdvance('NAME')
        args = self.parseArguments()
        if self.current_token.name == 'DOT':
            self.checkAndAdvance('DOT')
            return ParsingObjects.MethodCall(methodName, args, ParsingObjects.MethodCall(self.parseMethodCall()))
        else:
            self.checkAndAdvance('SEMICOLON')
            return ParsingObjects.MethodCall(methodName, args, None)

    def parseConstructor(self):
        name = self.current_token.value
        self.checkAndAdvance('NAME')
        params = self.parseParams()#change to handle params
        statments = []
        method_statment_names = ['PRINT', 'INTEGERTYPE', 'STRINGTYPE', 'FLOATTYPE', 'BOOLEANTYPE', 'NAME', 'IF', 'WHILE', 'END']
        while self.current_token.name != 'END':
            statments.append(self.parseStatment(method_statment_names))
        self.checkAndAdvance('END')
        return ParsingObjects.Constructor(name, params, statments)
    
    def parseThisStatment(self):
        self.advance()
        self.checkAndAdvance('DOT')
        name = self.current_token.value
        self.checkAndAdvance('NAME')
        if self.current_token == 'LPAREN':
            args = self.parseArguments()
            self.checkAndAdvance('SEMICOLON')
            return ParsingObjects.ThisRefrenceStatment(ParsingObjects.InstanceMethodCall(None, name, args))
        elif self.current_token == 'ASSIGNMENT':
            #add support
            #variable declaration, instance declaration
            return ParsingObjects.ThisAssignmentStatment()
        else: return ParsingObjects.ThisRefrenceStatment(ParsingObjects.VariableRefrenceStatment(name))

    def parseInstanceAssignment(self, name):
        self.checkAndAdvance('NEW')
        instanceOf = self.current_token.value
        self.checkAndAdvance('NAME')
        args = self.parseArguments()
        self.checkAndAdvance('SEMICOLON')
        return ParsingObjects.InstanceAssignmentStatment(instanceOf, name, ParsingObjects.ClassInstance(instanceOf, args))
    
    def parseInstanceDeclaration(self):
        className = self.current_token.value
        self.checkAndAdvance('NAME')
        name = self.current_token.value
        self.checkAndAdvance('NAME')
        instance = None
        if self.current_token.name == 'ASSIGNMENT':
            self.advance()
            if self.current_token.name == 'NAME':
                instance = self.current_token.value
                self.advance()
            else:
                self.checkAndAdvance('NEW')
                className2 = self.current_token.value
                self.checkAndAdvance('NAME')
                args = self.parseArguments()
                instance = ParsingObjects.ClassInstance(className2, args)
        self.checkAndAdvance('SEMICOLON')
        return ParsingObjects.InstanceDeclarationStatment(className, name, instance)

#######################################################################################################
#Function Parsing
#######################################################################################################

    #Parses A Function Declaration
    def parseFUNCStatment(self):
        self.checkAndAdvance('FUNC')
        type = self.current_token.name
        self.checkAndAdvanceList(['INTEGERTYPE', 'STRINGTYPE', 'BOOLEANTYPE', 'FLOATTYPE', 'NILTYPE'])
        name = self.current_token.value
        self.checkAndAdvance('NAME')
        params = self.parseParams()
        statments = []
        function_statment_names = ['NEW', 'PRINT', 'INTEGERTYPE', 'STRINGTYPE', 'FLOATTYPE', 'BOOLEANTYPE', 'NAME', 'IF', 'WHILE', 'END', 'RETURN']
        while self.current_token.name != 'END':
            statments.append(self.parseStatment(function_statment_names))
        self.checkAndAdvance('END')
        return ParsingObjects.FunctionDeclaration(type, name, params, statments, None)
    
    #Parses a Function Declaration's Paramaters
    def parseParams(self):
        self.checkAndAdvance('LPAREN')
        params = []
        while self.current_token.name != 'RPAREN':
            params.append(self.parseParam())
        self.checkAndAdvance('RPAREN')
        self.checkAndAdvance('COLON')
        return params

    #Parses a Function Declaration's Param
    def parseParam(self):
        type = self.current_token.name
        if type == 'NAME': type = self.current_token.value
        self.checkAndAdvanceList(['INTEGERTYPE', 'BOOLEANTYPE', 'STRINGTYPE', 'FLOATTYPE', 'NAME'])
        name = self.current_token.value
        self.checkAndAdvance('NAME')
        if self.current_token.name == 'COMMA': self.advance()
        return ParsingObjects.Param(type, name)

    #Parses a Function Call
    def parseFunctionCall(self):
        built_in_functions = {
        'substr':self.parseSubstringFunction, 
        'strinsert':self.parseStringInsertFunction, 
        'len':self.parseLenFunction,
        'get':self.parseGetFunction,
        }
        if self.current_token.value in built_in_functions:
            #getattr(self, 'parse' + self.current_token.name + 'Function')()
            return built_in_functions[self.current_token.value]()
        else:
            name = self.current_token.value
            self.checkAndAdvance('NAME')
            args = self.parseArguments()
            return ParsingObjects.FunctionCall(name, args)

    #Parses a Function Call's Arguments
    def parseArguments(self):
        self.checkAndAdvance('LPAREN')
        args = []
        while self.current_token.name != 'RPAREN':
            #expr = self.expression()
            args.append(self.expression())
            if self.current_token!=None and self.current_token.name == 'COMMA': self.advance()
        self.checkAndAdvance('RPAREN')
        return args

    #Parses a Function's Return Statment
    def parseRETURNStatment(self):
        self.checkAndAdvance('RETURN')
        val =  self.parseExpressionStatment()
        return ParsingObjects.Return(val)
    
    #Parses Built in substr() Function
    def parseSubstringFunction(self):
        self.checkAndAdvance('NAME')
        self.checkAndAdvance('LPAREN')
        strName = self.current_token.value
        self.checkAndAdvance('NAME')
        self.checkAndAdvance('COMMA')
        startIndex = self.expression()
        self.checkAndAdvance('COMMA')
        endIndex = self.expression()
        self.checkAndAdvance('RPAREN')
        return ParsingObjects.SubstringFunctionCall(strName, startIndex, endIndex)
    
    #Parses Built in strinsert() Function
    def parseStringInsertFunction(self):
        self.checkAndAdvance('NAME')
        self.checkAndAdvance('LPAREN')
        strName = self.current_token.value
        self.checkAndAdvance('NAME')
        self.checkAndAdvance('COMMA')
        index = self.expression()
        self.checkAndAdvance('COMMA')
        string = self.expression()
        self.checkAndAdvance('RPAREN')
        return ParsingObjects.StringInsertFunctionCall(strName, index, string)
    
    #Parses Built in len() Function
    def parseLenFunction(self):
        self.checkAndAdvance('NAME')
        self.checkAndAdvance('LPAREN')
        name = self.current_token.value
        self.checkAndAdvance('NAME')
        self.checkAndAdvance('RPAREN')
        return ParsingObjects.len(name)
    
    #Parses Built in get() Function
    def parseGetFunction(self):
        self.checkAndAdvance('NAME')
        self.checkAndAdvance('LPAREN')
        name = self.current_token.value
        self.checkAndAdvance('NAME')
        self.checkAndAdvance('COMMA')
        index = self.expression()
        self.checkAndAdvance('RPAREN')
        return ParsingObjects.get(name, index)

    #Function and Variable Declaration Helper Method
    def parseNILTYPEStatment(self):
        return self.arrayVariable()

    #Function and Variable Declaration Helper Method
    def parseINTEGERTYPEStatment(self):
        return self.arrayVariable()

    #Function and Variable Declaration Helper Method
    def parseSTRINGTYPEStatment(self):
        return self.arrayVariable()

    #Function and Variable Declaration Helper Method
    def parseBOOLEANTYPEStatment(self):
        return self.arrayVariable()
    
    #Function Declaration Helper Method
    def parseFLOATTYPEStatment(self):
        return self.arrayVariable()
    
    def arrayVariable(self):
        #change to getAttr()?
        if self.lookAhead(1).name == 'LBRACKET': return self.parseArrayDeclaration()
        else: return self.parseVariableDeclaration()

#######################################################################################################
#Variable and Array Parsing
#######################################################################################################

    #Parses a variable Declaration (includes Arrays)
    def parseVariableDeclaration(self):
        value = None
        type = self.current_token.name
        if type == 'NAME': return self.parseInstanceDeclaration()
        #type = self.current_token.value
        self.checkAndAdvanceList(['INTEGERTYPE', 'STRINGTYPE', 'BOOLEANTYPE', 'FLOATTYPE'])
        name = self.current_token.value
        self.checkAndAdvance('NAME')
        if self.current_token.name == 'ASSIGNMENT':
            self.advance()
            value = self.expression()
        self.checkAndAdvance('SEMICOLON')
        return ParsingObjects.VariableDeclarationStatment(type, name, value)
    
    def parseArrayDeclaration(self):
        thingThatIsAssigned = None
        type = self.current_token.name
        self.checkAndAdvanceList(['INTEGERTYPE', 'STRINGTYPE', 'BOOLEANTYPE', 'FLOATTYPE'])
        self.checkAndAdvance('LBRACKET')
        self.checkAndAdvance('RBRACKET')
        name = self.current_token.value
        self.checkAndAdvance('NAME')
        if self.current_token.name == 'ASSIGNMENT':
            thingThatIsAssigned = self.parseArrayAssignment(name)
        else: self.checkAndAdvance('SEMICOLON')
        return ParsingObjects.ArrayDeclaration(type, name, thingThatIsAssigned)
    
    def parseArrayAssignment(self, name):
        self.checkAndAdvance('ASSIGNMENT')
        if self.current_token.name == 'LBRACKET':
            self.advance()
            size = self.expression()
            self.checkAndAdvance('RBRACKET')
            self.checkAndAdvance('SEMICOLON')
            return ParsingObjects.ArraySizeAssignment(name, size)
        else:
            name2 = self.current_token.value
            self.checkAndAdvance('NAME')
            self.checkAndAdvance('SEMICOLON')
            return ParsingObjects.ArrayArrayAssignment(name, name2)
    
    #Parses Variable Assignments (includes Arrays)
    def parseNAMEStatment(self):
        if self.lookAhead(1).name == 'NAME':
            return self.parseVariableDeclaration()
        elif self.lookAhead(1).name == 'ASSIGNMENT':
            name = self.current_token.value
            self.checkAndAdvance('NAME')
            if self.lookAhead(1).name == 'LBRACKET':
                return self.parseArrayAssignment(name)
            elif self.lookAhead(1).name == 'NEW':
                self.advance()
                return self.parseInstanceAssignment(name)
            else:
                return self.parseVariableAssignment(name)#also can be array assignment (if an array is assigned to another array)
        #elif self.lookAhead(1).name == 'NAME':
            #return self.parseVariableDeclaration()
        elif self.lookAhead(1).name == 'LBRACKET':
            name = self.current_token.value
            self.checkAndAdvance('NAME')
            self.checkAndAdvance('LBRACKET')
            index = self.expression()
            self.checkAndAdvance('RBRACKET')
            self.checkAndAdvance('ASSIGNMENT')
            element = self.expression()
            self.checkAndAdvance('SEMICOLON')
            return ParsingObjects.ArrayIndexAssignment(name, index, element)
        else:
            return self.parseExpressionStatment()
    
    #Parses Variable Assignments
    def parseVariableAssignment(self, name):
        self.checkAndAdvance('ASSIGNMENT')
        value = self.expression()
        self.checkAndAdvance('SEMICOLON')
        return ParsingObjects.VariableAssignmentStatment(name, value)
        
#######################################################################################################
#Expression Parsing
#######################################################################################################

#I coded my own Expression Parsing. But the operator presedence (the order in which operators are parsed)
#is from Crafting Interpreters. https://craftinginterpreters.com/contents.html

    #Parses Expression Statment (1+1; func(); 'string';...)
    def parseExpressionStatment(self):
        expr = self.expression()
        self.checkAndAdvance('SEMICOLON')
        return ParsingObjects.Expression(expr)
    
    #Parses Expressions (1+1 2+2 func() 'string')
    def expression(self):
        return self.equality()
    def equality(self):
        return self.split(self.comparison, 'EQUALS')
    def comparison(self):
        return self.split(self.andOr, ['GREATER', 'LESS'])
    def andOr(self):
        return self.split(self.addition, ['AND', 'OR'])
    def addition(self):
        return self.split(self.multiplication, ['PLUS', 'MINUS'])
    def multiplication(self):
        return self.split(self.unary, ['MULT', 'DIV', 'MOD'])
    
    #Parses Unary Expressions (~Expression)
    def unary(self):
        if self.current_token.name in ['NOT']:
            operator = self.current_token
            self.advance()
            return ParsingObjects.UnaryOp(operator, self.unary())
        else:
            return self.grouping()

    #Parses Expression Groupings (((((1+1)+1))+1))
    def grouping(self):
        if self.current_token.name == 'LPAREN':
            self.advance()
            expr = self.expression()
            self.checkAndAdvance('RPAREN')
            return expr
        else:
            return self.literal()
    
    def literal(self):
        #'DOT'
        tokenNames = ['INT','STRING', 'BOOL','NAME', 'FLOAT', 'NEW']#'END'
        token = None
        if self.current_token.name in tokenNames: 
            token = getattr(self, 'handle'+self.current_token.name)()
        else:
            error = Errors.ParseError('Parsing Error', 'Unable To Parse Expression')
            error.ErrorCheck()
        return token

    #Used for Parsing Expressions (Parses with Respect to Operator Precedence)
    def split(self, nextMethod, tokens):
        left = nextMethod()
        while self.current_token.name in tokens:
            operator = self.current_token
            self.checkAndAdvanceList(['PLUS', 'MINUS', 'MULT', 'DIV', 'EQUALS', 'LESS', 'GREATER', 'MOD', 'AND', 'OR'])
            right = nextMethod()
            left = getattr(self, 'handle'+operator.name)(left, operator, right)
        return left

    #Parsing Helpers for split
    def handlePLUS(self, left, operator, right):
        return ParsingObjects.AdditionExpression(left, operator, right)
    def handleMINUS(self, left, operator, right):
        return ParsingObjects.SubtractionExpression(left, operator, right)
    def handleDIV(self, left, operator, right):
        return ParsingObjects.DivisionExpression(left, operator, right)
    def handleMULT(self, left, operator, right):
        return ParsingObjects.MultiplicationExpression(left, operator, right)
    def handleEQUALS(self, left, operator, right):
        return ParsingObjects.EquivalenceExpression(left, operator, right)
    def handleGREATER(self, left, operator, right):
        return ParsingObjects.GreaterComparisonExpression(left, operator, right)
    def handleLESS(self, left, operator, right):
        return ParsingObjects.LessComparisonExpression(left, operator, right)
    def handleOR(self, left, operator, right):
        return ParsingObjects.OrExpression(left, operator, right)
    def handleAND(self, left, operator, right):
        return ParsingObjects.AndExpression(left, operator, right)
    def handleMOD(self, left, operator, right):
        return ParsingObjects.ModExpression(left, operator, right)

    #Parsing Helpers for Literal
    def handleINT(self):
        val = self.current_token.value
        self.checkAndAdvance('INT')
        return ParsingObjects.LiteralInteger(val)
    def handleSTRING(self):
        val = self.current_token.value
        self.checkAndAdvance('STRING')
        return ParsingObjects.LiteralString(val)
    def handleBOOL(self):
        val = self.current_token.value
        self.checkAndAdvance('BOOL')
        return ParsingObjects.LiteralBoolean(val)
    def handleFLOAT(self):
        val = self.current_token.value
        self.checkAndAdvance('FLOAT')
        return ParsingObjects.LiteralFloat(val)
    
    def handleNEW(self):
        self.checkAndAdvance('NEW')
        instanceName = self.current_token.value
        self.checkAndAdvance('NAME')
        args = self.parseArguments()
        return ParsingObjects.ClassInstance(instanceName, args)

    #Handles Names in Expressions (Function Calls, Variable Refrences, Array Indexing)
    def handleNAME(self):
        if self.lookAhead(1).name == 'LPAREN': return self.parseFunctionCall()
        elif self.lookAhead(1).name == 'DOT': 
            return self.parseInstanceMethod()
        else:
            val = self.current_token.value
            self.checkAndAdvance('NAME')
            return ParsingObjects.VariableRefrenceStatment(val)

    def handleTHIS(self):
        self.advance()
        self.checkAndAdvance('DOT')
        name = self.current_token.value
        self.checkAndAdvance('NAME')
        if self.current_token == 'LPAREN':
            args = self.parseArguments()
            self.checkAndAdvance('SEMICOLON')
            #add chaining support
            return ParsingObjects.ThisRefrenceStatment(ParsingObjects.InstanceMethodCall(None, name, args))
        else: return ParsingObjects.ThisRefrenceStatment(ParsingObjects.VariableRefrenceStatment(name))

#######################################################################################################
#Miscellaneous Parsing
#######################################################################################################

    #Parses Print Statment (Note: print is not a function)
    def parsePRINTStatment(self):
        self.checkAndAdvance('PRINT')
        expr = self.expression()
        self.checkAndAdvance('SEMICOLON')
        return ParsingObjects.PrintStatment(expr)

    def parseENDStatment(self):
        self.checkAndAdvance('END')
        #return ParsingObjects.EndStatment()

#######################################################################################################
#Miscellaneous Parsing Helper Methods
####################################################################################################

    #Returns the Next Token
    def nextToken(self):
        #Replace with lookahead
        if self.token_index+1 < len(self.tokens): return self.tokens[self.token_index+1]
        else: return None
    
    #Returns the nth Token
    def lookAhead(self, index):
        if self.token_index+index < len(self.tokens): return self.tokens[self.token_index+index]
        else: return None

    #Checks that the Name of the Current Token is What it Should be
    def checkAndAdvance(self, tokenName):
        if self.current_token.name == tokenName: 
            self.advance()
            return True
        else:
            error = Errors.ParseError('Syntax Error:', 'Current Token: ' + self.current_token.name + ' should be: ' + tokenName)
            error.ErrorCheck()
            return False
    
    #Checks that the Name of the Current Token is What it Should be
    def checkAndAdvanceList(self, list):
        if self.current_token.name in list: 
            self.advance()
            return True
        else:
            error = Errors.ParseError('Missing Token Error (in list)', list)
            error.ErrorCheck()
            return False