import os
from VMParser import Parser
from CodeWriter import CodeWriter
from ExtractName import extractName

path = input("Enter path: ")
outputfilename = extractName(path)
print(outputfilename)
codewriter = CodeWriter(outputfilename)

if os.path.isfile(path):
    file=open(path)
    parser = Parser(path)
elif os.path.isdir(path):
    for file in os.listdir(path):
        if file.find('.vm') != -1:
            path = path+"/"+file
            parser = Parser(path)
else:
    print("Golly-gee willickers.")

while parser.hasMoreCommands() == True:
    parser.advance()
    print(parser.arg2())
    print(parser.commandType())



# path = input('Please input absolute path: ')
# if os.path.isfile(path):
#     file=open(path)
#     for char in file:
#         print(char)
# elif os.path.isdir(path):
#     i=1
#     for file in os.listdir(path):
#         program = open(file)
#         for line in program:
#             print(line)
#
# else:
#     print("Golly-gee willickers.")
