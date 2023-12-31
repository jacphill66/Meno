#Using the Visitor Pattern in Tree-Walk interpreters is boilerplate. (While the code is my own, I did not come up with this idea).
class ParseObject():
    def __init__(): pass

    def accept(): pass

    def __repr__(self): pass

    def ErrorCheck(self): return self

#######################################################################################################
#Control Flow Parsing
#######################################################################################################

class Else(ParseObject):
    def __init__(self, statments):
        self.statments = statments

    def __repr__(self):
        return f'Else Statment: else {self.statments}'

    def accept(self, visitor):
        return visitor.visitElseStatment(self)

class IfElseStatment(ParseObject):
    def __init__(self, ifStatment, elseStatments):
        self.ifStatment = ifStatment
        self.elseStatments = elseStatments

    def __repr__(self):
        return f'If Statment: if {self.ifStatment.cond}: {self.ifStatment.statments} else: {self.elseStatments.statments}'

    def accept(self, visitor):
        return visitor.visitIfElseStatment(self)

class IfStatment(ParseObject):
    def __init__(self, cond, statments):
        self.cond = cond
        self.statments = statments

    def __repr__(self):
        return f'If Statment: if {self.cond}: {self.statments}'

    def accept(self, visitor):
        return visitor.visitIfStatment(self)

class WhileStatment(ParseObject):
    def __init__(self, cond, statments):
        self.cond = cond
        self.statments = statments

    def __repr__(self):
        return f'While Statment: while {self.cond}: {self.statments}'

    def accept(self, visitor):
        return visitor.visitWhileStatment(self)

#######################################################################################################
#Function Parsing
#######################################################################################################

class Return(ParseObject):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'Return Statment: return {self.value}'

    def accept(self, visitor):
        return visitor.visitReturnStatment(self)

class Param(ParseObject):
    def __init__(self, type, name):
        self.type = type
        self.name = name
        self.value = None

    def __repr__(self):
        return f'Parameter: {self.type} {self.name}'

    def accept(self, visitor):
        return visitor.visitParam(self)

class FunctionDeclaration(ParseObject):
    def __init__(self, type, name, params, statments, className):
        self.type = type
        self.name = name
        self.params = params
        self.statments = statments
        #remove class name
        self.className = className

    def __repr__(self):
        return f'Function Declaration: function {self.type} {self.name} ({self.params}): {self.statments}'
    
    def accept(self, visitor):
        return visitor.visitFunctionDeclaration(self)

class FunctionCall(ParseObject):
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def __repr__(self):
        return f'Function Call: {self.name} ({self.args})'

    def accept(self, visitor):
        return visitor.visitFunctionCall(self)

class SubstringFunctionCall(ParseObject):
    def __init__(self, name, startIndex, endIndex):
        self.name = name
        self.startIndex = startIndex
        self.endIndex = endIndex

    def __repr__(self):
        return f'Substring Function Call: substring({self.name}, {self.startIndex}, {self.endIndex})'

    def accept(self, visitor):
        return visitor.visitSubstringStatment(self)

class StringInsertFunctionCall(ParseObject):
    def __init__(self, name, index, string):
        self.name = name
        self.index = index
        self.string = string

    def __repr__(self):
        return f'Stringinsert Function Call: strinsert{self.name}[{self.index}] @ {self.string}'

    def accept(self, visitor):
        return visitor.visitStringInsert(self)

class len(ParseObject):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'Len Function Call: len({self.name})'

    def accept(self, visitor):
        return visitor.visitLen(self)

class get(ParseObject):
    def __init__(self, name, index):
        self.name = name
        self.index = index

    def __repr__(self):
        return f'Get Function Call: get({self.name}, {self.index})'

    def accept(self, visitor):
        return visitor.visitGet(self)

#######################################################################################################
#Variable and Array Parsing
#######################################################################################################

class VariableRefrenceStatment(ParseObject):
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return f'Variable Refrence: {self.name}'

    def accept(self, visitor):
        return visitor.visitVariableRefrenceStatment(self)

class VariableAssignmentStatment(ParseObject):
    def __init__(self, name, value):
        self.name = name
        self.value = value
    
    def __repr__(self):
        return f'Variable Assignment: {self.name} @: {self.value}'
    
    def accept(self, visitor):
        return visitor.visitVariableAssignmentStatment(self)

class VariableDeclarationStatment(ParseObject):
    def __init__(self, type, name, value):
        self.type = type
        self.name = name
        self.value = value
    
    def __repr__(self):
        return f'Variable Declaration: {self.type} {self.name} @ {self.value}'
    
    def accept(self, visitor):
        return visitor.visitVariableDeclarationStatment(self)

class ArrayArrayAssignment(ParseObject):
    def __init__(self, name, name2):
        self.name = name
        self.name2 = name2

    def __repr__(self):
        return f'Array Assignment: {self.name} @ {self.name2}'

    def accept(self, visitor):
        return visitor.ArrayArrayAssignment(self)

class ArraySizeAssignment(ParseObject):
    def __init__(self, name, size):
        self.name = name
        self.size = size

    def __repr__(self):
        return f'Array Assignment: {self.name}  @ [{self.size}]'

    def accept(self, visitor):
        return visitor.visitEmptyArrayAssignment(self)

class ArrayDeclaration(ParseObject):
    def __init__(self, type, name, thing):
        self.type = type
        self.name = name
        self.thing = thing
        self.value = []

    def __repr__(self):
        return f'Array Declaration: {self.type} {self.name}[] @ {self.value}'

    def accept(self, visitor):
        return visitor.visitArrayDeclaration(self)

class ArrayIndexAssignment(ParseObject):
    def __init__(self, name, index, element):
        self.name = name
        self.index = index
        self.element = element

    def __repr__(self):
        return f'Array Index Assignment: {self.name}[{self.index}] @ {self.element}'

    def accept(self, visitor):
        return visitor.visitArrayIndexAssignment(self)

#######################################################################################################
#Expression Parsing
#######################################################################################################

class LiteralBoolean(ParseObject):
    def __init__(self, value):
        self.value = value
        self.type = 'BOOLEANTYPE'

    def __repr__(self):
        return f'Literal Boolean: {self.value}'

    def accept(self, visitor):
        return visitor.visitLiteralBoolean(self)

class LiteralInteger(ParseObject):
    def __init__(self, value):
        self.value = int(value)
        self.type = 'INTEGERTYPE'

    def __repr__(self):
        return f'Literal Integer: {self.value}'

    def accept(self, visitor):
        return visitor.visitLiteralInteger(self)

class LiteralFloat(ParseObject):
    def __init__(self, value):
        self.value = value
        self.type = 'FLOATTYPE'

    def __repr__(self):
        return f'Literal Float: {self.value}'

    def accept(self, visitor):
        return visitor.visitLiteralFloat(self)

class LiteralString(ParseObject):
    def __init__(self, value):
        self.value = value
        self.type = 'STRINGTYPE'

    def __repr__(self):
        return f'Literal String: {self.value}'

    def accept(self, visitor):
        return visitor.visitLiteralString(self)

class UnaryOp(ParseObject):
    def __init__(self, op, right):
        self.op = op
        self.right = right
    
    def __repr__(self):
        return f'Unary Expression: ({self.op} {self.right})'
    
    def accept(self, visitor):
        return visitor.visitUnaryOp(self)

class MultiplicationExpression(ParseObject):
    def __init__(self, left, op, right):
        self.right = right
        self.op = op
        self.left = left
    
    def __repr__(self):
        return f'Multiplication Expression: ({self.left} {self.op} {self.right})'

    def accept(self, visitor):
        return visitor.visitMultiplicationExpression(self)

class DivisionExpression(ParseObject):
    def __init__(self, left, op, right):
        self.right = right
        self.op = op
        self.left = left
    
    def __repr__(self):
        return f'Division Expression: ({self.left} {self.op} {self.right})'

    def accept(self, visitor):
        return visitor.visitDivisionExpression(self)

class SubtractionExpression(ParseObject):
    def __init__(self, left, op, right):
        self.right = right
        self.op = op
        self.left = left
    
    def __repr__(self):
        return f'Subtraction Expression: ({self.left} {self.op} {self.right})'

    def accept(self, visitor):
        return visitor.visitSubtractionExpression(self)

class AdditionExpression(ParseObject):
    def __init__(self, left, op, right):
        self.right = right
        self.op = op
        self.left = left
    
    def __repr__(self):
        return f'Addition Expression: ({self.left} {self.op} {self.right})'

    def accept(self, visitor):
        return visitor.visitAdditionExpression(self)

class LessComparisonExpression(ParseObject):
    def __init__(self, left, op, right):
        self.right = right
        self.op = op
        self.left = left
    
    def __repr__(self):
        return f'Less Than Comparison Expression: ({self.left} {self.op} {self.right})'

    def accept(self, visitor):
        return visitor.visitLessComparisonExpression(self)

class OrExpression(ParseObject):
    def __init__(self, left, op, right):
        self.right = right
        self.op = op
        self.left = left
    
    def __repr__(self):
        return f'Or Expression: ({self.left} {self.op} {self.right})'

    def accept(self, visitor):
        return visitor.visitOrExpression(self)

class AndExpression(ParseObject):
    def __init__(self, left, op, right):
        self.right = right
        self.op = op
        self.left = left
    
    def __repr__(self):
        return f'And Expression: ({self.left} {self.op} {self.right})'

    def accept(self, visitor):
        return visitor.visitAndExpression(self)

class ModExpression(ParseObject):
    def __init__(self, left, op, right):
        self.right = right
        self.op = op
        self.left = left
    
    def __repr__(self):
        return f'Modulus Expression: ({self.left} {self.op} {self.right})'

    def accept(self, visitor):
        return visitor.visitModExpression(self)

class GreaterComparisonExpression(ParseObject):
    def __init__(self, left, op, right):
        self.right = right
        self.op = op
        self.left = left
    
    def __repr__(self):
        return f'Greater Than Comparison Expression: ({self.left} {self.op} {self.right})'

    def accept(self, visitor):
        return visitor.visitGreaterComparisonExpression(self)

class EquivalenceExpression(ParseObject):
    def __init__(self, left, op, right):
        self.right = right
        self.op = op
        self.left = left
    
    def __repr__(self):
        return f'Equivalence Expression: ({self.left} {self.op} {self.right})'

    def accept(self, visitor):
        return visitor.visitEquivalenceExpression(self)

class Expression(ParseObject):#change to expression
    def __init__(self, exprAST):
        self.exprAST = exprAST
    
    def __repr__(self):
        return f'Expression Statment: {self.exprAST}'

    def accept(self, visitor):
        return visitor.visitExpressionStatment(self)

#######################################################################################################
#Class Parsing
#######################################################################################################

class ClassDeclaration(ParseObject):
    #add support for class (static) variables
    def __init__(self, name, constructor, methods, instanceVariables, staticMethods, staticVariables):
        self.name = name
        self.constructor = constructor
        self.methods = methods
        self.instanceVariables = instanceVariables
        self.staticMethods = staticMethods
        self.staticVariables = staticVariables

    def __repr__(self):
        return f'Class Declaration: {self.name} Instance Variables: {self.instanceVariable} Constructor: {self.constructor} Methods: {self.methods}'

    def accept(self, visitor):
        return visitor.visitClassDeclaration(self)

#Remove?
class MethodDeclaration(ParseObject):
    def __init__(self, type, name, params, statments):
        self.type = type
        self.name = name
        self.params = params
        self.statments = statments

    def __repr__(self):
        return f'Method Declaration: {self.name} ({self.params}): {self.statments}'
    
    def accept(self, visitor):
        return visitor.visitMethodDeclaration(self)

class InstanceMethodCall(ParseObject):
    def __init__(self, instanceName, methodCall, args):
        self.instanceName = instanceName
        self.methodCall = methodCall
        self.args = args

    def __repr__(self):
        return f'Instance Method Call: {self.instanceName}.{self.methodCall}({self.args});'
    
    def accept(self, visitor):
        return visitor.visitInstanceMethod(self)

class InstanceMethodCall2(ParseObject):
    def __init__(self, instance, methodCall, args):
        self.instance = instance
        self.methodCall = methodCall
        self.args = args

    def __repr__(self):
        return f'{self.instance}.{self.methodCall}'
    
    def accept(self, visitor):
        return visitor.visitInstanceMethod2(self)
    
class MethodCall(ParseObject):
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def __repr__(self):
        return f'Method Call: {self.name}({self.args})'
    
    def accept(self, visitor):
        return visitor.visitMethodCall(self)

class Constructor(ParseObject):
    def __init__(self, name, params, statments):
        self.name = name
        self.params = params
        self.statments = statments

    def __repr__(self):
        return f'Constructor Declaration: {self.name} ({self.params}): {self.statments}'
    
    def accept(self, visitor):
        return visitor.visitConstructor(self)

class ClassInstance(ParseObject):
    def __init__(self, className, args):
        self.className = className
        self.args = args
        self.vars = None

    def __repr__(self):
        return f'Class Instance: {self.className}({self.args})'

    def accept(self, visitor):
        return visitor.visitClassInstance(self)

class InstanceAssignmentStatment(ParseObject):
    def __init__(self, className, name, instance):
        self.className = className
        self.name = name
        self.instance = instance
    
    def __repr__(self):
        return f'Instance Assigment: {self.name} @ {self.instance}'
    
    def accept(self, visitor):
        return visitor.visitInstanceAssignmentStatment(self)

class ThisAssignmentStatment(ParseObject):
    def __init__(self, instanceVarName, thing):
        self.instanceVarName = instanceVarName
        self.thing = thing

    def __repr__(self):
        return f'This Assignment Statment: {self.thing} @ {self.thing}'
    
    def accept(self, visitor):
        return visitor.visitThisAssignmentStatment(self)

class ThisRefrenceStatment(ParseObject):
    def __init__(self, thing):
        self.thing = thing

    def __repr__(self):
        return f'This Refrence Statment: {self.thing}'
    
    def accept(self, visitor):
        return visitor.visitThisRefrenceStatment(self)

class InstanceDeclarationStatment(ParseObject):
    def __init__(self, className, name, instance):
        self.className = className
        self.name = name
        self.instance = instance

    def __repr__(self):
        return f'Instance Declaration: {self.name} @ {self.instance}'
    
    def accept(self, visitor):
        return visitor.visitInstanceDeclarationStatment(self)

#####################################################################################################
#Miscellaneous Parsing Helper Methods
####################################################################################################

class EndStatment(ParseObject):
    def __repr__(self):
        return f'End Statment: END'
    
    def accept(self, visitor):
        return visitor.visitEndStatment(self)

class PrintStatment(ParseObject):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'Print Statment: {self.value}'

    def accept(self, visitor):
        return visitor.visitPrintStatment(self)