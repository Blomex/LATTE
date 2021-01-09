from antlr4.error.ErrorListener import ErrorListener
import sys
from antlr4.error.ErrorStrategy import DefaultErrorStrategy
from antlr4.error.Errors import InputMismatchException
from antlr4 import Parser, RecognitionException


class ParserErrorListener(ErrorListener):

    def syntaxError(self, recognizer, offending_symbol, line, column, msg, e):
        print("ERROR", file=sys.stderr)
        print("Parse error at line {}, column {} : {}".format(line, column, msg), file=sys.stderr)
        sys.exit(1)


class ParserErrorHandler(DefaultErrorStrategy):
    def recover(self, recognizer: Parser, e: RecognitionException):
        raise (InputMismatchException(recognizer))

    def recoverInline(self, recognizer: Parser):
        raise (InputMismatchException(recognizer))

    def senc(self, recognizer: Parser):
        pass