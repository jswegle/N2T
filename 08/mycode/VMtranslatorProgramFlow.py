import os

class Parser(object):

    def __init__(self, vmfile):
        # print("Parser init")
        # print("-------------------------------------------------------D")
        # print(vmfile + ':')
        fhand = open(vmfile)
        self.file = fhand.readlines()
        # print(self.file)
        # print("-------------------------------------------------------D")
        self.cleanFile()
        print(self.file)
        self.commandindex=0
        self.totalcommands = 0
        for line in self.file:
            self.totalcommands = self.totalcommands+1
        self.currentcommand = None

####### API
#######

    def hasMoreCommands(self):
        return self.totalcommands - self.commandindex > 0

    def advance(self):
        if self.hasMoreCommands() == True:
            self.currentcommand = self.file[self.commandindex]
            self.commandindex = self.commandindex + 1

    def commandType(self):
        if self.currentcommand.find('push') != -1:
            return('C_PUSH')
        elif self.currentcommand.find('pop') != -1:
            return('C_POP')
        elif self.currentcommand.find('label') != -1:
            return('C_LABEL')
        elif self.currentcommand.find('if-goto') != -1:
            return('C_IF')
        elif self.currentcommand.find('goto') != -1:
            return('C_GOTO')
        elif self.currentcommand.find('function') != -1:
            return('C_FUNCTION')
        elif self.currentcommand.find('return') != -1:
            return('C_RETURN')
        elif self.currentcommand.find('call') != -1:
            return('C_CALL')
        else:
            return('C_ARITHMETIC')


    def arg1(self):
            #this function does not control when it is called,
            #but it should not be called when the current command is a C_RETURN
        if self.commandType() == 'C_ARITHMETIC':
            return self.currentcommand.split()[0]
        else:
            lst= self.currentcommand.split()
            return lst[1]

    def arg2(self):
        #should only be called in one of these four cases. The else statement is a failsafe
        if self.commandType()== "C_PUSH":
            lst=self.currentcommand.split()
            return(lst[2])
        if self.commandType()== "C_POP":
            lst=self.currentcommand.split()
            return(lst[2])
        if self.commandType()== "C_FUNCTION":
            lst=self.currentcommand.split()
            return(lst[2])
        if self.commandType()== "C_CALL":
            lst=self.currentcommand.split()
            return(lst[2])
        else:
            print("Not a valid current command")

####### end API
#######

    def cleanFile(self):
        #print("Cleaning!")
        cleanedFile=[]
        for line in self.file:
            line = line.strip()
            if line == '':
                continue
            elif line[0] == '/':
                continue
            else:
                if '//' in line:
                    line = line.split('//')[0]
                cleanedFile.append(line)
        self.file = cleanedFile


class CodeWriter(object):

    def __init__(self, asmfile):
        self.asm = open(asmfile, 'w+')
        self.curr_file = None
        self.boolcount = 0
        self.address = self.address_dict()
        
        self.currLabelPrefix = '$'
        self.returnAddressIndex = 0
        self.opList = ['gt', 'lt', 'eq']

##### API
#####



    def writeLabel(self, label):
        self.write('//WRITELABEL')
        self.write('(' + self.currLabelPrefix + '$' + label + ')')

    def writeGoto(self, label):
        self.write('//WRITEGOTO')
        self.write('@'+ self.currLabelPrefix + '$' + label)
        self.write('0;JMP')

    def writeIf(self, label):
        self.write('//WRITEIF')
        self.fromStacktoDandDec()
        self.write('@'+ self.currLabelPrefix + '$' + label)
        self.write('D;JNE')



    def setFileName(self, vm_filename):
        self.curr_file = vm_filename.split('/')[-1]

    def writeArithmetic(self, operation):
        self.fromStacktoDandDec()
        if operation == 'neg':
            self.write('D=-D')
        elif operation == 'not':
            self.write('D=!D')
        else:
            self.write('@R13')
            self.write('M=D')
            self.fromStacktoDandDec()
            self.write('@R13')
            if operation == 'add':
                self.write('D=M+D')
            elif operation == 'sub':
                self.write('D=D-M')
            elif operation == 'or':
                self.write('D=D|M')
            elif operation == 'and':
                self.write('D=D&M')
            elif operation in ['gt', 'lt', 'eq']:
                self.write('D=D-M')
                self.write('@bool{}'.format(self.boolcount))
                if operation == 'eq':
                    self.write('D;JEQ')
                if operation == 'gt':
                    self.write('D;JGT')
                if operation == 'lt':
                    self.write('D;JLT')
                self.write('@R14')
                self.write('M=0')
                self.write('D=M')
                self.write('@endbool{}'.format(self.boolcount))
                self.write('0;JMP')
                self.write('(bool{})'.format(self.boolcount))
                self.write('@R14')
                self.write('M=-1')
                self.write('D=M')
                self.write('(endbool{})'.format(self.boolcount))
                self.boolcount = self.boolcount + 1
        self.fromDtoStackandInc()

    def writePushPop(self, command, segment, index):
        self.addressToA(segment, index)
        if command == 'C_PUSH':
            if segment == 'constant':
                self.write('D=A')
            else:
                self.write('D=M')
            self.fromDtoStackandInc()
        elif command == 'C_POP':
            self.write('D=A')
            self.write('@R13')
            self.write('M=D')
            self.fromStacktoDandDec()
            self.write('@R13')
            self.write('A=M')
            self.write('M=D')

##### end API
#####

    def write(self, comm):
        self.asm.write(comm + '\n')

    def address_dict(self):
        return {
          'local': 'LCL', # Base R1
          'argument': 'ARG', # Base R2
          'this': 'THIS', # Base R3
          'that': 'THAT', # Base R4
          'pointer': 3, # Edit R3, R4
          'temp': 5, # Edit R5-12
          # R13-15 are free
          'static': 16, # Edit R16-255
      }

    def addressToA(self, segment, index):
        seg = self.address.get(segment)
        if segment in ['local', 'argument', 'this', 'that']:
            self.write('@'+seg)
            self.write('D=M')
            self.write('@'+str(index))
            self.write('A=D+A')
        elif segment == 'constant':
            self.write('@'+ str(index))
        elif segment in ['pointer', 'temp']:
            self.write('@R'+str(seg + int(index)))
        elif segment == 'static':
            self.write('@'+ self.curr_file + str(index))

    def fromStacktoDandDec(self):
         self.write('@SP')
         self.write('M=M-1')
         self.write('A=M')
         self.write('D=M')


    def fromDtoStackandInc(self):
        self.write('@SP')
        self.write('A=M')
        self.write('M=D')
        self.write('@SP')
        self.write('M=M+1')

class Main(object):

    def __init__(self, filepath):
        self.fileOrDir(filepath)
        # print(self.vmfiles)
        # print("-------------------------------------------------------D")
        self.cw = CodeWriter(self.asmfile)
        for vmfile in self.vmfiles:
            self.translate(vmfile)


    def fileOrDir(self, filepath):
        # print("fileOrDir:")
        # print("-------------------------------------------------------D")
        if '.vm' in filepath:
            self.asmfile = filepath.replace('vm', 'asm')
            self.vmfiles = [filepath]
        else:
            pathelements = filepath.split('/')
            self.asmfile = '/'.join(pathelements) + '/' + pathelements[-1] + '.asm'
            self.vmfiles = []
            for root, dirs, files in os.walk(filepath):
                for file in files:
                    if ".vm" in file:
                        self.vmfiles.append(root + '/' + file)


    def translate(self, vm_file):
        parser = Parser(vm_file)
        self.cw.setFileName(vm_file)
        while parser.hasMoreCommands() == True:
            parser.advance()
            if parser.commandType() == 'C_PUSH':
                self.cw.writePushPop('C_PUSH', parser.arg1(), parser.arg2())
            elif parser.commandType() == 'C_POP':
                self.cw.writePushPop('C_POP', parser.arg1(), parser.arg2())
            elif parser.commandType() == 'C_ARITHMETIC':
                self.cw.writeArithmetic(parser.arg1())
            elif parser.commandType() == 'C_LABEL':
                #print(parser.arg1())
                self.cw.writeLabel(parser.arg1())
            elif parser.commandType() == 'C_GOTO':
                self.cw.writeGoto(parser.arg1())
            elif parser.commandType() == 'C_IF':
                self.cw.writeIf(parser.arg1())
                #print(parser.currentcommand)
            elif parser.commandType() == 'C_FUNCTION':
                self.cw.writeFunction(parser.arg1(), parser.arg2())
            elif parser.commandType() == 'C_RETURN':
                self.cw.writeReturn()
            elif parser.commandType() == 'C_CALL':
                self.cw.writeCall(parser.arg1(), parser.arg2())

if __name__ == "__main__":
    import sys

    filepath = sys.argv[1]
    Main(filepath)
