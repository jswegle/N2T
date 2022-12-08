#maybe get rid of this empty line
class parser:

    def __init__(self, filename):
    #creates variables for later use
        self.currentcommand = None
        self.index = 0
    #gets out first list from the filename
        try:
            fhand=open(filename)
        except:
            print("Fuck you, asshole.")
            exit()
        self.commands=fhand.readlines()
        self.cleanlist()

    def cleanlist(self):
        #takes the left side of any commented line -- the part we want
        self.commands = [com.split("//")[0] for com in self.commands]
        #strips the /n character from each line
        self.commands = [com.strip() for com in self.commands]
        self.removeempty()

    def removeempty(self):
        #removes any empty lines
        cleancommands=[]
        for line in self.commands:
            if line != '':
                cleancommands.append(line)
        self.commands = cleancommands

    def hasmorecommands(self):
        return self.index < len(self.commands)

    def advance(self):
        if self.hasmorecommands():
            self.currentcommand = self.commands[self.index]
            self.index = self.index+1
        #print(self.currentcommand)

    def printindex(self):
        print(self.index)

    def commandtype(self, comm):
        if (comm[0] == '@'):
            return 'A_COMMAND'
        if (comm[0] == '('):
            return 'L_COMMAND'
        else:
            return 'C_COMMAND'


    def symbol(self, comm):
        if self.commandtype(comm) == 'A_COMMAND':
            return comm[1:]
        if self.commandtype(comm) == 'L_COMMAND':
            return comm[1:-1]
        else:
            return "Invalid command type"


    def dest(self, comm):
        if self.commandtype(comm) == 'C_COMMAND':
            if '=' in comm:
                equalindex = comm.rfind('=')
                return comm[0:equalindex]
            else:
                return "null"
        else:
            return "Invalid command type"

    def comp(self, comm):
        if self.commandtype(comm) == "C_COMMAND":
            if ';' in comm:
                semiindex = comm.rfind(";")
                return comm[0:semiindex]
            elif '=' in comm:
                equalindex = comm.rfind('=')
                return comm[equalindex+1:]
            else:
                return "Something's fucked up with this command bro"
        else:
            return "Invalid command type"

    def jump(self, comm):
        if self.commandtype(comm) == "C_COMMAND":
            if ';' in comm:
                semiindex = comm.rfind(";")
                return comm[semiindex+1:]
            else:
                return "null"
        else:
            return "Invalid command type"


    def print(self):
    #for debugging purposes
        for line in self.commands:
            print(line)
