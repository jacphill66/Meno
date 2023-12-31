import Errors
WHITE_SPACE = ' \t\n'
STRINGALPHABET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_!@#$%^&*()+=-<>,.?/;:"\[]}{\t\n '
NAMEALPHABET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_'
DIGITS = '0123456789'

class Position:
    def __init__(self, line, char):
        self.line = line
        self.char = char

class Token:
    def __init__(self, name, value, position):
        self.name = name
        self.value = value
        self.position = position

    def __repr__(self):
        return f'{self.name}: {self.value}'

class Lexer:
    def __init__(self, text):
        self.text = text
        self.index = 0
        self.line = 0
        self.current_char = self.text[self.index]
        self.lexed_tokens = []

    #Lexing helper methods
    def plus(self, pos): return Token('PLUS', None, pos)
    def minus(self, pos): return Token('MINUS', None, pos)
    def mult(self, pos): return Token('MULT', None, pos)
    def div(self, pos): return Token('DIV', None, pos)
    def equals(self, pos): return Token('EQUALS', None, pos)
    def less(self, pos): return Token('LESS', None, pos)
    def greater(self, pos): return Token('GREATER', None, pos)
    def notToken(self, pos): return Token('NOT', None, pos)
    def true(self, pos): return Token('BOOL', True, pos)
    def false(self, pos): return Token('BOOL', False, pos)
    def assignment(self, pos): return Token('ASSIGNMENT', None, pos)
    def lparen(self, pos): return Token('LPAREN', None, pos)
    def rparen(self, pos): return Token('RPAREN', None, pos)
    def returnToken(self, pos): return Token('RETURN', None, pos)
    def semicolon(self, pos): return Token('SEMICOLON', None, pos)
    def colon(self, pos): return Token('COLON', None, pos)
    def comma(self, pos): return Token('COMMA', None, pos)
    def lbracket(self, pos): return Token('LBRACKET', None, pos)
    def rbracket(self, pos): return Token('RBRACKET', None, pos)
    def mod(self, pos): return Token('MOD', None, pos)
    def andToken(self, pos): return Token('AND', None, pos)
    def orToken(self, pos): return Token('OR', None, pos)
    def dot(self, pos): return Token('DOT', None, pos)

    def lex(self):
        #single char tokens
        token_dict = {
            '+':self.plus,
            '-':self.minus,
            '*':self.mult,
            '/':self.div,
            '=':self.equals,
            '<':self.less,
            '>':self.greater,
            '~':self.notToken,
            'T':self.true,
            'F':self.false,
            '@':self.assignment,
            '(':self.lparen,
            ')':self.rparen,
            '^':self.returnToken,
            ';':self.semicolon,
            ':':self.colon,
            ',':self.comma,
            '[':self.lbracket,
            ']':self.rbracket,
            '%':self.mod,
            '&':self.andToken,
            '|':self.orToken,
            '.':self.dot
        }
        self.handleFirstRule()
        while self.current_char != None:
            if self.current_char =='#':
                while self.current_char!='\n': 
                    self.advance()
            elif self.current_char in WHITE_SPACE:
                if self.current_char == '\n': self.line+=1
                self.advance()
            elif self.current_char == '\'':
                self.addToken(self.handleString())
            elif self.current_char in token_dict:
                self.addToken((token_dict[self.current_char](Position(self.line, self.index))))
                self.advance()
            elif self.current_char in DIGITS:#literal number
                self.addToken(self.handleNumber())
            elif self.current_char in NAMEALPHABET:#literalString, name, or a multichar token
                self.addToken(self.handleName())
            else:
                print(self.current_char)
                error = Errors.LexError('Invalid Token', 'User Entered an Invalid Token')
                error.ErrorCheck()
        if not self.checkEnd(): 
            error = Errors.LexError('Missing End', 'Add :\'end\' to the End of the Program')
            error.ErrorCheck()
        return self.lexed_tokens

    def handleString(self):
        if self.current_char != '\'': return Errors.LexError('Missing Quote', 'Missing Left \'')
        self.advance()
        curr_string = ''
        while self.current_char in STRINGALPHABET:
            curr_string+=self.current_char
            self.advance()
        if self.current_char != '\'': return Errors.LexError('Missing Quote', 'Missing Right: \'')
        self.advance()
        return Token('STRING', curr_string, Position(self.line, self.index))

    def print(self, pos): return Token('PRINT', None, pos)
    def ifToken(self, pos): return Token('IF', None, pos)
    def elseToken(self, pos): return Token('ELSE', None, pos)
    def whileToken(self, pos): return Token('WHILE', None, pos)
    def function(self, pos): return Token('FUNC', None, pos)
    def integer(self, pos): return Token('INTEGERTYPE', 'INTEGERTYPE', pos)
    def boolean(self, pos): return Token('BOOLEANTYPE', 'BOOLEANTYPE', pos)
    def float(self, pos): return Token('FLOATTYPE', 'FLOATTYPE', pos)
    def string(self, pos): return Token('STRINGTYPE', 'STRINGTYPE', pos)
    def end(self, pos): return Token('END', None, pos)
    def nil(self, pos): return Token('NILTYPE', 'NILTYPE', pos)
    def classToken(self, pos): return Token('CLASS', None, pos)
    def method(self, pos): return Token('METHOD', None, pos)
    def new(self, pos): return Token('NEW', None, pos)
    def this(self, pos): return Token('THIS', None, pos)
    def static(self, pos): return Token('STATIC', None, pos)

    def handleName(self):
        currString = ''
        longer_tokens = {
            'print':self.print,
            'if':self.ifToken,
            'else':self.elseToken,
            'while':self.whileToken,
            'function':self.function,
            'integer':self.integer,
            'boolean':self.boolean,
            'float':self.float,
            'string':self.string,
            'end':self.end,
            'nil':self.nil,
            'class':self.classToken, 
            'method':self.method,
            'new':self.new,
            'this':self.this,
            'static':self.static
        }
        while self.current_char !=None and self.current_char in NAMEALPHABET:
            currString += self.current_char
            if currString in longer_tokens and not self.nextCharInAlphabet():
                self.advance() 
                return longer_tokens[currString](None)
            self.advance()
        return Token('NAME', currString, None)

    def handleNumber(self):
        currNumber = ''
        dot = False
        while self.current_char!=None and self.current_char in DIGITS or self.current_char == '.':
            if not dot and self.current_char == '.':
                dot = True
            elif dot and self.current_char == '.':
                return Errors.LexError('Float Error','Too Many .\'s')
            currNumber += self.current_char
            self.advance()
        if dot: return Token('FLOAT', currNumber, None)
        else: return Token('INT', currNumber, None)

    def checkEnd(self):
        if len(self.text) >= 3: 
            return 'end' == self.text[len(self.text)-3:len(self.text)]
        return False

    def nextCharInAlphabet(self):
        if self.index+1 < len(self.text): return self.text[self.index+1] in NAMEALPHABET
        else: return False

    def advance(self):
        self.index+=1
        if self.index < len(self.text): self.current_char=self.text[self.index]
        else: self.current_char = None
    
    def addToken(self, token):
        self.lexed_tokens.append(token)
    
    def handleFirstRule(self):
        currString = ''
        count = 0
        str = 'You Don\'t Talk About Meno!'
        while count < len(str):
            currString += self.current_char
            count +=1
            self.advance()
        if currString != str:
            error = Errors.LexError('Missing First Rule', 'Don\'t forget the first rule!')
            error.ErrorCheck()