import re

class Tokenizer(object):

    def __init__(self, file):
        self.currentToken = None
        self.tokenIndex = None
        self.loadLists()
        self.loadDictionary()
        fhand = open(file)
        self.tokenList = fhand.readlines()
        self.prepare()
        self.toEnd = len(self.tokenList)

    def loadLists(self):
        self.keywords = [
            'class',
            'constructor',
            'function',
            'method',
            'field',
            'static',
            'var',
            'int',
            'char',
            'boolean',
            'void',
            'true',
            'false',
            'null',
            'this',
            'let',
            'do',
            'if',
            'else',
            'while',
            'return'
        ]
        self.symbols = [
            '{', '}', '(', ')', '[', ']', '.',
            ',', ';', '+', '-', '*', '/', '&',
            '|', '<', '>', '=', '~'
        ]

    def loadDictionary(self):
        self.symbolSwitch = {
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            '&': '&amp;'
        }

    def prepare(self):
        cleanedFile = []

        for line in self.tokenList:
            line = line.strip()
            if line == '':
                continue
            if line[0] == '/':
               continue
            if line[0] == '*':
                continue
            if '/*' in line:
                fields = line.split('/*')
                line = fields[0]
            if '//' in line:
                fields = line.split('//')
                line = fields[0]
            tokenized = re.findall(r'[\w]+|[*\{\}()\[\].,;+\\\-&/|<>=~\?]|[\"\'].+[\"\']', line)
            for token in tokenized:
                cleanedFile.append(token)

        self.tokenList = cleanedFile

    def createXML(self):
        if self.tokenType() == "KEYWORD":
            return("<keyword> " +
                self.currentToken + " </keyword>")
        if self.tokenType() == "IDENTIFIER":
            return("<identifier> " +
                self.currentToken + " </identifier>")
        if self.tokenType() == "SYMBOL":
            return("<symbol> "+
                self.symbol() + " </symbol>")
        if self.tokenType() == "STRING_CONST":
            return("<stringConstant> "+
                self.stringVal() + " </stringConstant>")
        if self.tokenType() == "INT_CONST":
            return("<integerConstant> "+
                self.currentToken + " </integerConstant>")

#####   API ######


    def hasMoreTokens(self):
        if self.toEnd > 0:
            return True
        else:
            return False

    def advance(self):
        if self.currentToken == None:
            self.tokenIndex = 0
        else:
            self.tokenIndex = self.tokenIndex +1
        if self.hasMoreTokens():
            self.currentToken = self.tokenList[self.tokenIndex]
            self.toEnd = self.toEnd - 1

    def lookAhead(self):
        if self.toEnd >= 1:
            return self.tokenList[self.tokenIndex+1]

    def tokenType(self):
        if self.currentToken in self.keywords:
            return('KEYWORD')
        elif self.currentToken in self.symbols:
            return('SYMBOL')
        elif str.isdigit(self.currentToken):
            if 0 <= int(self.currentToken) <= 32767:
                return('INT_CONST')
        elif self.currentToken[0] == '"':
            return('STRING_CONST')
        match = re.fullmatch(r'[a-zA-Z_]+[0-9a-zA-Z_]*', self.currentToken)
        if match != None:
            return('IDENTIFIER')
        print('Made it through all possible token types... :(')

    def symbol(self):
        if self.tokenType() == 'SYMBOL':
            if any(str in self.currentToken for str in self.symbolSwitch):
                return self.symbolSwitch[self.currentToken]
            else:
                return self.currentToken

    def identifier(self):
        if self.tokenType() == 'IDENTIFIER':
            return self.currentToken

    def intVal(self):
        if self.tokenType() == 'INT_CONST':
            return int(self.currentToken)

    def stringVal(self):
        if self.tokenType() == "STRING_CONST":
            return self.currentToken[1:-1]
