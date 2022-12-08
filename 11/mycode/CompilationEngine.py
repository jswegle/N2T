class CompilationEngine(object):
    def __init__(self, tokenizer, output):
        self.output = open(output, 'w')
        self.tokenizer = tokenizer
        self.tokenizer.advance() ## currentToken goes from None to class
        self.loadLists()
        self.tab = '\t'
        self.CompileClass()

    def loadLists(self):
        self.statementNames = ['do', 'while', 'if', 'let', 'return']
        self.operators = ['+', '~', '-', '*', '/', '&', '|', '<', '>', '=']

    def incTab(self):
        self.tab = self.tab + '\t'

    def decTab(self):
        i = len(self.tab)
        if i >1:
            self.tab = self.tab[:-1]

    def writeAndInc(self):
        self.output.write(self.tab+self.tokenizer.createXML()+'\n')
        self.tokenizer.advance()

    def CompileClass(self):
        self.output.write('<class>\n')
        self.writeAndInc()
        self.writeAndInc()
        self.writeAndInc()
        self.CompileClassVarDec()
        while self.tokenizer.currentToken != '}':
            self.CompileSubroutine()

        self.writeAndInc()              ## }
        self.decTab()
        self.output.write('</class>')


    def CompileClassVarDec(self):
        if any(str in self.tokenizer.currentToken for str in ("field", "static")):
            self.output.write(self.tab+'<classVarDec>\n')
            self.incTab()
            while self.tokenizer.currentToken != ';':
                self.writeAndInc()
            self.writeAndInc()
            self.decTab()
            self.output.write(self.tab+'</classVarDec>\n')
            self.CompileClassVarDec()

    def CompileSubroutine(self):
        if any(str in self.tokenizer.currentToken for str in ('function', 'constructor', 'method')):
            self.output.write(self.tab+'<subroutineDec>\n')
            self.incTab()
            self.writeAndInc()
            self.writeAndInc()
            self.writeAndInc()          ## subroutineName
            self.writeAndInc()          ## (
            self.compileParameterList()
            self.writeAndInc()          ## )
            self.output.write(self.tab+'<subroutineBody>\n')
            self.incTab()
            self.writeAndInc()          ## '{'
            while 'var' in self.tokenizer.currentToken:
                self.compileVarDec()

            self.compileStatements()
            self.writeAndInc()          ## '}'
            self.decTab()
            self.output.write(self.tab+'</subroutineBody>\n')
            self.decTab()
            self.output.write(self.tab+'</subroutineDec>\n')


    def compileParameterList(self):
        self.output.write(self.tab+'<parameterList>\n')
        self.incTab()
        while self.tokenizer.currentToken != ')':
            self.writeAndInc()
        self.decTab()
        self.output.write(self.tab+'</parameterList>\n')


    def compileVarDec(self):
        self.output.write(self.tab+'<varDec>\n')
        self.incTab()
        while self.tokenizer.currentToken != ';':
            self.writeAndInc()
        self.writeAndInc()                      ## ;
        self.decTab()
        self.output.write(self.tab+'</varDec>\n')


    def compileStatements(self):
        self.output.write(self.tab+'<statements>\n')
        self.incTab()
        while any(str in self.tokenizer.currentToken for str in self.statementNames):
            if self.tokenizer.currentToken == 'do':
                self.compileDo()
            elif self.tokenizer.currentToken == 'let':
                self.compileLet()
            elif self.tokenizer.currentToken == 'while':
                self.compileWhile()
            elif self.tokenizer.currentToken == 'return':
                self.compileReturn()
            elif self.tokenizer.currentToken == 'if':
                self.compileIf()
        self.decTab()
        self.output.write(self.tab+'</statements>\n')

    def compileDo(self):
        self.output.write(self.tab+'<doStatement>\n')
        self.incTab()
        self.writeAndInc()              ## do
        self.writeAndInc()              ## subroutineName | class/var Name
        if self.tokenizer.currentToken == '.':
            self.writeAndInc()          ## '.'
            self.writeAndInc()          ## subroutineName
        self.writeAndInc()              ## (

        self.CompileExpressionList()
        self.writeAndInc()              ## ')'
        self.writeAndInc()              ## ';'
        self.decTab()
        self.output.write(self.tab+'</doStatement>\n')

    def compileLet(self):
        self.output.write(self.tab+'<letStatement>\n')
        self.incTab()
        self.writeAndInc()                  ## let
        self.writeAndInc()                  ## var
        if self.tokenizer.currentToken == '[':
            self.writeAndInc()              ## [
            self.CompileExpression()
            self.writeAndInc()              ## ]
        self.writeAndInc()                  ## =
        self.CompileExpression()
        self.writeAndInc()                  ## ;
        self.decTab()
        self.output.write(self.tab+'</letStatement>\n')

    def compileWhile(self):
        self.output.write(self.tab+'<whileStatement>\n')
        self.incTab()
        self.writeAndInc()              ## while
        self.writeAndInc()              ## (
        self.CompileExpression()
        self.writeAndInc()              ## )
        self.writeAndInc()              ## {
        while self.tokenizer.currentToken != '}':
            self.compileStatements()
        self.writeAndInc()              ## }
        self.decTab()
        self.output.write(self.tab+'</whileStatement>\n')


    def compileReturn(self):
        self.output.write(self.tab+'<returnStatement>\n')
        self.incTab()
        self.writeAndInc()                  ## return
        if self.tokenizer.currentToken != ';' :
            self.CompileExpression()
        self.writeAndInc()                  ## writes
        self.decTab()
        self.output.write(self.tab+'</returnStatement>\n')

    def compileIf(self):
        self.output.write(self.tab+'<ifStatement>\n')
        self.incTab()
        self.writeAndInc()          ## if
        self.writeAndInc()          ## (
        self.CompileExpression()
        self.writeAndInc()          ## )
        self.writeAndInc()          ## {
        self.compileStatements()
        self.writeAndInc()          ## }
        if self.tokenizer.currentToken == 'else':
            self.writeAndInc()      ## else
            self.writeAndInc()      ## {
            self.compileStatements()
            self.writeAndInc()      ## }
        self.decTab()
        self.output.write(self.tab+'</ifStatement>\n')

    def CompileExpression(self):
        ## term (op term)*
        self.output.write(self.tab+'<expression>\n')
        self.incTab()
        self.CompileTerm()
        while any(str in self.tokenizer.currentToken for str in self.operators):
            self.writeAndInc()          ## op
            self.CompileTerm()
        self.decTab()
        self.output.write(self.tab+'</expression>\n')

    def CompileTerm(self):
        self.output.write(self.tab+'<term>\n')
        self.incTab()
        #print(self.tokens[self.i])
        if any(str in self.tokenizer.currentToken for str in self.operators):
            ## unaryOp term
            self.writeAndInc()              ## op
            self.CompileTerm()
        elif self.tokenizer.currentToken == '(':
            ## ( expression )
            self.writeAndInc()              ## (
            self.CompileExpression()
            self.writeAndInc()              ## )
            #self.output.write(self.tab+'EXITING ( term )\n')
        elif self.tokenizer.lookAhead() == '.':
            ## ( className | varName ) . subroutineName ( expressionList )
            self.writeAndInc()              ## className | varName
            self.writeAndInc()              ## '.'
            self.writeAndInc()              ## subroutineName
            self.writeAndInc()              ## '('
            self.CompileExpressionList()
            self.writeAndInc()              ## ')'
        elif self.tokenizer.lookAhead() == '(':
            ## subroutineName ( expressionList )
            self.writeAndInc()
            self.writeAndInc() ## writes '('
            self.CompileExpressionList()
            self.writeAndInc() ## writes ')'
        elif self.tokenizer.lookAhead() == '[':
            ## varName [ expression ]
            self.writeAndInc()              ## varName
            self.writeAndInc()              ## '['
            self.CompileExpression()
            self.writeAndInc()              ## ']'
        else:
            ## intConst | strConst | keywordConst | varName
            self.writeAndInc()
        #self.writeAndInc()
        self.decTab()
        self.output.write(self.tab+'</term>\n')

    def CompileExpressionList(self):
        self.output.write(self.tab+'<expressionList>\n')
        self.incTab()
        while self.tokenizer.currentToken != ')' :
            self.CompileExpression()
            if self.tokenizer.currentToken == ',':
                self.writeAndInc()
        self.decTab()
        self.output.write(self.tab+'</expressionList>\n')
