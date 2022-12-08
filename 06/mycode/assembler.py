from parser import parser
from code import (transdest, transcomp, transjump, tobinary)
from symboltable import SymbolTable

def firstpass(parser, st):
    ROMIndex = 0
    for command in parser.commands:
        if parser.commandtype(command) == "L_COMMAND":
            st.addEntry(parser.symbol(command), ROMIndex)
        else:
            ROMIndex = ROMIndex+1
    #st.print()

file = input("Name of file to translate: ")
parser = parser(file)
parser.cleanlist()
st = SymbolTable()
firstpass(parser, st)

#create output file
breakindex = file.find('.')
output = open(file[0:breakindex]+'.hack', 'w+')

while parser.hasmorecommands() :
    parser.advance()
    if parser.commandtype(parser.currentcommand) == "A_COMMAND":
        #if the a command is the raw number
        try:
            decimal = int(parser.symbol(parser.currentcommand))

            command = tobinary(decimal)

            output.write(command)
            output.write('\n')
        #if the a command is variable
        except:
            if not st.contains(parser.symbol(parser.currentcommand)):
                st.addEntry(parser.symbol(parser.currentcommand), st.nextopen)
                st.nextopen = st.nextopen+1
            decimal = st.getAddress(parser.symbol(parser.currentcommand))
        #decimal = int(parser.symbol(parser.currentcommand))
            command = tobinary(decimal)
            output.write(command)
            output.write('\n')
    elif parser.commandtype(parser.currentcommand) == "C_COMMAND":
        comp = parser.comp(parser.currentcommand)
        dest = parser.dest(parser.currentcommand)
        jump = parser.jump(parser.currentcommand)
        output.write('111')
        output.write(transcomp(comp))
        output.write(transdest(dest))
        output.write(transjump(jump))
        output.write('\n')

#st.print()
