
class compilationEngine(object):

    def __init__(self, tokens, output):
        self.output = output
        self.tokens = tokens
        self.i = 1
        self.loadLists()
        self.tokenNumber = len(self.tokens)
        self.tab = '\t'
        #for token in self.tokens:
        #    print(token)
        #self.output.write(self.tokens[0]+'\n')
        self.CompileClass()
        #print(self.tab)


    def loadLists(self):
        self.statementNames = ['do', 'while', 'if', 'let', 'return']
        self.operators = ['+', '~', '-', '*', ' / ', '&amp', '|', '&lt', '&gt', '=']


    def incTab(self):
        self.tab = self.tab + '\t'

    def decTab(self):
        i = len(self.tab)
        if i >1:
            self.tab = self.tab[:-1]

    def incrementI(self):
        ##self.i is our token index
        if self.i < self.tokenNumber:
            self.i = self.i+1

    def writeAndInc(self):
        self.output.write(self.tab+self.tokens[self.i]+'\n')
        self.incrementI()

    def lookAhead(self):
        lookAhead = self.i+1
        return self.tokens[lookAhead]

    def CompileClass(self):
        #print('In CompileClass')
        self.output.write('<class>\n')
        self.writeAndInc()
        self.writeAndInc()
        self.writeAndInc()
        #print('heading to compileclassVarDec')
        self.CompileClassVarDec()
        while '}' not in self.tokens[self.i]:
            self.CompileSubroutine()
        # self.CompileSubroutine()
        # self.CompileSubroutine()
        # self.CompileSubroutine()
        self.writeAndInc() ## writes }
        self.decTab()
        self.output.write('</class>')


    def CompileClassVarDec(self):
        #print(self.tokens[self.i])
        if any(str in self.tokens[self.i] for str in ("field", "static")):
            #print("In CompileClassVarDec")
            self.output.write(self.tab+'<classVarDec>\n')
            self.incTab()
            while ';' not in self.tokens[self.i]:
                self.writeAndInc()
            self.writeAndInc()
            self.decTab()
            self.output.write(self.tab+'</classVarDec>\n')
            self.CompileClassVarDec()
        #self.output.write("\t\tClassvardec!\n")

    def CompileSubroutine(self):
        if any(str in self.tokens[self.i] for str in ('function', 'constructor', 'method')):
            self.output.write(self.tab+'<subroutineDec>\n')
            self.incTab()
            self.writeAndInc()
            self.writeAndInc()
            self.writeAndInc() ##writes subroutineName
            self.writeAndInc() ##writes (
            self.compileParameterList()
            self.writeAndInc() ## writes )
            self.output.write(self.tab+'<subroutineBody>\n')
            self.incTab()
            self.writeAndInc() ##writes '{'
            while 'var' in self.tokens[self.i]:
                self.compileVarDec()

            self.compileStatements()
            self.writeAndInc() ## writes '}'
            self.decTab()
            self.output.write(self.tab+'</subroutineBody>\n')
            self.decTab()
            self.output.write(self.tab+'</subroutineDec>\n')


    def compileParameterList(self):
        self.output.write(self.tab+'<parameterList>\n')
        self.incTab()
        while ')' not in self.tokens[self.i]:
            self.writeAndInc()
        self.decTab()
        self.output.write(self.tab+'</parameterList>\n')


    def compileVarDec(self):
        self.output.write(self.tab+'<varDec>\n')
        self.incTab()
        while ';' not in self.tokens[self.i]:
            self.writeAndInc()
        self.writeAndInc() ## writes ';'
        self.decTab()
        self.output.write(self.tab+'</varDec>\n')


    def compileStatements(self):
        self.output.write(self.tab+'<statements>\n')
        self.incTab()
        #print(self.tokens[self.i])
        while any(str in self.tokens[self.i] for str in self.statementNames):
            if 'do' in self.tokens[self.i]:
                self.compileDo()
            elif 'let' in self.tokens[self.i]:
                self.compileLet()
            elif 'while' in self.tokens[self.i]:
                self.compileWhile()
            elif 'return' in self.tokens[self.i]:
                self.compileReturn()
            elif 'if' in self.tokens[self.i]:
                self.compileIf()
        self.decTab()
        self.output.write(self.tab+'</statements>\n')

    def compileDo(self):
        self.output.write(self.tab+'<doStatement>\n')
        self.incTab()
        self.writeAndInc() ##writes do
        self.writeAndInc() ## either subroutineName or class/var Name. Second case enters if
        if '.' in self.tokens[self.i]:
            self.writeAndInc() ## writes '.'
            self.writeAndInc() ## writes subroutineName
        self.writeAndInc() ##writes (

        self.CompileExpressionList()
        self.writeAndInc() ## writes ')'
        self.writeAndInc() ## writes ';'
        self.decTab()
        self.output.write(self.tab+'</doStatement>\n')

    def compileLet(self):
        self.output.write(self.tab+'<letStatement>\n')
        self.incTab()
        self.writeAndInc()
        self.writeAndInc()
        if '[' in self.tokens[self.i]:
            self.writeAndInc() ## writes [
            self.CompileExpression()
            self.writeAndInc() ## writes ]
        self.writeAndInc() ## writes =
        self.CompileExpression()
        self.writeAndInc() ## writes ;
        self.decTab()
        self.output.write(self.tab+'</letStatement>\n')

    def compileWhile(self):
        self.output.write(self.tab+'<whileStatement>\n')
        self.incTab()
        self.writeAndInc() ##writes 'while'
        self.writeAndInc() ## writes '('
        self.CompileExpression()
        self.writeAndInc() ## writes ')'
        self.writeAndInc() ## writes '{'
        while '}' not in self.tokens[self.i]:
            self.compileStatements()
        self.writeAndInc() ## writes '}'
        self.decTab()
        self.output.write(self.tab+'</whileStatement>\n')


    def compileReturn(self):
        self.output.write(self.tab+'<returnStatement>\n')
        self.incTab()
        self.writeAndInc() ## writes return
        if ';' not in self.tokens[self.i]:
            self.CompileExpression()
        self.writeAndInc()  ##writes ;
        self.decTab()
        self.output.write(self.tab+'</returnStatement>\n')

    def compileIf(self):
        self.output.write(self.tab+'<ifStatement>\n')
        self.incTab()
        self.writeAndInc() ## writes if
        self.writeAndInc() ## writes (
        self.CompileExpression()
        self.writeAndInc() ## writes )
        self.writeAndInc() ## writes {
        self.compileStatements()
        self.writeAndInc() ## writes }
        if 'else' in self.tokens[self.i]:
            self.writeAndInc() ## writes else
            self.writeAndInc() ## writes {
            self.compileStatements()
            self.writeAndInc() ## writes }
        self.decTab()
        self.output.write(self.tab+'</ifStatement>\n')

    def CompileExpression(self): ## term (op term)*
        self.output.write(self.tab+'<expression>\n')
        self.incTab()
        self.CompileTerm()
        while any(str in self.tokens[self.i] for str in self.operators):
            # print('what the actual fuck')
            # print(self.tokens[self.i])
            # print('\n')
            #self.output.write(self.tab+'ENTER CompEx,WHILE\n')
            self.writeAndInc()
            self.CompileTerm()
            #self.output.write(self.tab+'EXIT CompEx,WHILE\n')
        self.decTab()
        self.output.write(self.tab+'</expression>\n')

    def CompileTerm(self):
        self.output.write(self.tab+'<term>\n')
        self.incTab()
        print(self.tokens[self.i])
        if any(str in self.tokens[self.i] for str in self.operators):
            #self.output.write(self.tab+'ENTERING UNARY\n')
            self.writeAndInc() ## writes the operator
            self.CompileTerm()
            #self.output.write(self.tab+'EXITING UNARY\n')
        elif '(' in self.tokens[self.i]: ## for ( term ) case
            #self.output.write(self.tab+'ENTERING ( term )\n')
            self.writeAndInc() ## writes (
            self.CompileExpression()
            self.writeAndInc() ## writes )
            #self.output.write(self.tab+'EXITING ( term )\n')
        elif '.' in self.lookAhead():
            self.writeAndInc()
            self.writeAndInc() ## writes '.'
            self.writeAndInc()
            self.writeAndInc() ## writes '('
            self.CompileExpressionList()
            self.writeAndInc() ## writes ')'
        elif '(' in self.lookAhead():
            self.writeAndInc()
            self.writeAndInc() ## writes '('
            self.CompileExpressionList()
            self.writeAndInc() ## writes ')'
        elif '[' in self.lookAhead():
            self.writeAndInc()
            self.writeAndInc() ## writes '['
            self.CompileExpression()
            self.writeAndInc() ## writes ']'
        else: ## in this case its just a simple identifer
            self.writeAndInc()
        #self.writeAndInc()
        self.decTab()
        self.output.write(self.tab+'</term>\n')

    def CompileExpressionList(self):
        self.output.write(self.tab+'<expressionList>\n')
        self.incTab()
        while ')' not in self.tokens[self.i]:
            self.CompileExpression()
            if ',' in self.tokens[self.i]:
                self.writeAndInc()
        self.decTab()
        self.output.write(self.tab+'</expressionList>\n')


class JackTokenizer(object):

    def __init__(self, file):
        self.currentToken = None
        self.tokenIndex = None
        self.loadLists()
        self.loadDictionary()
        fhand = open(file)
        self.file = fhand.readlines()
        self.prepare()
        self.toEnd = len(self.file)
        #print(self.file)
        #while(self.hasMoreTokens()):
        #    self.advance()
        #    print(self.currentToken)
        #    print(self.tokenType())
        #    print(self.stringVal())
        #print("after a while")


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
            '<':'&lt;',
            '>': '&gt;',
            '"': '&quot;',
            '&': '&amp;'
        }

    def prepare(self):
        cleanedFile = []

        for line in self.file:
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
            #print(line)
            tokenized = re.findall(r'[\w]+|[*\{\}()\[\].,;+\\\-&/|<>=~\?]|[\"\'].+[\"\']', line)
            for token in tokenized:
                cleanedFile.append(token)
                #print(token)

        self.file = cleanedFile
        #print(self.file)

    def writetoXML(self, line):
        self.output.write(line + '\n')

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
        self.currentToken = self.file[self.tokenIndex]
        self.toEnd = self.toEnd - 1
        # if self.currentToken == "\"":
        #     stringToken = "\""
        #     lookAheadIndex = 1
        #     while(self.file[self.tokenIndex + lookAheadIndex] != "\""):
        #         stringToken += self.file[self.tokenIndex + lookAheadIndex]
        #         lookAheadIndex = lookAheadIndex + 1
        #         if self.file[self.tokenIndex + lookAheadIndex] != "\"":
        #             stringToken += " "
        #     self.currentToken = stringToken
        #     self.tokenIndex = self.tokenIndex + lookAheadIndex
        #     self.toEnd = self.toEnd - lookAheadIndex

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

class Main(object):

    def __init__(self, filepath):
        self.jackfiles = []
        self.fileOrDir(filepath)
        for file in self.jackfiles:
            tokenizeroutputfilename = file.split('.')[0]+'blah.xml'
            tokenslist = []
            self.tokenizeroutput = open(tokenizeroutputfilename, 'w')
            tokenizer = JackTokenizer(file)
            #print(tokenizer.file)
            self.tokenizeroutput.write("<tokens>\n")
            tokenslist.append("<tokens>")
            while tokenizer.hasMoreTokens() == True:
                tokenizer.advance()
                #print(tokenizer.currentToken)
                if tokenizer.tokenType() == "KEYWORD":
                    self.tokenizeroutput.write("<keyword> " +
                        tokenizer.currentToken + " </keyword>\n")
                    tokenslist.append("<keyword> " +
                        tokenizer.currentToken + " </keyword>")
                if tokenizer.tokenType() == "IDENTIFIER":
                    self.tokenizeroutput.write("<identifier> " +
                        tokenizer.currentToken + " </identifier>\n")
                    tokenslist.append("<identifier> " +
                        tokenizer.currentToken + " </identifier>")
                if tokenizer.tokenType() == "SYMBOL":
                    self.tokenizeroutput.write("<symbol> "+
                        tokenizer.symbol() + " </symbol>\n")
                    tokenslist.append("<symbol> "+
                        tokenizer.symbol() + " </symbol>")
                if tokenizer.tokenType() == "STRING_CONST":
                    self.tokenizeroutput.write("<stringConstant> "+
                        tokenizer.stringVal() + " </stringConstant>\n")
                    tokenslist.append("<stringConstant> "+
                        tokenizer.stringVal() + " </stringConstant>")
                if tokenizer.tokenType() == "INT_CONST":
                    self.tokenizeroutput.write("<integerConstant> "+
                        tokenizer.currentToken + " </integerConstant>\n")
                    tokenslist.append("<integerConstant> "+
                        tokenizer.currentToken + " </integerConstant>")
            self.tokenizeroutput.write("</tokens>")
            tokenslist.append("</tokens>")
            outputfilename = file.split('.')[0]+'.xml'
            #print(outputfilename)
            self.Output = open(outputfilename, 'w')
            compEngine = compilationEngine(tokenslist, self.Output)



    def fileOrDir(self, filepath):
        # print("fileOrDir:")
        # print("-------------------------------------------------------D")
        if '.jack' in filepath:
            self.jackfiles = [filepath]
        else:
            pathelements = filepath.split('/')
            for root, dirs, files in os.walk(filepath):
                for file in files:
                    if ".jack" in file:
                        self.jackfiles.append(root + '/' + file)


if __name__ == '__main__':
    import sys
    import os
    import re
    filepath = sys.argv[1]
    Main(filepath)
