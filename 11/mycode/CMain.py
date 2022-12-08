
class Main(object):
    def __init__(self, filepath):
        self.jackfiles = []
        self.fileOrDir(filepath)
        for file in self.jackfiles:
            tokenizer = Tokenizer(file)
            outputname = file.split('.')[0]+".00.xml"
            compEngine = CompilationEngine(tokenizer, outputname)

    def fileOrDir(self, filepath):
        if '.jack' in filepath:
            self.jackfiles = [filepath]
        else:
            pathelements = filepath.split('/')
            for root, dirs, files in os.walk(filepath):
                for file in files:
                    if ".jack" in file:
                        self.jackfiles.append(root + '/' + file)

if __name__ == "__main__":
    import os
    import sys
    from JackTokenizer import Tokenizer
    from CompilationEngine import CompilationEngine
    filepath = sys.argv[1]
    Main(filepath)
