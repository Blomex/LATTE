import sys
import os
from antlr4 import *

from CodeGenerator import CodeGenerator
from LatteLexer import LatteLexer
from LatteParser import LatteParser
from LatteReturnChecker import LatteReturnChecker
from LatteSemanticAnalyzer import LatteSemanticAnalyzer
from ParserErrorListener import ParserErrorListener, ParserErrorHandler
from CompileTimeErrors import CompileException
from antlr4.error.ErrorStrategy import BailErrorStrategy


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
    sys.exit(main(sys.argv))
