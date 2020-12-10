# Generated from Latte.g4 by ANTLR 4.8
from antlr4 import *

if __name__ is not None and "." in __name__:
    from .LatteParser import LatteParser
else:
    from LatteParser import LatteParser

from copy import deepcopy
from CompileTimeErrors import *

DEBUG = False


def printd(*args):
    if DEBUG:
        print(*args)


class LatteSemanticAnalyzer(ParseTreeVisitor):
    def __init__(self):
        # global variables = variables outside current block
        self.block_variables = {}
        self.global_variables = {}
        self.classes = {}
        self.class_attributes = {}
        self.class_methods = {}
        self.errors = []
        self.current_type = None
        # basic types + void
        self.types = ['boolean', 'int', 'string', 'void']
        # just basic types used for expressions
        self.basic_types = ['boolean', 'int', 'string']
        self.default_super_class = '#latte.lang.object'
        # there is no superclass of base class
        self.classes[self.default_super_class] = None

        self.class_attributes[self.default_super_class] = {}
        self.class_methods[self.default_super_class] = {}
        # Some methods available through runtime
        self.class_methods[self.default_super_class]['printInt'] = ('void', ['int'])
        self.class_methods[self.default_super_class]['readInt'] = ('int', [])
        self.class_methods[self.default_super_class]['printString'] = ('void', ['string'])
        self.class_methods[self.default_super_class]['readString'] = ('string', [])
        self.class_methods[self.default_super_class]['error'] = ('void', [])
        # Current class context, will be used during static analysis
        self.current_class = self.default_super_class

    def visitProgram(self, ctx: LatteParser.ProgramContext):
        printd("inside program")
        functions = ctx.getChildren(predicate=lambda c: isinstance(c, LatteParser.FunTopDefContext))
        functions = [fun.fundef() for fun in functions]

        # register functions
        self._register_methods(ctx, functions)
        # class can be extended by another class, or not.
        class_list = [i for i in ctx.getChildren(predicate=lambda c: isinstance(c, LatteParser.ClassDefContext))]
        extend_class_list = [c for c in ctx.getChildren(predicate=lambda c: isinstance(c, LatteParser.ClassExtDefContext))]
        self._defined = False
        for c in class_list:
            self.visit(c)
        self._defined = True
        for c in class_list:
            self.visit(c)
        self._defined = False
        for ec in extend_class_list:
            self.visit(ec)
        self._defined = True
        for ec in extend_class_list:
            self.visit(ec)

        for function in functions:
            self.visit(function)
            if function.ID().getText() == 'main':
                ret_type, par_types = self.class_methods[self.default_super_class]['main']
                if ret_type != 'int':
                    raise InvalidReturnType(function)
                if par_types != []:
                    raise InvalidNumberOfArguments(function)
        if 'main' not in self.class_methods[self.default_super_class]:
            raise MissingMainDeclaration(ctx)
        return

    # Visit a parse tree produced by LatteParser#arg.
    def visitArg(self, ctx: LatteParser.ArgContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LatteParser#block.
    def visitBlock(self, ctx: LatteParser.BlockContext):
        printd("inside block")
        if ctx.stmt():
            # Deepcopy required to copy 'inside' lists
            global_variables = deepcopy(self.global_variables)
            local_variables = deepcopy(self.block_variables)

            self.global_variables.update(self.block_variables)
            self.block_variables = {}
            printd(global_variables, local_variables)
            self.visitChildren(ctx)
            self.global_variables = global_variables
            self.block_variables = local_variables
        else:
            printd("empty block")

    # Visit a parse tree produced by LatteParser#Empty.
    def visitEmpty(self, ctx: LatteParser.EmptyContext):
        printd("inside empty")
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LatteParser#BlockStmt.
    def visitBlockStmt(self, ctx: LatteParser.BlockStmtContext):
        printd("inside block stmt")
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LatteParser#Decl.
    def visitDecl(self, ctx: LatteParser.DeclContext):
        printd("inside decl")
        # TODO FIXUP
        # Get type of decl
        self.item_current_type = ctx.type_().getText()
        # Decl can't be void
        if self.item_current_type == 'void':
            raise InvalidVariableDeclaration(ctx)
        printd(self.classes)
        printd(self.item_current_type)
        # make sure type is declarred
        if self.item_current_type not in self.basic_types and self.item_current_type not in self.classes:
            raise UnknownType(ctx)
        # visit every declared variable
        for item in ctx.getChildren():
            printd(item.getText())
            self.visit(item)
        del self.item_current_type
        return

    # Visit a parse tree produced by LatteParser#Ass.
    def visitAss(self, ctx: LatteParser.AssContext):
        # get types of left and right side
        printd("inside assignment")
        exprs = ctx.expr()
        left = self.visit(exprs[0])
        right = self.visit(exprs[1])
        # Check if type is the same
        printd("assignment types{} {} ".format(left, right))
        if not self._is_same_type(right, left):
            raise TypeMismatch(ctx)
        # We can only assign things to variables or class attributes
        if isinstance(exprs[0], LatteParser.EIdContext) or isinstance(exprs[0], LatteParser.EFieldAccesContext):
            printd("return from ass")
            return
        else:
            raise RhsAssignment(ctx)

    # Visit a parse tree produced by LatteParser#Incr.
    def visitIncr(self, ctx: LatteParser.IncrContext):
        type = self.visit(ctx.expr())
        if type != 'int':
            raise UnsupportedOperand(ctx)

    # Visit a parse tree produced by LatteParser#Decr.
    def visitDecr(self, ctx: LatteParser.DecrContext):
        type = self.visit(ctx.expr())
        if type != 'int':
            raise UnsupportedOperand(ctx)

    # Visit a parse tree produced by LatteParser#Ret.
    def visitRet(self, ctx: LatteParser.RetContext):
        printd("inside ret")
        ret_type = self.visit(ctx.expr())
        if ret_type == 'void':
            # Not allowed, we are supposed to use visitVRet in those instances
            raise InvalidReturnType(ctx)
        # current_type = currently expected return type
        if not self._is_same_type(ret_type, self.current_type):
            raise InvalidReturnType(ctx)
        return self.current_type

    # Visit a parse tree produced by LatteParser#VRet.
    def visitVRet(self, ctx: LatteParser.VRetContext):
        printd("inside vret, type = {}".format(self.current_type))
        if self.current_type != "void":
            raise InvalidReturnType(ctx)

    # Visit a parse tree produced by LatteParser#Cond.
    def visitCond(self, ctx: LatteParser.CondContext):
        type = self.visit(ctx.expr())
        if type != 'boolean':
            raise TypeMismatch
        else:
            self.visit(ctx.stmt())

    # Visit a parse tree produced by LatteParser#CondElse.
    def visitCondElse(self, ctx: LatteParser.CondElseContext):
        type = self.visit(ctx.expr())
        if type != 'boolean':
            raise TypeMismatch(ctx.expr())
        for stmt in ctx.stmt():
            self.visit(stmt)

    # Visit a parse tree produced by LatteParser#While.
    def visitWhile(self, ctx: LatteParser.WhileContext):
        type = self.visit(ctx.expr())
        if type != 'boolean':
            raise TypeMismatch(ctx.expr())
        else:
            self.visit(ctx.stmt())
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LatteParser#SExp.
    def visitSExp(self, ctx: LatteParser.SExpContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LatteParser#Int.
    def visitInt(self, ctx: LatteParser.IntContext):
        printd("visited int context")
        return "int"

    # Visit a parse tree produced by LatteParser#Str.
    def visitStr(self, ctx: LatteParser.StrContext):
        return "string"

    # Visit a parse tree produced by LatteParser#Bool.
    def visitBool(self, ctx: LatteParser.BoolContext):
        return "bool"

    # Visit a parse tree produced by LatteParser#Void.
    def visitVoid(self, ctx: LatteParser.VoidContext):
        return "void"

    # Visit a parse tree produced by LatteParser#item.
    def visitItem(self, ctx: LatteParser.ItemContext):
        printd("inside item")
        ident = ctx.ID().getText()
        if ident in self.block_variables:
            raise MultipleDefinitionsOfVariable(ctx)
        if ctx.expr():
            expr_type = self.visit(ctx.expr())
            printd(expr_type, self.item_current_type)
            if not self._is_same_type(expr_type, self.item_current_type):
                raise TypeMismatch(ctx)
        printd(self.block_variables)
        self.block_variables[ident] = self.item_current_type
        printd(self.block_variables)

    # Visit a parse tree produced by LatteParser#EId.
    def visitEId(self, ctx: LatteParser.EIdContext):
        printd("inside EId")
        ident = ctx.ID().getText()
        printd("ident is {}".format(ident))
        itype = self._find_ident_type(ctx, ident)
        printd("type is {}".format(itype))
        ctx.expr_type = itype
        return itype

    # Visit a parse tree produced by LatteParser#FunTopDef.
    def visitFunTopDef(self, ctx: LatteParser.FunTopDefContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LatteParser#ClassDef.
    def visitClassDef(self, ctx: LatteParser.ClassDefContext):
        # this class is not extended by anything, so its extended by our default class
        printd("inside visitClassDef {}".format(ctx.getText()))
        base_class = ctx.ID().getText()
        print("self._defined is {}".format(self._defined))
        if self._defined is False:
            self._add_class_defition(ctx, base_class, self.default_super_class)
        else:
            self._verify_class(ctx, base_class)
        return
    # Visit a parse tree produced by LatteParser#ClassExtDef.
    def visitClassExtDef(self, ctx: LatteParser.ClassExtDefContext):
        classes = ctx.ID()  # List of classes, first is base, second is super
        if self._defined is False:
            self._add_class_defition(ctx, classes[0].getText(), classes[1].getText())
        else:
            self._verify_class(ctx, classes[0].getText())
        return
    # Visit a parse tree produced by LatteParser#classattr.
    def visitClassattr(self, ctx: LatteParser.ClassattrContext):
        # save attributes
        type = ctx.type_().getText()
        # can be list of IDS according to grammar
        attributes_ids = [a.getText() for a in ctx.ID()]
        if type == 'void':
            raise InvalidVariableDeclaration(ctx)
        elif type not in self.classes and type not in self.basic_types:
            raise UnknownType(ctx)
        else:
            for a in attributes_ids:
                if a in self.class_attributes:
                    raise MultipleDefinitionsOfVariable(ctx)
                self.class_attributes[self.current_class][a] = type

    # Visit a parse tree produced by LatteParser#classfun.
    def visitClassfun(self, ctx: LatteParser.ClassfunContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LatteParser#FunDef.
    def visitFunDef(self, ctx: LatteParser.FunDefContext):
        # We are in method definition
        # We need to get method name, type and arguments
        type = ctx.type_().getText()
        name = ctx.ID().getText()
        arg_types = []
        arg_ids = []
        if ctx.arg():  # function has arguments, parse them
            # only get argument types, not identifiers
            arg_types = ctx.arg().getChildren(predicate=lambda c: isinstance(c, ParserRuleContext))
            arg_types = [a.getText() for a in arg_types]
            arg_ids = ctx.arg().ID()
            arg_ids = [a.getText() for a in arg_ids]
        printd(arg_types, arg_ids)
        printd(type, name, arg_types)

        # unknown type
        if type not in self.basic_types and type not in self.classes and type != 'void':
            raise UnknownType(ctx.type_())
        for arg_type in arg_types:
            if arg_type == 'void':
                raise InvalidVariableDeclaration(ctx)
            if arg_type not in self.basic_types and arg_type not in self.classes:
                raise UnknownType(ctx.type_())
        for i, arg_id in enumerate(arg_ids):
            if arg_id in self.block_variables:
                raise MultipleDefinitionsOfVariable(ctx)
            self.block_variables[arg_id] = arg_types[i]
        # Validate function execution
        self.current_type = type
        self.visit(ctx.block())
        self.block_variables = {}
        del self.current_type
        return

    # Visit a parse tree produced by LatteParser#Class.
    def visitClass(self, ctx: LatteParser.ClassContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LatteParser#EFunCall.
    def visitEFunCall(self, ctx: LatteParser.EFunCallContext):
        # make sure it has correct types
        printd("inside EFunCall")
        name = ctx.ID().getText()
        arg_types = [self.visit(exp) for exp in ctx.expr()]
        fun_ret, fun_types = self._find_method_type(ctx, name)
        self._verify_function_arguments(ctx, arg_types, fun_types)
        ctx.expr_type = fun_ret
        return fun_ret

    # Visit a parse tree produced by LatteParser#ERelOp.
    def visitERelOp(self, ctx: LatteParser.ERelOpContext):
        [ltype, op, rtype] = self._get_operators(ctx)
        if ltype == 'int' or type(op) in {LatteParser.EqContext, LatteParser.NeqContext}:
            ctx.expr_type = 'boolean'
            return 'boolean'
        else:
            raise UnsupportedOperand(op)

    # Visit a parse tree produced by LatteParser#ETrue.
    def visitETrue(self, ctx: LatteParser.ETrueContext):
        ctx.expr_type = 'boolean'
        return ctx.expr_type

    # Visit a parse tree produced by LatteParser#ENullCast.
    def visitENullCast(self, ctx: LatteParser.ENullCastContext):
        type = ctx.type_().getText()
        if type not in self.classes:
            raise UnknownType(ctx)
        ctx.expr_type = type
        return type

    # Visit a parse tree produced by LatteParser#EOr.
    def visitEOr(self, ctx: LatteParser.EOrContext):
        [ltype, op, rtype] = self._get_operators(ctx)
        if ltype != 'boolean':
            raise UnsupportedOperand(ctx)
        ctx.expr_type = 'boolean'
        return ctx.expr_type

    # Visit a parse tree produced by LatteParser#EInt.
    def visitEInt(self, ctx: LatteParser.EIntContext):
        ctx.exprType = 'int'
        return 'int'

    # Visit a parse tree produced by LatteParser#EUnOp.
    def visitEUnOp(self, ctx: LatteParser.EUnOpContext):
        for c in ctx.getChildren():
            printd(c.getText())
        op, rtype = (self.visit(c) for c in ctx.getChildren())
        printd("visitng EUnOp, {} {}".format(op.getText(), rtype))
        if rtype == 'int' and type(op) == LatteParser.NegContext:
            ctx.expr_type = 'int'
            return 'int'
        if rtype == 'boolean' and type(op) == LatteParser.NotContext:
            ctx.expr_type = 'boolean'
            return 'boolean'
        raise UnsupportedOperand(op)

    # Visit a parse tree produced by LatteParser#ENewClass.
    def visitENewClass(self, ctx: LatteParser.ENewClassContext):
        printd("inside ENewClass")
        class_name = ctx.ID().getText()
        printd(class_name)
        if class_name not in self.classes:
            raise UnknownType(ctx)
        ctx.expr_type = class_name
        return class_name

    # Visit a parse tree produced by LatteParser#EStr.
    def visitEStr(self, ctx: LatteParser.EStrContext):
        ctx.expr_type = 'string'
        return 'string'

    # Visit a parse tree produced by LatteParser#EMulOp.
    def visitEMulOp(self, ctx: LatteParser.EMulOpContext):
        printd("inside mul")
        [ltype, op, rtype] = self._get_operators(ctx)
        if ltype != 'int':
            raise UnsupportedOperand(ctx)
        ctx.expr_type = 'int'
        return 'int'

    # Visit a parse tree produced by LatteParser#EAnd.
    def visitEAnd(self, ctx: LatteParser.EAndContext):
        [ltype, op, rtype] = self._get_operators(ctx)
        if ltype == 'boolean':
            ctx.expr_type = ltype
            return ltype
        raise UnsupportedOperand(ctx)

    # Visit a parse tree produced by LatteParser#EFieldAcces.
    def visitEFieldAcces(self, ctx: LatteParser.EFieldAccesContext):
        # expr '.' expr
        exprs = ctx.expr()
        type = self.visit(exprs[0])
        printd("type of obj: {}".format(type))
        expr = exprs[1]
        printd(expr.getText())
        actual_class = self.current_class
        # lhs type should be class, cannot be primitive type
        if type in self.basic_types or type == 'void':
            raise InvalidAttributeAcces(ctx)
        # possible access:
        # 1) object.attribute
        # 2) object.method()
        # 3) object.another_object.(1 or 2 or 3)
        # 1)
        if isinstance(expr, LatteParser.EIdContext):
            printd("inside EfieldAcces EIdContext")
            ident = expr.ID().getText()
            self.current_class = type
            printd("current class to check for method: {}".format(self.current_class))
            ctx.expr_type = self._find_attribute_type(ctx, ident)
            self.current_class = actual_class
            return ctx.expr_type
        elif isinstance(expr, LatteParser.EFunCallContext):
            printd("inside EFieldAcces EfunCallContext")
            ident = expr.ID().getText()
            printd(ident)
            x = [x.getText() for x in expr.expr()]
            printd(x)
            printd("visiting args " + self.current_class)
            args = [self.visit(arg) for arg in expr.expr()]
            self.current_class = type
            printd("current class to check for method: {}".format(self.current_class))
            ctx.expr_type, param_types = self._find_method_type(ctx, ident)
            printd("expected/ correct args: {} | {} ".format(args, param_types))
            self.current_class = actual_class
            self._verify_function_arguments(ctx, args, param_types)
            self.current_class = actual_class
            return ctx.expr_type
        elif isinstance(expr, LatteParser.EFieldAccesContext):
            self.current_class = type
            ctx.expr_type = self.visit(expr)
            self.current_class = actual_class
            return ctx.expr_type
        return ctx.expr_type

    # Visit a parse tree produced by LatteParser#EParen.
    def visitEParen(self, ctx: LatteParser.EParenContext):
        res = self.visit(ctx.expr())
        return res

    # Visit a parse tree produced by LatteParser#EFalse.
    def visitEFalse(self, ctx: LatteParser.EFalseContext):
        ctx.expr_type = 'boolean'
        return ctx.expr_type

    # Visit a parse tree produced by LatteParser#EAddOp.
    def visitEAddOp(self, ctx: LatteParser.EAddOpContext):
        printd("inside add")
        [ltype, op, rtype] = self._get_operators(ctx)
        if ltype == 'int':
            ctx.expr_type = 'int'
            printd(ltype, rtype)
            return 'int'
        elif ltype == 'string' and type(op) == LatteParser.AddContext:
            ctx.expr_type = 'string'
            return 'string'
        raise UnsupportedOperand(ctx)

    # Visit a parse tree produced by LatteParser#Not.
    def visitNot(self, ctx: LatteParser.NotContext):
        return ctx

    # Visit a parse tree produced by LatteParser#Neg.
    def visitNeg(self, ctx: LatteParser.NegContext):
        return ctx

    # Visit a parse tree produced by LatteParser#Add.
    def visitAdd(self, ctx: LatteParser.AddContext):
        return ctx

    # Visit a parse tree produced by LatteParser#Sub.
    def visitSub(self, ctx: LatteParser.SubContext):
        return ctx

    # Visit a parse tree produced by LatteParser#Mul.
    def visitMul(self, ctx: LatteParser.MulContext):
        return ctx

    # Visit a parse tree produced by LatteParser#Div.
    def visitDiv(self, ctx: LatteParser.DivContext):
        return ctx

    # Visit a parse tree produced by LatteParser#Mod.
    def visitMod(self, ctx: LatteParser.ModContext):
        return ctx

    # Visit a parse tree produced by LatteParser#Lt.
    def visitLt(self, ctx: LatteParser.LtContext):
        return ctx

    # Visit a parse tree produced by LatteParser#Le.
    def visitLe(self, ctx: LatteParser.LeContext):
        return ctx

    # Visit a parse tree produced by LatteParser#Gt.
    def visitGt(self, ctx: LatteParser.GtContext):
        return ctx

    # Visit a parse tree produced by LatteParser#Ge.
    def visitGe(self, ctx: LatteParser.GeContext):
        return ctx

    # Visit a parse tree produced by LatteParser#Eq.
    def visitEq(self, ctx: LatteParser.EqContext):
        return ctx

    # Visit a parse tree produced by LatteParser#Neq.
    def visitNeq(self, ctx: LatteParser.NeqContext):
        return ctx

    def _get_operators(self, ctx):
        # Get types
        printd("inside get op")
        [ltype, op, rtype] = [self.visit(c) for c in ctx.getChildren()]
        printd(self.global_variables)
        for c in ctx.getChildren():
            printd(c.getText())
        if not self._is_same_type(ltype, rtype) and not self._is_same_type(rtype, ltype):
            raise TypeMismatch(ctx)
        elif ltype == 'void':
            return UnsupportedOperand(ctx)
        elif ltype not in self.basic_types and type(op) not in {LatteParser.EqContext, LatteParser.NeqContext}:
            raise UnsupportedOperand(ctx)
        return [ltype, op, rtype]
        pass

    def _is_same_type(self, x, y):
        printd("inside same type {} {} ".format(x, y))
        if x in self.basic_types and y in self.basic_types:
            return x == y
        elif x in self.classes and y in self.classes:
            class_1 = x
            while class_1 != self.classes[self.default_super_class]:
                if class_1 == y:
                    printd("same type")
                    return True
                class_1 = self.classes[class_1]
        printd("not same type")
        return False

    def _register_methods(self, ctx, functions):
        # for every method we will save parameter types and return value
        # current class is available under self.current_class
        # functions is list of method for currently analyzed class
        for f in functions:
            type = f.type_().getText()
            name = f.ID().getText()
            if f.arg() is not None:
                # only parse types, ignore symbols
                arg_types = f.arg().getChildren(predicate=lambda c: isinstance(c, ParserRuleContext))
            else:
                arg_types = []
            arg_types = [x.getText() for x in arg_types]
            # Check if function is already declared. If not, add it to declarations
            if name in self.class_methods[self.current_class]:
                raise MultipleDefinitionsOfFunction(f)
            else:
                self.class_methods[self.current_class][name] = (type, arg_types)

    def _add_class_defition(self, ctx, base_class, super_class):
        printd("inside add class definition")
        if base_class in self.classes:
            raise MultipleDefinitionsOfClass
        else:
            self.classes[base_class] = super_class
            self.class_methods[base_class] = {}
            self.class_attributes[base_class] = {}
            # workaround for 'self'
            self.class_attributes[base_class]['self'] = base_class
            self.current_class = self.default_super_class
    def _verify_class(self, ctx, base_class):
            printd("inside class veirification")
            self.current_class = base_class
            methods = [method.fundef() for method in ctx.classfun()]
            printd("methods: {}".format(methods))
            self._register_methods(ctx, methods)
            self.visitChildren(ctx)
            self.current_class = self.default_super_class
    def _find_ident_type(self, ctx, ident):
        printd("inside ident type {}".format(ident))
        if ident in self.block_variables:
            return self.block_variables[ident]
        if ident in self.global_variables:
            return self.global_variables[ident]
        return self._find_attribute_type(ctx, ident)

    def _find_attribute_type(self, ctx, ident):
        printd("inside find attribute, class and ident: {} {} ".format(self.current_class, ident))
        current_class = self.current_class
        while current_class != self.classes[self.default_super_class]:
            if ident in self.class_attributes[current_class]:
                return self.class_attributes[current_class][ident]
            current_class = self.classes[current_class]
        raise UndeclaredVariable(ctx)

    def _find_method_type(self, ctx, ident):
        current_class = self.current_class
        # find method in superclasses
        printd("finding method")
        while current_class != self.classes[self.default_super_class]:
            printd("current class: {}".format(current_class))
            if ident in self.class_methods[current_class]:
                printd("found method type: {}".format(self.class_methods[current_class][ident]))
                return self.class_methods[current_class][ident]
            else:
                current_class = self.classes[current_class]
        # If we didnt found method, it means it doesnt exist
        raise UndeclaredFunction(ctx)

    def _verify_function_arguments(self, ctx, args, param_types):
        # check if function parameters have correct type
        if len(args) != len(param_types):
            raise InvalidNumberOfArguments(ctx)
        else:
            for i in range(len(args)):
                if not self._is_same_type(args[i], param_types[i]):
                    raise TypeMismatch(ctx.expr(i))
        pass
# del LatteParser
