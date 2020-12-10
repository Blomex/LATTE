import sys
class CompileException(Exception):
    def __init__(self, ctx):
        self.ctx = ctx
        self.line = ctx.start.line
        self.column = ctx.start.column
    def __str__(self):
        error = "Error {} at line {}, column {}: {}".format(type(self).__name__, self.line, self.column, self.ctx.getText())
        return error


class UnsupportedOperand(CompileException):
    def __init__(self, ctx):
        super().__init__(ctx)


class UnknownType(CompileException):
    def __init__(self, ctx):
        super().__init__(ctx)


class InvalidVariableDeclaration(CompileException):
    def __init__(self, ctx):
        super().__init__(ctx)

class MissingMainDeclaration(CompileException):
    def __init__(self, ctx):
        super().__init__(ctx)

class InvalidReturnType(CompileException):
    def __init__(self, ctx):
        super().__init__(ctx)

class ReturnUnreachable(CompileException):
    def __init__(self, ctx):
        super().__init__(ctx)

class UndeclaredFunction(CompileException):
    def __init__(self, ctx):
        super().__init__(ctx)

class UndeclaredVariable(CompileException):
    def __init__(self, ctx):
        super().__init__(ctx)

class MultipleDefinitionsOfFunction(CompileException):
    def __init__(self, ctx):
        super().__init__(ctx)

class MultipleDefinitionsOfVariable(CompileException):
    def __init__(self, ctx):
        super().__init__(ctx)

class TypeMismatch(CompileException):
    def __init__(self, ctx):
        super().__init__(ctx)


class UnreachableCode(CompileException):
    def __init__(self, ctx):
        super().__init__(ctx)

class InvalidNumberOfArguments(CompileException):
    def __init__(self, ctx):
        super().__init__(ctx)
class MultipleDefinitionsOfClass(CompileException):
    def __init__(self, ctx):
        super().__init__(ctx)
class RhsAssignment(CompileException):
    def __init__(self, ctx):
        super().__init__(ctx)

class InvalidAttributeAcces(CompileException):
    def __init__(self, ctx):
        super().__init__(ctx)