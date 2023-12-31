import Lexing, Parser, EnvironmentAndScope, sys, Interpreting2

def lexText(text):
        lexer = Lexing.Lexer(text)
        tokens = lexer.lex()
        print(tokens)

def parseTokens(tokens):
    parser = Parser.Parse(tokens)
    result = parser.parse()
    print(result)

def lexFileText(fname):
    text = getFileText(fname)
    lexer = Lexing.Lexer(text)
    tokens = lexer.lex()
    print(tokens)

def lexAndParseFile(fname):
    text = getFileText(fname)
    lexer = Lexing.Lexer(text)
    tokens = lexer.lex()
    print(tokens)
    parser = Parser.Parse(tokens)
    result = parser.parse()
    for element in result:
        print(element)

def lexParseAndInterpretFile(fname):
    text = getFileText(fname)
    lexer = Lexing.Lexer(text)
    tokens = lexer.lex()
    print(tokens)

    parser = Parser.Parse(tokens)
    statments = parser.parse()

    interpreter = Interpreting2.Interpreter(statments)
    interpreter.interpret()

def getFileText(fname):
    f = open(fname)
    text = f.read()
    return text

sys.setrecursionlimit(10000)

lexParseAndInterpretFile('C:\\Users\\jacphill\\Desktop\\Class Demo\\demo.txt')