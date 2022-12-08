import os

class Parser:

    def __init__(self, path):
        fhand = open(path)
        self.file = fhand.readlines()
        self.cleanFile()
        self.commandindex=0
        self.totalcommands = 0
        for line in self.file:
            self.totalcommands = self.totalcommands+1
        self.currentcommand = None

    def hasMoreCommands(self):
        return self.totalcommands - self.commandindex > 0


#need to call advance once to load the first current command
    def advance(self):
        if self.hasMoreCommands() == True:
            self.currentcommand = self.file[self.commandindex]
            self.commandindex = self.commandindex + 1



    def cleanFile(self):
        list = []
        for line in self.file:
            line = line.strip()
            if line == '':
                continue
            elif line[0] == '/':
                continue
            else:
                list.append(line)
        self.file = list


    def commandType(self):
        if self.currentcommand.find('push') != -1:
            return('C_PUSH')
        elif self.currentcommand.find('pop') != -1:
            return('C_POP')
        elif self.currentcommand.find('label') != -1:
            return('C_LABEL')
        elif self.currentcommand.find('goto') != -1:
            return('C_GOTO')
        elif self.currentcommand.find('if') != -1:
            return('C_IF')
        elif self.currentcommand.find('function') != -1:
            return('C_FUNCTION')
        elif self.currentcommand.find('return') != -1:
            return('C_RETURN')
        elif self.currentcommand.find('call') != -1:
            return('C_CALL')
        else:
            return('C_ARITHMETIC')
            #not sure if catching everything else with arithmetic is a good idea of not but...

    def arg1(self):
        #this function does not control when it is called,
        #but it should not be called when the current command is a C_RETURN
        if self.commandType() == 'C_ARITHMETIC':
            return self.currentcommand
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
