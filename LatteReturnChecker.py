# Generated from Latte.g4 by ANTLR 4.8
from antlr4 import *

if __name__ is not None and "." in __name__:
    from .LatteParser import LatteParser
else:
    from LatteParser import LatteParser
from CompileTimeErrors import ReturnUnreachable
from LatteSemanticAnalyzer import printd
undefined = None
"""
class checks if return is reachable in every function.
return type is already guaranteed to be correct (it if exists) thanks to semantic analyzer
"""


class LatteReturnChecker(ParseTreeVisitor):

    def __init__(self):
        self._ret = False

    # Visit a parse tree produced by LatteParser#program.
    def visitProgram(self, ctx: LatteParser.ProgramContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LatteParser#FunTopDef.
    def visitFunTopDef(self, ctx: LatteParser.FunTopDefContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LatteParser#ClassDef.
    def visitClassDef(self, ctx: LatteParser.ClassDefContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LatteParser#ClassExtDef.
    def visitClassExtDef(self, ctx: LatteParser.ClassExtDefContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LatteParser#classattr.
    def visitClassattr(self, ctx: LatteParser.ClassattrContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LatteParser#classfun.
    def visitClassfun(self, ctx: LatteParser.ClassfunContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LatteParser#FunDef.
    def visitFunDef(self, ctx: LatteParser.FunDefContext):
        self._ret = False
        if ctx.type_().getText() != 'void':
            self.visitChildren(ctx)
            if not self._ret:
                raise ReturnUnreachable(ctx)
            self._ret = False

    # Visit a parse tree produced by LatteParser#arg.
    def visitArg(self, ctx: LatteParser.ArgContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LatteParser#block.
    def visitBlock(self, ctx: LatteParser.BlockContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LatteParser#Empty.
    def visitEmpty(self, ctx: LatteParser.EmptyContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LatteParser#BlockStmt.
    def visitBlockStmt(self, ctx: LatteParser.BlockStmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LatteParser#Decl.
    def visitDecl(self, ctx: LatteParser.DeclContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LatteParser#Ass.
    def visitAss(self, ctx: LatteParser.AssContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LatteParser#Incr.
    def visitIncr(self, ctx: LatteParser.IncrContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LatteParser#Decr.
    def visitDecr(self, ctx: LatteParser.DecrContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LatteParser#Ret.
    def visitRet(self, ctx: LatteParser.RetContext):
        self._ret = True

    # Visit a parse tree produced by LatteParser#VRet.
    def visitVRet(self, ctx: LatteParser.VRetContext):
        self._ret = True

    # Visit a parse tree produced by LatteParser#Cond.
    def visitCond(self, ctx: LatteParser.CondContext):
        if self._ret:
            return
        condition = self.visit(ctx.expr())
        printd("if result: {}".format(condition))
        if condition:
            printd("condition is true")
            self.visit(ctx.stmt())

    # Visit a parse tree produced by LatteParser#CondElse.
    def visitCondElse(self, ctx: LatteParser.CondElseContext):
        printd("inside if else")
        if self._ret:
            return
        condition = self.visit(ctx.expr())
        if condition == undefined:
            printd("condition is undefined")
            self.visit(ctx.stmt()[0])  # check if return is achieveable in this branch
            first = self._ret
            self._ret = False
            self.visit(ctx.stmt()[1])
            if not (first and self._ret):
                self._ret = False
        elif condition:
            self.visit(ctx.stmt()[0])
        else:
            self.visit(ctx.stmt()[1])

    # Visit a parse tree produced by LatteParser#While.
    def visitWhile(self, ctx: LatteParser.WhileContext):
        condition = self.visit(ctx.expr())
        if condition:
            self.visit(ctx.stmt())
            self._ret = True

    # Visit a parse tree produced by LatteParser#SExp.
    def visitSExp(self, ctx: LatteParser.SExpContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LatteParser#Int.
    def visitInt(self, ctx: LatteParser.IntContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LatteParser#Str.
    def visitStr(self, ctx: LatteParser.StrContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LatteParser#Bool.
    def visitBool(self, ctx: LatteParser.BoolContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LatteParser#Void.
    def visitVoid(self, ctx: LatteParser.VoidContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LatteParser#Class.
    def visitClass(self, ctx: LatteParser.ClassContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LatteParser#item.
    def visitItem(self, ctx: LatteParser.ItemContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LatteParser#EId.
    def visitEId(self, ctx: LatteParser.EIdContext):
        return undefined

    # Visit a parse tree produced by LatteParser#EFunCall.
    def visitEFunCall(self, ctx: LatteParser.EFunCallContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LatteParser#ERelOp.
    def visitERelOp(self, ctx: LatteParser.ERelOpContext):
        [left, op, right] = [self.visit(c) for c in ctx.getChildren()]
        if left == undefined or right == undefined:
            return undefined
        elif op == '==':
            return left == right
        elif op == '<':
            return left < right
        elif op == '<=':
            return left <= right
        elif op == '>':
            return left > right
        elif op == '>=':
            return left >= right
        elif op == '!=':
            return left != right

    # Visit a parse tree produced by LatteParser#ETrue.
    def visitETrue(self, ctx: LatteParser.ETrueContext):
        return True

    # Visit a parse tree produced by LatteParser#ENullCast.
    def visitENullCast(self, ctx: LatteParser.ENullCastContext):
        return None

    # Visit a parse tree produced by LatteParser#EOr.
    def visitEOr(self, ctx: LatteParser.EOrContext):
        [left, _op, right] = [self.visit(c) for c in ctx.getChildren()]
        if left is True or right is True:
            return True
        elif left is False and right is False:
            return False
        else:
            return undefined

    # Visit a parse tree produced by LatteParser#EInt.
    def visitEInt(self, ctx: LatteParser.EIntContext):
        printd("vising int, {}".format(ctx.getText()))
        return int(ctx.getText())

    # Visit a parse tree produced by LatteParser#EUnOp.
    def visitEUnOp(self, ctx: LatteParser.EUnOpContext):
        [op, right] = [self.visit(c) for c in ctx.getChildren()]
        if right == undefined:
            return undefined
        elif op == '-':
            return -right
        elif op == '!':
            return not right

    # Visit a parse tree produced by LatteParser#ENewClass.
    def visitENewClass(self, ctx: LatteParser.ENewClassContext):
        return undefined

    # Visit a parse tree produced by LatteParser#EStr.
    def visitEStr(self, ctx: LatteParser.EStrContext):
        printd("inside str {}".format(ctx.getText()[1:-1]))
        return ctx.getText()[1:-1]

    # Visit a parse tree produced by LatteParser#EMulOp.
    def visitEMulOp(self, ctx: LatteParser.EMulOpContext):
        [left, op, right] = [self.visit(c) for c in ctx.getChildren()]
        if left == undefined or right == undefined:
            return undefined
        elif op == '%':
            return left % right
        elif op == '*':
            return left * right
        elif op == '/':
            return left / right

    # Visit a parse tree produced by LatteParser#EAnd.
    def visitEAnd(self, ctx: LatteParser.EAndContext):
        [left, _op, right] = [self.visit(c) for c in ctx.getChildren()]
        if left == undefined or right == undefined:
            return undefined
        if left is True and right is True:
            return True
        elif left is False or right is False:
            return False
        printd("unreachable")

    # Visit a parse tree produced by LatteParser#EFieldAcces.
    def visitEFieldAcces(self, ctx: LatteParser.EFieldAccesContext):
        return undefined

    # Visit a parse tree produced by LatteParser#EParen.
    def visitEParen(self, ctx: LatteParser.EParenContext):
        return self.visit(ctx.expr())

    # Visit a parse tree produced by LatteParser#EFalse.
    def visitEFalse(self, ctx: LatteParser.EFalseContext):
        return False

    # Visit a parse tree produced by LatteParser#EAddOp.
    def visitEAddOp(self, ctx: LatteParser.EAddOpContext):
        [left, op, right] = [self.visit(c) for c in ctx.getChildren()]
        printd(left, op, right)
        if left == undefined or right == undefined:
            return undefined
        if op == '+':
            printd("result of add is {}".format(left + right))
            return left + right
        else:
            return left - right

    # Visit a parse tree produced by LatteParser#Not.
    def visitNot(self, ctx: LatteParser.NotContext):
        return ctx.getText()

    # Visit a parse tree produced by LatteParser#Neg.
    def visitNeg(self, ctx: LatteParser.NegContext):
        return ctx.getText()

    # Visit a parse tree produced by LatteParser#Add.
    def visitAdd(self, ctx: LatteParser.AddContext):
        return ctx.getText()

    # Visit a parse tree produced by LatteParser#Sub.
    def visitSub(self, ctx: LatteParser.SubContext):
        return ctx.getText()

    # Visit a parse tree produced by LatteParser#Mul.
    def visitMul(self, ctx: LatteParser.MulContext):
        return ctx.getText()

    # Visit a parse tree produced by LatteParser#Div.
    def visitDiv(self, ctx: LatteParser.DivContext):
        return ctx.getText()

    # Visit a parse tree produced by LatteParser#Mod.
    def visitMod(self, ctx: LatteParser.ModContext):
        return ctx.getText()

    # Visit a parse tree produced by LatteParser#Lt.
    def visitLt(self, ctx: LatteParser.LtContext):
        return ctx.getText()

    # Visit a parse tree produced by LatteParser#Le.
    def visitLe(self, ctx: LatteParser.LeContext):
        return ctx.getText()

    # Visit a parse tree produced by LatteParser#Gt.
    def visitGt(self, ctx: LatteParser.GtContext):
        return ctx.getText()

    # Visit a parse tree produced by LatteParser#Ge.
    def visitGe(self, ctx: LatteParser.GeContext):
        return ctx.getText()

    # Visit a parse tree produced by LatteParser#Eq.
    def visitEq(self, ctx: LatteParser.EqContext):
        return ctx.getText()

    # Visit a parse tree produced by LatteParser#Neq.
    def visitNeq(self, ctx: LatteParser.NeqContext):
        return ctx.getText()


del LatteParser
