import sys
import os.path
from antlr4 import *
sys.path.append(os.path.dirname(sys.path[0]))
from src.CodeGenerator import CodeGenerator
from src.LatteLexer import LatteLexer
from src.LatteParser import LatteParser
from src.LatteReturnChecker import LatteReturnChecker
from src.LatteSemanticAnalyzer import LatteSemanticAnalyzer
from src.ParserErrorListener import ParserErrorListener, ParserErrorHandler
from src.CompileTimeErrors import CompileException


def main(argv):
    if len(argv) == 2:
        file = argv[1]
        filename, file_extension = os.path.splitext(file)
        result_file_path = filename + ".ll"
        text = FileStream(file)
        lexer = LatteLexer(text)
        stream = CommonTokenStream(lexer)
        parser = LatteParser(stream)
        parser.removeErrorListeners()
        parser.addErrorListener(ParserErrorListener())
        parser._errHandler = ParserErrorHandler()
        tree = parser.program()
        # need to pass name to visitor, to create class with such name
        try:
            ast = LatteSemanticAnalyzer().visitProgram(tree)
            ast2 = LatteReturnChecker().visitProgram(tree)
            codegen = CodeGenerator(file=result_file_path).visitProgram(tree)
            print("OK", file=sys.stdout)
            print(tree.toStringTree(recog=parser))
            return 0
        except CompileException as e:
            print("ERROR", file=sys.stderr)
            print(e, file=sys.stderr)
            return 1
    else:
        print("Wrong number of arguments. 1 argument expected.")
        return 1


if __name__ == '__main__':
    print(sys.path)
    sys.exit(main(sys.argv))
