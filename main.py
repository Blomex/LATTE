import sys
import os
from antlr4 import *
from LatteLexer import LatteLexer
from LatteParser import LatteParser
from LatteReturnChecker import LatteReturnChecker
from LatteSemanticAnalyzer import LatteSemanticAnalyzer
from ParserErrorListener import ParserErrorListener, ParserErrorHandler
from CompileTimeErrors import CompileException
from antlr4.error.ErrorStrategy import BailErrorStrategy
def main(argv):
    # text = InputStream(input(">"))
    if len(argv) == 2:
        file = argv[1]
        filename, file_extension = os.path.splitext(file)
        result_file_path = filename + ".j"
        text = FileStream(file)
        lexer = LatteLexer(text)
        stream = CommonTokenStream(lexer)
        parser = LatteParser(stream)
        parser.removeErrorListeners()
        parser.addErrorListener(ParserErrorListener())
        parser._errHandler = ParserErrorHandler()
        tree = parser.program()
        # need to pass name to visitor, to create class with such name
        #name = os.path.basename(file)
        try:
           ast = LatteSemanticAnalyzer().visitProgram(tree)
           ast2 = LatteReturnChecker().visitProgram(tree)
           print("OK", file=sys.stdout)
           print(tree.toStringTree(recog=parser))
           return 0
        except CompileException as e:
            print("ERROR", file=sys.stderr)
            print(e, file=sys.stderr)
            #raise e
        # if parser.getNumberOfSyntaxErrors() == 0:
        #     result_file = open(result_file_path, "w+")
        #     for line in ast:
        #         print(line, file=result_file)
        #     result_file.close()
        #     sys.exit(0)
        # else:
        #     print("Code generation failed due to parsing error", file=sys.stderr)
        #     sys.exit(1)
    else:
        print("Wrong number of arguments. 1 argument expected.")
        #ast = InstantVisitor().visitCompileUnit(tree)
        #value = EvaluateExpressionVisitor().visit(ast)
        #print('=', value)
if __name__ == '__main__':
    main(sys.argv)
