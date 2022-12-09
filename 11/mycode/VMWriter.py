class VMWriter(object):
    def __init__(self, file):
        outputname = file.split('.')[0]+'my.vm'
        self.fhand = open(outputname, "w")


    def writePush(self, segment, index):
        self.fhand.write("PUSH " + segment + ' ' + str(index))

    def writePop(self, segment, index):
        self.fhand.write("POP " + segment + ' ' + str(index))

    def WriteArithmetic(self, command):
        self.fhand.write(command)

    def WriteLabel(self, label):
        self.fhand.write('label '+ label)

    def WriteGoto(self, label):
        self.fhand.write("goto "+ label)

    def WriteIf(self, label):
        self.fhand.write('if-goto '+ label)

    def writeCall(self, name, args):
        self.fhand.write('call ' + name + ' ' + str(args))

    def writeFunction(self, name, nLocals):
        self.fhand.write('function ' + name + ' ' + str(nLocals))

    def writeReturn(self):
        self.fhand.write('return')

    def close(self):
        self.fhand.close()


import os
