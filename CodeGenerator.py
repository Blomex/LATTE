# Generated from Latte.g4 by ANTLR 4.8
from itertools import repeat

from antlr4 import *

if __name__ is not None and "." in __name__:
    from .LatteParser import LatteParser
else:
    from LatteParser import LatteParser
import sys
from copy import deepcopy


# This class defines a complete generic visitor for a parse tree produced by LatteParser.

class CodeGenerator(ParseTreeVisitor):
    def __init__(self, file=sys.stdout):
        # next label id
        self._current_register = 0
        self.class_types = {}
        self.class_attributes = {}
        self.f = open(file, "w+")
        self.generated_code = []
        self.pre_code = []
        self.class_vars = {}
        self.nextLabel = 0
        self.class_methods = {}
        self.current_class = None
        self.strings = {}
        self.inheritance = {}
        self.strings[""] = "@emptystr"
        self.pre_code.append("@emptystr = private unnamed_addr constant [1 x i8] c\"\\00\"")

    # Visit a parse tree produced by LatteParser#program.
    def visitProgram(self, ctx: LatteParser.ProgramContext):
        # TODO create class types
        self.pre_code.append("declare i8* @malloc(i64)")
        self.pre_code.append("declare void @error")
        self.pre_code.append("declare void @printString(i8*)")
        self.pre_code.append("declare void @printInt(i32)")
        self.pre_code.append("declare i32 @readInt()")
        self.pre_code.append("declare i8* @readString()")
        self.pre_code.append("declare i8* @concat(i8*, i8*)")

        self.class_methods = ctx.class_methods
        class_list = [i for i in ctx.getChildren(predicate=lambda c: isinstance(c, LatteParser.ClassDefContext))]
        extend_class_list = [c for c in
                             ctx.getChildren(predicate=lambda c: isinstance(c, LatteParser.ClassExtDefContext))]
        for i in class_list + extend_class_list:
            self.visit(i)
        print(self.class_types)
        for k in self.class_types.keys():
            self.pre_code.append("%{} = type {{ {} }}".format(k, ", ".join(self.class_types[k])))
        functions = [i for i in ctx.getChildren(predicate=lambda c: isinstance(c, LatteParser.FunTopDefContext))]
        for f in functions:
            self._generate_function(f.fundef())
        for x in self.pre_code:
            print(x, file=self.f)
        # self._mark_unreachable_code()
        for x in self.generated_code:
            print(x, file=self.f)

        # return self.visitChildren(ctx)

    # Visit a parse tree produced by LatteParser#FunTopDef.
    def visitFunTopDef(self, ctx: LatteParser.FunTopDefContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LatteParser#ClassDef.
    def visitClassDef(self, ctx: LatteParser.ClassDefContext):
        clsname = ctx.ID().getText()
        self.inheritance[clsname] = "#latte.lang.object"
        attributes = [i for i in ctx.getChildren(predicate=lambda c: isinstance(c, LatteParser.ClassattrContext))]
        attributes = [(self._getType(i), [x.getText() for x in i.ID()]) for i in attributes]
        attributes_names = [x.ID()[0].getText() for x in
                            ctx.getChildren(predicate=lambda c: isinstance(c, LatteParser.ClassattrContext))]
        print("attribute names: {}".format(attributes_names))
        self.class_types[clsname] = []
        for i in attributes:
            self.class_types[clsname].extend(repeat(i[0], len(i[1])))
        print("Class {}, attributes: {}".format(clsname, self.class_types[clsname]))
        if clsname not in self.class_attributes:
            self.class_attributes[clsname] = {}
        for i, attr in enumerate(attributes_names):
            self.class_attributes[clsname][attr] = i
        print(self.class_attributes)
        self._generate_code_for_methods(ctx)
        return

    # Visit a parse tree produced by LatteParser#ClassExtDef.
    def visitClassExtDef(self, ctx: LatteParser.ClassExtDefContext):
        clsname = ctx.ID()[0].getText()
        baseclsname = ctx.ID()[1].getText()
        self.inheritance[clsname] = baseclsname
        attributes = [i for i in ctx.getChildren(predicate=lambda c: isinstance(c, LatteParser.ClassattrContext))]
        attributes = [(self._getType(i), [x.getText() for x in i.ID()]) for i in attributes]
        attributes_names = [x.ID()[0].getText() for x in
                            ctx.getChildren(predicate=lambda c: isinstance(c, LatteParser.ClassattrContext))]
        #attributes.insert(0, ("%{}*".format(baseclsname), ["super"]))
        self.class_types[clsname] = self.class_types[baseclsname].copy()
        for i in attributes:
            self.class_types[clsname].extend(repeat(i[0], len(i[1])))
        print("Extended class {}, attributes: {}".format(clsname, self.class_types[clsname]))
        if clsname not in self.class_attributes:
            self.class_attributes[clsname] = self.class_attributes[baseclsname].copy()
        for i, attr in enumerate(attributes_names, start=len(self.class_attributes[clsname])):
            self.class_attributes[clsname][attr] = i
        print("DEBUG {}".format(self.class_attributes))
        self._generate_code_for_methods(ctx)
    # Visit a parse tree produced by LatteParser#classattr.
    def visitClassattr(self, ctx: LatteParser.ClassattrContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LatteParser#classfun.
    def visitClassfun(self, ctx: LatteParser.ClassfunContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LatteParser#FunDef.
    def visitFunDef(self, ctx: LatteParser.FunDefContext):
        print("inside fundef")
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LatteParser#arg.
    def visitArg(self, ctx: LatteParser.ArgContext):
        print("inside function arg")
        dict = {}
        for i, x in enumerate(ctx.type_()):
            dict[ctx.ID()[i].getText()] = self._getType(x.getText(), True)
        print(dict)
        return dict

    # Visit a parse tree produced by LatteParser#block.
    def visitBlock(self, ctx: LatteParser.BlockContext):
        print("inside block")
        previous_vars = deepcopy(self.vars)
        self.visitChildren(ctx)
        self.vars = previous_vars

    # Visit a parse tree produced by LatteParser#Empty.
    def visitEmpty(self, ctx: LatteParser.EmptyContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LatteParser#BlockStmt.
    def visitBlockStmt(self, ctx: LatteParser.BlockStmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LatteParser#Decl.
    def visitDecl(self, ctx: LatteParser.DeclContext):
        self.declType = self._getType(ctx)
        print("inside decl")
        self.visitChildren(ctx)
        del self.declType

    # Visit a parse tree produced by LatteParser#Ass.
    def visitAss(self, ctx: LatteParser.AssContext):
        self._visitAss(ctx, '=')

    # Visit a parse tree produced by LatteParser#Incr.
    def visitIncr(self, ctx: LatteParser.IncrContext):
        self._visitAss(ctx, '++')

    # Visit a parse tree produced by LatteParser#Decr.
    def visitDecr(self, ctx: LatteParser.DecrContext):
        self._visitAss(ctx, '--')

    # Visit a parse tree produced by LatteParser#Ret.
    def visitRet(self, ctx: LatteParser.RetContext):
        result = self.visit(ctx.expr())
        type = self._getType(ctx.expr().expr_type, is_type=True)
        self.generated_code.append("ret {} {}".format(type, result))

    # Visit a parse tree produced by LatteParser#VRet.
    def visitVRet(self, ctx: LatteParser.VRetContext):
        self.generated_code.append("ret void")

    # Visit a parse tree produced by LatteParser#Cond.
    def visitCond(self, ctx: LatteParser.CondContext):
        expr_result = self.get_value(ctx.expr())
        if self._is_register(expr_result):
            label_true = self._get_next_label()
            label_rest = self._get_next_label()
            self.generated_code.append("br i1 {}, label %{}, label %{}"
                                       .format(expr_result, label_true, label_rest))
            self.generated_code.append("{}:".format(label_true))
            self.visit(ctx.stmt())
            self.generated_code.append("br label %{}".format(label_rest))
            self.generated_code.append("{}:".format(label_rest))
            return
        else:
            if expr_result == '1':
                self.visit(ctx.stmt())
                return
            else:
                return

    # Visit a parse tree produced by LatteParser#CondElse.
    def visitCondElse(self, ctx: LatteParser.CondElseContext):
        expr_result = self.get_value(ctx.expr())
        if self._is_register(expr_result):
            true_label = self._get_next_label()
            false_label = self._get_next_label()
            rest_label = self._get_next_label()
            self.generated_code.append("br i1 {}, label %{true}, label %{false}"
                                       .format(expr_result, true=true_label, false=false_label))
            # true label
            self.generated_code.append("{}:".format(true_label))
            self.visit(ctx.stmt()[0])
            # skip else part if we visited true
            self.generated_code.append("br label %{}".format(rest_label))
            # FALSE
            self.generated_code.append("{}:".format(false_label))
            self.visit(ctx.stmt()[1])
            self.generated_code.append("br label %{}".format(rest_label))
            # REST
            self.generated_code.append("{}:".format(rest_label))
        elif expr_result == '1':
            self.visit(ctx.stmt()[0])
        elif expr_result == '0':
            self.visit(ctx.stmt()[1])
        return

    # Visit a parse tree produced by LatteParser#While.
    def visitWhile(self, ctx: LatteParser.WhileContext):

        check_cond = self._get_next_label()
        loop_body = self._get_next_label()
        after_loop = self._get_next_label()
        self.generated_code.append("br label %{}".format(check_cond))
        self.generated_code.append("{}:".format(loop_body))
        self.visit(ctx.stmt())
        self.generated_code.append("br label %{}".format(check_cond))
        self.generated_code.append("{}:".format(check_cond))
        result = self.get_value(ctx.expr())
        self.generated_code.append("br i1 {}, label %{}, label %{}".format(result, loop_body, after_loop))
        self.generated_code.append("{}:".format(after_loop))

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
        print("inside decl item")
        print(self.class_types)
        new_reg = self._get_register()
        self.generated_code.append("{} = alloca {type}".format(new_reg, type=self.declType))
        ident = ctx.ID().getText()
        if ident not in self.vars:
            self.vars[ident] = (self.declType, new_reg)
        print(self.vars)
        # only declaration
        if not ctx.expr():
            self.vars[ident] = (self.declType, new_reg)
            if self.declType in ['i32', 'i1']:
                self.generated_code.append("store {type} 0, {type}* {reg}".format(type=self.declType, reg=new_reg))
            # TODO string i klasy
            elif self.declType == 'i8*':
                strlen = 1
                self.generated_code.append(
                    "store i8* getelementptr inbounds ([{len} x i8], [{len} x i8]* {str_label}, i32 0, i32 0), i8** {reg}"
                        .format(len=strlen, str_label=self.strings[""], reg=new_reg))
                return new_reg
            else:  # Klasy
                self.generated_code.append("store {type} null, {type}* {reg}".format(type=self.declType, reg=new_reg))
                return new_reg

        else:
            # First generate code for current variables
            result = self.visit(ctx.expr())
            # then replace variable
            print(self.vars)
            self.vars[ident] = (self.declType, new_reg)
            if self.declType in ['i32', 'i1']:
                self.generated_code.append("store {type} {res}, {type}* {reg}"
                                           .format(type=self.declType, res=result, reg=new_reg))
            elif self.declType == 'i8*':
                # constant string
                print(result)
                if result[0] == '@':
                    strlen = len(eval(ctx.expr().getText())) + 1
                    self.generated_code.append(
                        "store i8* getelementptr inbounds ([{len} x i8], [{len} x i8]* {str_label}, i32 0, i32 0), i8** {reg}"
                        .format(len=strlen, str_label=result, reg=new_reg))
                    return new_reg
                    # self.generated_code
                else:  # String as result of function
                    self.generated_code.append("store i8* {}, i8** {}".format(result, new_reg))
                    return new_reg
            else:  # Klasy
                self.generated_code.append("store {type} {result}, {type}* {reg}".format(type=self.declType,result=result, reg=new_reg))
                return result

            # elif: # TODO STRING I KLASY

    # Visit a parse tree produced by LatteParser#EId.
    def visitEId(self, ctx: LatteParser.EIdContext):
        print("inside Eid")
        print(self.current_class)
        new_reg = self._get_register()
        ident = ctx.ID().getText()
        if ident in self.vars:
            type, reg = self.vars[ident]
            self.generated_code.append(
                "{new_reg} = load {type}, {type}* {reg}".format(new_reg=new_reg, type=type, reg=reg))
            #TODO remove dead code
        # else:  # class attribute
        #     class_name = "Point2"
        #     attribute_idx = self.class_attributes[class_name][ident]
        #     attribute_type = self.class_types[class_name][attribute_idx]
        #     clstype, clsreg = self.vars["%this"]
        #     loadreg = self._get_register()
        #     self.generated_code.append("{} = load {type}, {type}* {clsptr}"
        #                                .format(loadreg, type=clstype, clsptr=clsreg))
        #     print("loading class: {}".format(self.generated_code[-1]))
        #     elem_ptr = self._get_register()
        #     self.generated_code.append("{} = getelementptr inbounds {type}, {type}* {reg}, i32 0, i32 {idx}"
        #                                .format(elem_ptr, type=clstype[:-1], reg=loadreg, idx=attribute_idx))
        #     self.generated_code.append("{} = load {type}, {type}* {elem_ptr}"
        #                                .format(new_reg, type=attribute_type, elem_ptr=elem_ptr))
        return new_reg

    # Visit a parse tree produced by LatteParser#EFunCall.
    def visitEFunCall(self, ctx: LatteParser.EFunCallContext):
        print("function call")
        print(self.class_methods)
        name = ctx.ID().getText()
        print(name, self.current_class)
        if self.current_class is None:
            self.current_class = "#latte.lang.object"
        main_class = self.current_class
        while name not in self.class_methods[self.current_class] and self.current_class != "#latte.lang.object":
            self.current_class = self.inheritance[self.current_class]
        if name in self.class_methods[self.current_class]:
            ret_type, par_types = self.class_methods[self.current_class][name]
        class_argument = ""
        if main_class != "#latte.lang.object":
            if main_class != self.current_class:
                prev = ctx.clsptr
                ctx.clsptr = self._get_register()
                self.generated_code.append("{} = bitcast %{}* {} to %{}*"
                                           .format(ctx.clsptr, main_class,  prev, self.current_class))
            class_argument = "%" + self.current_class + "* " + ctx.clsptr
            name = "_" + self.current_class + "_" + name
        print(self.current_class, name)
        previous = self.current_class
        self.current_class = "#latte.lang.object"
        args = [self.visit(a) for a in ctx.expr()]
        self.current_class = previous
        type = self._getType(ret_type, True)
        par_types = [self._getType(x, True) for x in par_types]
        print("name: {}, type: {}, args_types: {} {}".format(name, type, par_types, args))
        if class_argument != "" and len(par_types) > 0:
            class_argument += ", "
            print("par_types: {}".format(par_types))
        for i, ptype in enumerate(par_types):
            if isinstance(ctx.expr()[i], LatteParser.EFieldAccesContext) and ptype in ['i1', 'i32', 'i8*'] \
                    and not isinstance(ctx.expr()[i].expr()[1], LatteParser.EFunCallContext):
                get_elem = self._get_register()
                self.generated_code.append("{} = load {}, {}* {}".format(get_elem, ptype, ptype, args[i]))
                args[i] = get_elem
        print(args)
        self.current_class = None
        if type != 'void':
            new_reg = self._get_register()
            self.generated_code.append("{} = call {type} @{name} ({clsarg}{params})"
                                       .format(new_reg, type=type, name=name, clsarg=class_argument,
                                               params=", ".join([par_types[i] + " " + x for i, x in enumerate(args)])))
            self.current_class = None
            print("after fun call {}".format(new_reg))
            return new_reg
        self.generated_code.append("call {type} @{name} ({clsarg}{params})"
                                   .format(type=type, name=name, clsarg=class_argument,
                                           params=", ".join([par_types[i] + " " + x for i, x in enumerate(args)])))
        self.current_class = None

    # Visit a parse tree produced by LatteParser#ERelOp.
    def visitERelOp(self, ctx: LatteParser.ERelOpContext):
        print("inside rel op")
        op = self.visit(ctx.relOp())
        r1 = self.get_value(ctx.expr()[0])
        r2 = self.get_value(ctx.expr()[1])
        new_register = self._get_register()
        # TODO can be optimized
        type = self._getType(ctx.expr()[0].expr_type, True)
        if type in ['i1', 'i32']:
            self.generated_code.append(
                "{new} = icmp {op} {t} {r1}, {r2}".format(new=new_register, op=op, t=type, r1=r1, r2=r2))
        elif type == 'i8*':
            # String
            if r1 is None:
                ptr_reg = self._get_register()
                self.generated_code.append("{} = alloca i8*".format(ptr_reg))

            tmp_reg = self._get_register()
            self.generated_code.append("{tmp} = call i32 @strcmp(i8* {r1}, i8* {r2})"
                                       .format(tmp=tmp_reg, r1=r1, r2=r2))
            self.generated_code.append("{} = icmp eq i32 {}, 0".format(new_register, tmp_reg))
        else: # klasy
            self.generated_code.append("{new} = icmp {op} {t} {r1}, {r2}"
                                       .format(new=new_register, op=op, t=type, r1=r1, r2=r2))
        return new_register

    # Visit a parse tree produced by LatteParser#ETrue.
    def visitETrue(self, ctx: LatteParser.ETrueContext):
        return '1'

    # Visit a parse tree produced by LatteParser#ENullCast.
    def visitENullCast(self, ctx: LatteParser.ENullCastContext):
        return "null"

    # Visit a parse tree produced by LatteParser#EOr.
    def visitEOr(self, ctx: LatteParser.EOrContext):
        label_true = self._get_next_label()
        label_rest = self._get_next_label()
        label_false = self._get_next_label()
        left_false = self._get_next_label()
        result = self.get_value(ctx.expr()[0])
        alloc_reg = self._get_register()
        new_reg = self._get_register()
        if self._is_register(result):
            self.generated_code.append("{} = alloca i1".format(alloc_reg))
            self.generated_code.append(
                "br i1 {}, label %{true}, label %{false}".format(result, true=label_true, false=left_false))
            # LEFT FALSE
            self.generated_code.append("{}:".format(left_false))
            # check if right is true
            right_result = self.get_value(ctx.expr()[1])
            self.generated_code.append(
                "br i1 {}, label %{true}, label %{false}".format(right_result, true=label_true, false=label_false))
            # Whole expression is false
            self.generated_code.append("{}:".format(label_false))
            self.generated_code.append("store i1 0, i1* {}".format(alloc_reg))
            self.generated_code.append("br label %{}".format(label_rest))
            # Whole expression is True
            self.generated_code.append("{}:".format(label_true))
            self.generated_code.append("store i1 1, i1* {}".format(alloc_reg))
            self.generated_code.append("br label %{}".format(label_rest))
            self.generated_code.append("{}:".format(label_rest))
            self.generated_code.append("{} = load i1, i1* {}".format(new_reg, alloc_reg))

        else:  # first result is some kind of constant, not register
            # check second result
            if result == '1':
                return '1'
            right_result = self.get_value(ctx.expr()[1])
            if self._is_register(right_result):
                self.generated_code.append("{} = alloca i1".format(alloc_reg))
                self.generated_code.append(
                    "br i1 {}, label %{true}, label %{false}".format(right_result, true=label_true, false=label_false))
                # Whole expression is false
                self.generated_code.append("{}:".format(label_false))
                self.generated_code.append("store i1 0, i1* {}".format(alloc_reg))
                self.generated_code.append("br label %{}".format(label_rest))
                # Whole expression is True
                self.generated_code.append("{}:".format(label_true))
                self.generated_code.append("store i1 1, i1* {}".format(alloc_reg))
                self.generated_code.append("br label %{}".format(label_rest))
                # rest
                self.generated_code.append("{}:".format(label_rest))
                self.generated_code.append("{} = load i1, i1* {}".format(new_reg, alloc_reg))
            else:
                return right_result
        return new_reg

    # Visit a parse tree produced by LatteParser#EInt.
    def visitEInt(self, ctx: LatteParser.EIntContext):
        return ctx.INT().getText()

    # Visit a parse tree produced by LatteParser#EUnOp.
    def visitEUnOp(self, ctx: LatteParser.EUnOpContext):
        op = self.visit(ctx.unOp())
        register = self.get_value(ctx.expr())
        new_register = self._get_register()
        if op == '-':
            if self._is_register(register):
                self.generated_code.append("{} = sub i32 {}, {}".format(new_register, 0, register))
                return new_register
            else:
                return str(-int(register))
        elif op == '!':
            if self._is_register(register):
                self.generated_code.append("{} = sub i1 {}, {}".format(new_register, 1, register))
                return new_register
            else:
                # TODO check if works
                return '0' if register == '1' else '1'

    # Visit a parse tree produced by LatteParser#ENewClass.
    def visitENewClass(self, ctx: LatteParser.ENewClassContext):
        offset_reg_ptr = self._get_register()
        offset_size_reg = self._get_register()
        malloc_reg = self._get_register()
        new_reg = self._get_register()
        self.generated_code.append("{} = getelementptr {}, {} null, i64 1"
                                   .format(offset_reg_ptr, self.declType[:-1], self.declType))
        self.generated_code.append("{} = ptrtoint {} {} to i64"
                                   .format(offset_size_reg, self.declType, offset_reg_ptr))
        self.generated_code.append("{} = call i8* @malloc(i64 {})"
                                   .format(malloc_reg, offset_size_reg))
        self.generated_code.append("{} = bitcast i8* {} to {}"
                                   .format(new_reg, malloc_reg, self.declType))

        for i, attr_type in enumerate(self.class_types[self.declType[1:-1]]):
            print("current_attr = {}".format(attr_type))
            current_attribute = self._get_register()
            self.generated_code.append("{} = getelementptr inbounds {t}, {t}* {reg}, i32 0, i32 {idx}"
                                       .format(current_attribute, t=self.declType[:-1], reg=new_reg, idx=i))
            if attr_type in ['i1', 'i32']:
                self.generated_code.append("store {type} 0, {type}* {register}"
                                           .format(type=attr_type, register=current_attribute))
            elif attr_type == 'i8*':
                strlen = 1
                self.generated_code.append(
                    "store i8* getelementptr inbounds ([{len} x i8], [{len} x i8]* {str_label}, i32 0, i32 0), i8** {reg}"
                        .format(len=strlen, str_label=self.strings[""], reg=current_attribute))
            else:
                self.generated_code.append("store {type} null, {type}* {register}"
                                           .format(type=attr_type, register=current_attribute))
        # self.generated_code.append("store {type} {cast_reg}, {type}* {new_reg}"
        #                            .format(type=self.declType, cast_reg=cast_reg, new_reg=new_reg))
        return new_reg

    # Visit a parse tree produced by LatteParser#EStr.
    def visitEStr(self, ctx: LatteParser.EStrContext):
        print("inside EStr")
        string_name = ctx.getText()
        if string_name in self.strings:
            return self._get_constant_string(string_name)
        else:
            str_len = len(eval(string_name)) + 1
            str_label = "@str{}".format(self._get_next_label())
            self.pre_code.append("{str_label} = private unnamed_addr constant [{str_len} x i8] c\"{str}\\00\""
                                 .format(str_label=str_label, str=eval(string_name), str_len=str_len))
            self.strings[string_name] = str_label
            return self._get_constant_string(string_name)

    # Visit a parse tree produced by LatteParser#EMulOp.
    def visitEMulOp(self, ctx: LatteParser.EMulOpContext):
        left = self.get_value(ctx.expr()[0])
        right = self.get_value(ctx.expr()[1])
        op = ctx.mulOp().getText()
        new_reg = self._get_register()
        if op == '*':
            if self._is_register(left) or self._is_register(right):
                self.generated_code.append("{} = mul nsw i32 {}, {}".format(new_reg, left, right))
                return new_reg
            else:
                return str(int(left) * int(right))
        if op == '/':
            if self._is_register(left) or self._is_register(right):
                self.generated_code.append("{} = sdiv i32 {}, {}".format(new_reg, left, right))
                return new_reg
            elif right == '0':
                self.generated_code.append("call void @error()")
                self.generated_code.append("unreachable")
                return new_reg
            else:
                return str(int(left) // int(right))
        if op == '%':
            if self._is_register(left) or self._is_register(right):
                self.generated_code.append("{} = srem i32 {}, {}".format(new_reg, left, right))
                return new_reg
            else:
                return str(int(left) % int(right))

    # Visit a parse tree produced by LatteParser#EAnd.
    def visitEAnd(self, ctx: LatteParser.EAndContext):
        start_label = self._get_next_label()
        left_true = self._get_next_label()
        label_true = self._get_next_label()
        label_rest = self._get_next_label()
        label_false = self._get_next_label()
        # left part
        result = self.get_value(ctx.expr()[0])
        # if left is false, then we jump to label_false
        alloc_reg = self._get_register()
        new_reg = self._get_register()
        if self._is_register(result):
            self.generated_code.append("{} = alloca i1".format(alloc_reg))
            self.generated_code.append(
                "br i1 {}, label %{true}, label %{false}".format(result, true=left_true, false=label_false))
            self.generated_code.append("{}:".format(left_true))
            right_result = self.get_value(ctx.expr()[1])
            self.generated_code.append(
                "br i1 {}, label %{true}, label %{false}".format(right_result, true=label_true, false=label_false))
            # TRUE
            self.generated_code.append("{}:".format(label_true))
            self.generated_code.append("store i1 1, i1* {}".format(alloc_reg))
            self.generated_code.append("br label %{}".format(label_rest))
            # FALSE
            self.generated_code.append("{}:".format(label_false))
            self.generated_code.append("store i1 0, i1* {}".format(alloc_reg))
            self.generated_code.append("br label %{}".format(label_rest))

        else:
            if result == '1':
                right_result = self.get_value(ctx.expr()[1])
                if self._is_register(right_result):
                    self.generated_code.append("{} = alloca i1".format(alloc_reg))
                    self.generated_code.append(
                        "br i1 {}, label%{}, label %{}".format(right_result, label_true, label_false))
                    # FALSE
                    self.generated_code.append("{}:".format(label_false))
                    self.generated_code.append("store i1 0, i1* {}".format(alloc_reg))
                    self.generated_code.append("br label %{}".format(label_rest))
                    # TRUE
                    self.generated_code.append("{}:".format(label_true))
                    self.generated_code.append("store i1 1, i1* {}".format(alloc_reg))
                    self.generated_code.append("br label %{}".format(label_rest))
                else:
                    return right_result
            if result == '0':
                return '0'
        self.generated_code.append("{}:".format(label_rest))
        self.generated_code.append("{} = load i1, i1* {}".format(new_reg, alloc_reg))
        return new_reg
        # return self.visitChildren(ctx)

    # Visit a parse tree produced by LatteParser#EFieldAcces.
    def visitEFieldAcces(self, ctx: LatteParser.EFieldAccesContext):
        print("visiting field access")
        print(ctx.getText())
        clsptr = self.visit(ctx.expr()[0])
        print(self.vars)
        expr = ctx.expr()[1]  # second expression
        self.current_class, _ = self.vars[ctx.expr()[0].getText()]
        self.current_class = self.current_class[1:-1]
        print(self.current_class)
        # possible access:
        # 1) object.attribute
        # 2) object.method()
        # 3) object.another_object.(1 or 2 or 3)
        print("class on the left pointer: {}".format(clsptr))
        if isinstance(expr, LatteParser.EIdContext):
            ident = expr.ID().getText()
            print("class type: {} ident: {}".format(self.current_class, ident))
            # offset of the element in class
            idx = self.class_attributes[self.current_class][ident]
            # type of the element in class
            attr_type = self.class_types[self.current_class][idx]
            print("idx and attr: {} {}".format(idx, attr_type))
            elem_ptr = self._get_register()
            self.generated_code.append("{} = getelementptr inbounds {t}, {t}* {reg}, i32 0, i32 {idx}"
                                       .format(elem_ptr, t="%" + self.current_class, reg=clsptr, idx=idx))
            self.current_class = None
            return elem_ptr
        elif isinstance(expr, LatteParser.EFunCallContext):
            ident = expr.ID().getText()
            print("method call, type: {} ident: {}".format(self.current_class, ident))
            print(self.vars)
            prev = self.current_class
            fun_name = "_" + self.current_class + "_" + ident
            expr.clsptr = clsptr
            result = self.visit(expr)
            print("after efuncallcontext {}".format(result))
            self.current_class = prev
            self.current_class = None
            return result

    # Visit a parse tree produced by LatteParser#EParen.
    def visitEParen(self, ctx: LatteParser.EParenContext):
        return self.visit(ctx.expr())

    # Visit a parse tree produced by LatteParser#EFalse.
    def visitEFalse(self, ctx: LatteParser.EFalseContext):
        return '0'

    # Visit a parse tree produced by LatteParser#EAddOp.
    def visitEAddOp(self, ctx: LatteParser.EAddOpContext):
        print("inside EAddOp")
        r1 = self.get_value(ctx.expr()[0])
        r2 = self.get_value(ctx.expr()[1])
        operator = self.visit(ctx.addOp())
        print("{} {} ".format(r1, operator))
        new_reg = self._get_register()
        if ctx.expr_type == 'int':
            if operator == '+':
                self.generated_code.append("{} = add i32 {}, {}".format(new_reg, r1, r2))
            elif operator == '-':
                self.generated_code.append("{} = sub i32 {}, {}".format(new_reg, r1, r2))
        if ctx.expr_type == 'string':
            self.generated_code.append("{} = call i8* @concat(i8* {}, i8* {})"
                                       .format(new_reg, r1, r2))
        return new_reg

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
        return 'slt'

    # Visit a parse tree produced by LatteParser#Le.
    def visitLe(self, ctx: LatteParser.LeContext):
        return 'sle'

    # Visit a parse tree produced by LatteParser#Gt.
    def visitGt(self, ctx: LatteParser.GtContext):
        return 'sgt'

    # Visit a parse tree produced by LatteParser#Ge.
    def visitGe(self, ctx: LatteParser.GeContext):
        return 'sge'

    # Visit a parse tree produced by LatteParser#Eq.
    def visitEq(self, ctx: LatteParser.EqContext):
        return 'eq'

    # Visit a parse tree produced by LatteParser#Neq.
    def visitNeq(self, ctx: LatteParser.NeqContext):
        return 'ne'

    def _getType(self, i, is_type=False):
        if is_type:
            type = i
        else:
            type = i.type_().getText()
        # TODO dopisac pozostale typy
        if type == 'int':
            return 'i32'
        if type == 'boolean':
            return 'i1'
        if type == 'string':
            return 'i8*'
        if type == 'void':
            return 'void'
        return "%" + type + "*"  # pointer to class

    def _generate_code_for_methods(self, ctx):
        methods = [i for i in ctx.getChildren(predicate=lambda c: isinstance(c, LatteParser.ClassfunContext))]
        print("methods in class: {}", [x.getText() for x in methods])
        clsname = ctx.ID() if isinstance(ctx, LatteParser.ClassDefContext) else ctx.ID()[0]
        for x in methods:
            self._generate_class_method(x, clsname.getText())

    def _generate_class_method(self, ctx: LatteParser.ClassfunContext, class_name):
        print("generating code for method {} with class name {}".format(ctx.getText(), class_name))
        fun_name = "_{}_{}".format(class_name, ctx.fundef().ID().getText())
        self.generated_code.append("${} = comdat any".format(fun_name))
        fun: LatteParser.fundef = ctx.fundef()
        fun_type = self._getType(fun)
        arg = fun.arg()
        arguments = self.visit(arg) if arg is not None else {}
        print(arguments, fun_type)
        first_line = "define {fun_type} @{fun_name}(%{class_name}* %this".format(fun_type=fun_type,
                                                                                 fun_name=fun_name,
                                                                                 class_name=class_name)
        # self.current_class = class_name
        # self.class_methods[class_name][fun_name] = (fun_type, arguments.values())
        if len(arguments) > 0:
            first_line += ', ' + ', '.join(arguments[x] + " " + "%{}".format(x) for x in arguments.keys())
        first_line += '){'
        self.generated_code.append(first_line)
        self.vars = {}
        # register for class ptr
        new_reg = self._get_register()
        self.generated_code.append("{} = alloca %{type}*".format(new_reg, type=class_name))
        self.generated_code.append("store {type} {value}, {type}* {ptr}"
                                   .format(type="%{}*".format(class_name), value="%this", ptr=new_reg))
        self.vars["self"] = ("%{}*".format(class_name), new_reg)
        # register class attributes
        cls_reg = self._get_register()
        self.generated_code.append("{} = load {type}, {type}* {cls}"
                                   .format(cls_reg, type="%{}*".format(class_name), cls=new_reg))
        for attr in self.class_attributes[class_name]:
            print("cls_attr {}".format(attr))
            new_reg = self._get_register()
            idx = self.class_attributes[class_name][attr]
            att_type = self.class_types[class_name][idx]

            self.generated_code.append("{} = getelementptr inbounds {type}, {type}* {reg}, i32 0, i32 {idx}"
                                       .format(new_reg, type="%{}".format(class_name), reg=cls_reg, idx=idx))
            self.vars[attr] = (att_type, new_reg)
        for k in arguments.keys():
            new_reg = self._get_register()
            self.generated_code.append("{} = alloca {type}".format(new_reg, type=arguments[k]))
            self.generated_code.append("store {type} {value}, {type}* {ptr}"
                                       .format(type=arguments[k], value="%{}".format(k), ptr=new_reg))
            self.vars[k] = (arguments[k], new_reg)
        print("vars {}".format(self.vars))
        self.visitChildren(ctx)
        if fun_type == 'void' and 'ret' not in self.generated_code[-1]:
            self.generated_code.append("ret void")
        elif 'ret' not in self.generated_code[-1]:
            self.generated_code.append("unreachable")
        self.generated_code.append('}')
        # self.current_class = None

    def _generate_function(self, ctx: LatteParser.fundef):
        print("generating code for function")
        name = ctx.ID().getText()
        type = self._getType(ctx)
        print("name: " + name)
        if ctx.arg():
            args = self.visit(ctx.arg())
        else:
            args = {}
        # argTypes = [self._getType(x) for x in ctx.arg()] if ctx.arg() else []
        self.vars = {}
        self.generated_code.append("define {type} @{name} ({args}){{"
                                   .format(type=type, name=name,
                                           args=", ".join([args[k] + ' %' + k for k in args.keys()])))
        for k in args.keys():
            new_reg = self._get_register()
            self.generated_code.append("{} = alloca {type}".format(new_reg, type=args[k]))
            self.generated_code.append(
                "store {type} {value}, {type}* {ptr}".format(type=args[k], value="%{}".format(k), ptr=new_reg))
            self.vars[k] = (args[k], new_reg)
        print(self.vars)
        self.visitChildren(ctx)
        if type == 'void' and 'ret' not in self.generated_code[-1]:
            self.generated_code.append("ret void")
        elif 'ret' not in self.generated_code[-1]:
            self.generated_code.append("unreachable")
        self.generated_code.append("}")

    def _get_next_label(self):
        self.nextLabel += 1
        return "l{}".format(self.nextLabel)

    def _visitAss(self, ctx, op):
        print("visitass")
        if op == '=':
            lhs = ctx.expr()[0]
        else:
            lhs = ctx.expr()
        if isinstance(lhs, LatteParser.EIdContext):
            ident = lhs.ID().getText()
            ltype, register = self.vars[ident]
            if op == '=':
                self.declType = ltype
                right = self.visit(ctx.expr()[1])
                del self.declType
                expr_res_type = self._getType(ctx.expr()[1].expr_type, True)
                if expr_res_type != ltype:
                    prev = right
                    right = self._get_register()
                    self.generated_code.append("{} = bitcast {} {} to {}"
                                               .format(right, expr_res_type, prev, ltype))
                self.generated_code.append("store {type} {value}, {type}* {ptr}".
                                           format(type=ltype, value=right, ptr=register))
                return lhs
            elif op == '++':
                loaded_val = self._get_register()
                new_reg = self._get_register()
                self.generated_code.append("{} = load i32, i32* {}".format(loaded_val, register))
                self.generated_code.append("{} = add nsw i32 {}, 1".format(new_reg, loaded_val))
                self.generated_code.append("store i32 {}, i32* {}".format(new_reg, register))
                return lhs
            elif op == '--':
                loaded_val = self._get_register()
                new_reg = self._get_register()
                self.generated_code.append("{} = load i32, i32* {}".format(loaded_val, register))
                self.generated_code.append("{} = add nsw i32 {}, -1".format(new_reg, loaded_val))
                self.generated_code.append("store i32 {}, i32* {}".format(new_reg, register))
                return lhs
        elif isinstance(lhs, LatteParser.EFieldAccesContext):
            print("assigning to class field")
            ident = lhs.expr()[0].getText()
            ltype, register = self.vars[ident]
            left_class = self.visit(lhs)
            if op == '++':
                elem = self._get_register()
                new_reg = self._get_register()
                self.generated_code.append("{} = load i32, i32* {}".format(elem, left_class))
                self.generated_code.append("{} = add nsw i32 {}, 1".format(new_reg, elem))
                self.generated_code.append("store i32 {}, i32* {}".format(new_reg, left_class))
            elif op == '--':
                elem = self._get_register()
                new_reg = self._get_register()
                self.generated_code.append("{} = load i32, i32* {}".format(elem, left_class))
                self.generated_code.append("{} = add nsw i32 {}, -1".format(new_reg, elem))
                self.generated_code.append("store i32 {}, i32* {}".format(new_reg, left_class))
            else:  # assignment
                rhs = self.visit(ctx.expr()[1])
                rtype = ctx.expr()[1].expr_type
                self.generated_code.append("store {type} {rhs}, {type}* {lhs}"
                                           .format(rhs=rhs, lhs=left_class, type=self._getType(rtype, True)))
                print("ltype: {}".format(rtype))
                pass

        # TODO

    def _get_register(self):
        self._current_register += 1
        return "%r{}".format(self._current_register)

    def _is_register(self, param):
        if param is not None:
            return len(param) > 2 and param[0] == '%' and param[1] == 'r'
        else:
            return False

    def _mark_unreachable_code(self):
        indexes = [i for i, x in enumerate(self.generated_code) if x == '}']
        for i in indexes:
            if "ret" not in self.generated_code[i - 1]:
                self.generated_code.insert(i, "unreachable")

    def _get_constant_string(self, cstr):
        print("get constant string {}".format(cstr))
        if cstr in self.strings:
            print("ok")
            label = self.strings[cstr]
            str_len = len(eval(cstr)) + 1
            string_handle = "getelementptr inbounds( [{len} x i8], [{len} x i8]* {label}, i32 0, i32 0)" \
                .format(len=str_len, label=label)
            print(string_handle)
            return string_handle

    def get_value(self, ctx):
        # Returns element by value
        print("get value")
        # required because field access content returns pointer to element by default.
        if isinstance(ctx, LatteParser.EFieldAccesContext):
            if isinstance(ctx.expr()[1], LatteParser.EFunCallContext):
                return self.visit(ctx)
            new_reg = self._get_register()
            expr_type = self._getType(ctx.expr_type, True)
            self.generated_code.append("{} = load {}, {}* {}"
                                       .format(new_reg, expr_type, expr_type, self.visit(ctx)))
            return new_reg
        else:
            result = self.visit(ctx)
            print("after get_value result {}".format(result))
            return result
            # del LatteParser
