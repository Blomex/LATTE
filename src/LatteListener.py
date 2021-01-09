# Generated from Latte.g4 by ANTLR 4.8
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .LatteParser import LatteParser
else:
    from src.LatteParser import LatteParser

# This class defines a complete listener for a parse tree produced by LatteParser.
class LatteListener(ParseTreeListener):

    # Enter a parse tree produced by LatteParser#program.
    def enterProgram(self, ctx:LatteParser.ProgramContext):
        pass

    # Exit a parse tree produced by LatteParser#program.
    def exitProgram(self, ctx:LatteParser.ProgramContext):
        pass


    # Enter a parse tree produced by LatteParser#FunTopDef.
    def enterFunTopDef(self, ctx:LatteParser.FunTopDefContext):
        pass

    # Exit a parse tree produced by LatteParser#FunTopDef.
    def exitFunTopDef(self, ctx:LatteParser.FunTopDefContext):
        pass


    # Enter a parse tree produced by LatteParser#ClassDef.
    def enterClassDef(self, ctx:LatteParser.ClassDefContext):
        pass

    # Exit a parse tree produced by LatteParser#ClassDef.
    def exitClassDef(self, ctx:LatteParser.ClassDefContext):
        pass


    # Enter a parse tree produced by LatteParser#ClassExtDef.
    def enterClassExtDef(self, ctx:LatteParser.ClassExtDefContext):
        pass

    # Exit a parse tree produced by LatteParser#ClassExtDef.
    def exitClassExtDef(self, ctx:LatteParser.ClassExtDefContext):
        pass


    # Enter a parse tree produced by LatteParser#classattr.
    def enterClassattr(self, ctx:LatteParser.ClassattrContext):
        pass

    # Exit a parse tree produced by LatteParser#classattr.
    def exitClassattr(self, ctx:LatteParser.ClassattrContext):
        pass


    # Enter a parse tree produced by LatteParser#classfun.
    def enterClassfun(self, ctx:LatteParser.ClassfunContext):
        pass

    # Exit a parse tree produced by LatteParser#classfun.
    def exitClassfun(self, ctx:LatteParser.ClassfunContext):
        pass


    # Enter a parse tree produced by LatteParser#FunDef.
    def enterFunDef(self, ctx:LatteParser.FunDefContext):
        pass

    # Exit a parse tree produced by LatteParser#FunDef.
    def exitFunDef(self, ctx:LatteParser.FunDefContext):
        pass


    # Enter a parse tree produced by LatteParser#arg.
    def enterArg(self, ctx:LatteParser.ArgContext):
        pass

    # Exit a parse tree produced by LatteParser#arg.
    def exitArg(self, ctx:LatteParser.ArgContext):
        pass


    # Enter a parse tree produced by LatteParser#block.
    def enterBlock(self, ctx:LatteParser.BlockContext):
        pass

    # Exit a parse tree produced by LatteParser#block.
    def exitBlock(self, ctx:LatteParser.BlockContext):
        pass


    # Enter a parse tree produced by LatteParser#Empty.
    def enterEmpty(self, ctx:LatteParser.EmptyContext):
        pass

    # Exit a parse tree produced by LatteParser#Empty.
    def exitEmpty(self, ctx:LatteParser.EmptyContext):
        pass


    # Enter a parse tree produced by LatteParser#BlockStmt.
    def enterBlockStmt(self, ctx:LatteParser.BlockStmtContext):
        pass

    # Exit a parse tree produced by LatteParser#BlockStmt.
    def exitBlockStmt(self, ctx:LatteParser.BlockStmtContext):
        pass


    # Enter a parse tree produced by LatteParser#Decl.
    def enterDecl(self, ctx:LatteParser.DeclContext):
        pass

    # Exit a parse tree produced by LatteParser#Decl.
    def exitDecl(self, ctx:LatteParser.DeclContext):
        pass


    # Enter a parse tree produced by LatteParser#Ass.
    def enterAss(self, ctx:LatteParser.AssContext):
        pass

    # Exit a parse tree produced by LatteParser#Ass.
    def exitAss(self, ctx:LatteParser.AssContext):
        pass


    # Enter a parse tree produced by LatteParser#Incr.
    def enterIncr(self, ctx:LatteParser.IncrContext):
        pass

    # Exit a parse tree produced by LatteParser#Incr.
    def exitIncr(self, ctx:LatteParser.IncrContext):
        pass


    # Enter a parse tree produced by LatteParser#Decr.
    def enterDecr(self, ctx:LatteParser.DecrContext):
        pass

    # Exit a parse tree produced by LatteParser#Decr.
    def exitDecr(self, ctx:LatteParser.DecrContext):
        pass


    # Enter a parse tree produced by LatteParser#Ret.
    def enterRet(self, ctx:LatteParser.RetContext):
        pass

    # Exit a parse tree produced by LatteParser#Ret.
    def exitRet(self, ctx:LatteParser.RetContext):
        pass


    # Enter a parse tree produced by LatteParser#VRet.
    def enterVRet(self, ctx:LatteParser.VRetContext):
        pass

    # Exit a parse tree produced by LatteParser#VRet.
    def exitVRet(self, ctx:LatteParser.VRetContext):
        pass


    # Enter a parse tree produced by LatteParser#Cond.
    def enterCond(self, ctx:LatteParser.CondContext):
        pass

    # Exit a parse tree produced by LatteParser#Cond.
    def exitCond(self, ctx:LatteParser.CondContext):
        pass


    # Enter a parse tree produced by LatteParser#CondElse.
    def enterCondElse(self, ctx:LatteParser.CondElseContext):
        pass

    # Exit a parse tree produced by LatteParser#CondElse.
    def exitCondElse(self, ctx:LatteParser.CondElseContext):
        pass


    # Enter a parse tree produced by LatteParser#While.
    def enterWhile(self, ctx:LatteParser.WhileContext):
        pass

    # Exit a parse tree produced by LatteParser#While.
    def exitWhile(self, ctx:LatteParser.WhileContext):
        pass


    # Enter a parse tree produced by LatteParser#SExp.
    def enterSExp(self, ctx:LatteParser.SExpContext):
        pass

    # Exit a parse tree produced by LatteParser#SExp.
    def exitSExp(self, ctx:LatteParser.SExpContext):
        pass


    # Enter a parse tree produced by LatteParser#Int.
    def enterInt(self, ctx:LatteParser.IntContext):
        pass

    # Exit a parse tree produced by LatteParser#Int.
    def exitInt(self, ctx:LatteParser.IntContext):
        pass


    # Enter a parse tree produced by LatteParser#Str.
    def enterStr(self, ctx:LatteParser.StrContext):
        pass

    # Exit a parse tree produced by LatteParser#Str.
    def exitStr(self, ctx:LatteParser.StrContext):
        pass


    # Enter a parse tree produced by LatteParser#Bool.
    def enterBool(self, ctx:LatteParser.BoolContext):
        pass

    # Exit a parse tree produced by LatteParser#Bool.
    def exitBool(self, ctx:LatteParser.BoolContext):
        pass


    # Enter a parse tree produced by LatteParser#Void.
    def enterVoid(self, ctx:LatteParser.VoidContext):
        pass

    # Exit a parse tree produced by LatteParser#Void.
    def exitVoid(self, ctx:LatteParser.VoidContext):
        pass


    # Enter a parse tree produced by LatteParser#Class.
    def enterClass(self, ctx:LatteParser.ClassContext):
        pass

    # Exit a parse tree produced by LatteParser#Class.
    def exitClass(self, ctx:LatteParser.ClassContext):
        pass


    # Enter a parse tree produced by LatteParser#item.
    def enterItem(self, ctx:LatteParser.ItemContext):
        pass

    # Exit a parse tree produced by LatteParser#item.
    def exitItem(self, ctx:LatteParser.ItemContext):
        pass


    # Enter a parse tree produced by LatteParser#EId.
    def enterEId(self, ctx:LatteParser.EIdContext):
        pass

    # Exit a parse tree produced by LatteParser#EId.
    def exitEId(self, ctx:LatteParser.EIdContext):
        pass


    # Enter a parse tree produced by LatteParser#EFunCall.
    def enterEFunCall(self, ctx:LatteParser.EFunCallContext):
        pass

    # Exit a parse tree produced by LatteParser#EFunCall.
    def exitEFunCall(self, ctx:LatteParser.EFunCallContext):
        pass


    # Enter a parse tree produced by LatteParser#ERelOp.
    def enterERelOp(self, ctx:LatteParser.ERelOpContext):
        pass

    # Exit a parse tree produced by LatteParser#ERelOp.
    def exitERelOp(self, ctx:LatteParser.ERelOpContext):
        pass


    # Enter a parse tree produced by LatteParser#ETrue.
    def enterETrue(self, ctx:LatteParser.ETrueContext):
        pass

    # Exit a parse tree produced by LatteParser#ETrue.
    def exitETrue(self, ctx:LatteParser.ETrueContext):
        pass


    # Enter a parse tree produced by LatteParser#ENullCast.
    def enterENullCast(self, ctx:LatteParser.ENullCastContext):
        pass

    # Exit a parse tree produced by LatteParser#ENullCast.
    def exitENullCast(self, ctx:LatteParser.ENullCastContext):
        pass


    # Enter a parse tree produced by LatteParser#EOr.
    def enterEOr(self, ctx:LatteParser.EOrContext):
        pass

    # Exit a parse tree produced by LatteParser#EOr.
    def exitEOr(self, ctx:LatteParser.EOrContext):
        pass


    # Enter a parse tree produced by LatteParser#EInt.
    def enterEInt(self, ctx:LatteParser.EIntContext):
        pass

    # Exit a parse tree produced by LatteParser#EInt.
    def exitEInt(self, ctx:LatteParser.EIntContext):
        pass


    # Enter a parse tree produced by LatteParser#EUnOp.
    def enterEUnOp(self, ctx:LatteParser.EUnOpContext):
        pass

    # Exit a parse tree produced by LatteParser#EUnOp.
    def exitEUnOp(self, ctx:LatteParser.EUnOpContext):
        pass


    # Enter a parse tree produced by LatteParser#ENewClass.
    def enterENewClass(self, ctx:LatteParser.ENewClassContext):
        pass

    # Exit a parse tree produced by LatteParser#ENewClass.
    def exitENewClass(self, ctx:LatteParser.ENewClassContext):
        pass


    # Enter a parse tree produced by LatteParser#EStr.
    def enterEStr(self, ctx:LatteParser.EStrContext):
        pass

    # Exit a parse tree produced by LatteParser#EStr.
    def exitEStr(self, ctx:LatteParser.EStrContext):
        pass


    # Enter a parse tree produced by LatteParser#EMulOp.
    def enterEMulOp(self, ctx:LatteParser.EMulOpContext):
        pass

    # Exit a parse tree produced by LatteParser#EMulOp.
    def exitEMulOp(self, ctx:LatteParser.EMulOpContext):
        pass


    # Enter a parse tree produced by LatteParser#EAnd.
    def enterEAnd(self, ctx:LatteParser.EAndContext):
        pass

    # Exit a parse tree produced by LatteParser#EAnd.
    def exitEAnd(self, ctx:LatteParser.EAndContext):
        pass


    # Enter a parse tree produced by LatteParser#EFieldAcces.
    def enterEFieldAcces(self, ctx:LatteParser.EFieldAccesContext):
        pass

    # Exit a parse tree produced by LatteParser#EFieldAcces.
    def exitEFieldAcces(self, ctx:LatteParser.EFieldAccesContext):
        pass


    # Enter a parse tree produced by LatteParser#EParen.
    def enterEParen(self, ctx:LatteParser.EParenContext):
        pass

    # Exit a parse tree produced by LatteParser#EParen.
    def exitEParen(self, ctx:LatteParser.EParenContext):
        pass


    # Enter a parse tree produced by LatteParser#EFalse.
    def enterEFalse(self, ctx:LatteParser.EFalseContext):
        pass

    # Exit a parse tree produced by LatteParser#EFalse.
    def exitEFalse(self, ctx:LatteParser.EFalseContext):
        pass


    # Enter a parse tree produced by LatteParser#EAddOp.
    def enterEAddOp(self, ctx:LatteParser.EAddOpContext):
        pass

    # Exit a parse tree produced by LatteParser#EAddOp.
    def exitEAddOp(self, ctx:LatteParser.EAddOpContext):
        pass


    # Enter a parse tree produced by LatteParser#Not.
    def enterNot(self, ctx:LatteParser.NotContext):
        pass

    # Exit a parse tree produced by LatteParser#Not.
    def exitNot(self, ctx:LatteParser.NotContext):
        pass


    # Enter a parse tree produced by LatteParser#Neg.
    def enterNeg(self, ctx:LatteParser.NegContext):
        pass

    # Exit a parse tree produced by LatteParser#Neg.
    def exitNeg(self, ctx:LatteParser.NegContext):
        pass


    # Enter a parse tree produced by LatteParser#Add.
    def enterAdd(self, ctx:LatteParser.AddContext):
        pass

    # Exit a parse tree produced by LatteParser#Add.
    def exitAdd(self, ctx:LatteParser.AddContext):
        pass


    # Enter a parse tree produced by LatteParser#Sub.
    def enterSub(self, ctx:LatteParser.SubContext):
        pass

    # Exit a parse tree produced by LatteParser#Sub.
    def exitSub(self, ctx:LatteParser.SubContext):
        pass


    # Enter a parse tree produced by LatteParser#Mul.
    def enterMul(self, ctx:LatteParser.MulContext):
        pass

    # Exit a parse tree produced by LatteParser#Mul.
    def exitMul(self, ctx:LatteParser.MulContext):
        pass


    # Enter a parse tree produced by LatteParser#Div.
    def enterDiv(self, ctx:LatteParser.DivContext):
        pass

    # Exit a parse tree produced by LatteParser#Div.
    def exitDiv(self, ctx:LatteParser.DivContext):
        pass


    # Enter a parse tree produced by LatteParser#Mod.
    def enterMod(self, ctx:LatteParser.ModContext):
        pass

    # Exit a parse tree produced by LatteParser#Mod.
    def exitMod(self, ctx:LatteParser.ModContext):
        pass


    # Enter a parse tree produced by LatteParser#Lt.
    def enterLt(self, ctx:LatteParser.LtContext):
        pass

    # Exit a parse tree produced by LatteParser#Lt.
    def exitLt(self, ctx:LatteParser.LtContext):
        pass


    # Enter a parse tree produced by LatteParser#Le.
    def enterLe(self, ctx:LatteParser.LeContext):
        pass

    # Exit a parse tree produced by LatteParser#Le.
    def exitLe(self, ctx:LatteParser.LeContext):
        pass


    # Enter a parse tree produced by LatteParser#Gt.
    def enterGt(self, ctx:LatteParser.GtContext):
        pass

    # Exit a parse tree produced by LatteParser#Gt.
    def exitGt(self, ctx:LatteParser.GtContext):
        pass


    # Enter a parse tree produced by LatteParser#Ge.
    def enterGe(self, ctx:LatteParser.GeContext):
        pass

    # Exit a parse tree produced by LatteParser#Ge.
    def exitGe(self, ctx:LatteParser.GeContext):
        pass


    # Enter a parse tree produced by LatteParser#Eq.
    def enterEq(self, ctx:LatteParser.EqContext):
        pass

    # Exit a parse tree produced by LatteParser#Eq.
    def exitEq(self, ctx:LatteParser.EqContext):
        pass


    # Enter a parse tree produced by LatteParser#Neq.
    def enterNeq(self, ctx:LatteParser.NeqContext):
        pass

    # Exit a parse tree produced by LatteParser#Neq.
    def exitNeq(self, ctx:LatteParser.NeqContext):
        pass



del LatteParser