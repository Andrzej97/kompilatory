import AST

level = 0

def addToClass(cls):

    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator

def getIndent():
    # global level
    tmp = ""
    for l in range(0, level):
        tmp += "| "
    return tmp

class TreePrinter:

    @addToClass(AST.Node)
    def printTree(self):
        raise Exception("printTree not defined in class " + self.__class__.__name__)


    @addToClass(AST.Program)
    def printTree(self):
        return str(self.insts)


    @addToClass(AST.Instructions)
    def printTree(self):
        ret = ""
        x = ""
        for i in self.instrs:
            ret += x + str(i) 
            x = "\n"
        return ret


    @addToClass(AST.Print)
    def printTree(self):
        global level
        ret = ""
        tmp = getIndent()
        level += 1
        ret += tmp + "PRINT\n" + str(self.expr)
        level -= 1
        return ret


    @addToClass(AST.Assignment)
    def printTree(self):
        global level
        ret = ""
        tmp = getIndent()
        level += 1
        ret = tmp + str(self.oper) + "\n" + str(self.id)+ "\n"  + str(self.expr)
        level -= 1
        return ret


    @addToClass(AST.Ref)
    def printTree(self):
        global level
        ret = ""
        tmp = getIndent()
        level += 1
        ret = tmp + "REF" + "\n"  + str(self.id) + "\n" + str(self.vector)
        level -= 1
        return ret


    @addToClass(AST.Assign_operator)
    def printTree(self):
        return str(self.oper)


    # @addToClass(AST.Vectors)
    # def printTree(self):
    #     global level
    #     ret = ""
    #     tmp = getIndent()
    #     level += 1
    #     ret = tmp + "VECTOR" + "\n"
    #     x = ""
    #     for i in self.vectors:
    #         ret += x + str(i) 
    #         x = "\n"
    #     level -= 1
    #     return ret


    @addToClass(AST.Vector)
    def printTree(self):
        global level
        ret = ""
        tmp = getIndent()
        level += 1
        ret = tmp + "VECTOR" + "\n" + str(self.expressions)
        level -= 1
        return ret


    @addToClass(AST.Expressions)
    def printTree(self):
        ret = ""
        x = ""
        for i in self.exprs:
            ret += x + str(i) 
            x = "\n"
        return ret


    @addToClass(AST.Choice)
    def printTree(self):
        global level
        ret = ""
        tmp = getIndent()
        level += 1
        if self.inst2 == None:
            ret += tmp + "IF\n" + str(self.cond) + "\n" +  tmp + "THEN" + "\n" + str(self.inst1)
        else:
            ret += tmp + "IF\n" + str(self.cond) + "\n" + tmp + "THEN" + "\n" + str(self.inst1) + "\n" + tmp + "ELSE\n" + str(self.inst2)
        level -= 1
        return ret


    @addToClass(AST.While)
    def printTree(self):
        global level
        ret = ""
        tmp = getIndent()
        level += 1
        ret += tmp + "WHILE\n"+ str(self.cond) + "\n" + str(self.stmt)
        level -= 1
        return ret


    @addToClass(AST.For)
    def printTree(self):
        global level
        ret = ""
        tmp = getIndent()
        level += 1
        ret += tmp + "FOR\n" + str(self.id) + "\n" + str(self.range) + "\n" + str(self.inst)
        level -= 1
        return ret


    @addToClass(AST.Range)
    def printTree(self):
        global level
        ret = ""
        tmp = getIndent()
        level += 1
        ret += tmp + "RANGE\n"+ str(self.range_from) + "\n" + str(self.range_to)
        level -= 1
        return ret


    @addToClass(AST.Return)
    def printTree(self):
        global level
        ret = ""
        tmp = getIndent()
        level += 1
        ret += tmp + "RETURN\n" + str(self.ret)
        level -= 1
        return ret


    @addToClass(AST.Continue)
    def printTree(self):
        global level
        ret = ""
        tmp = getIndent()
        ret += tmp + "CONTINUE"
        return ret


    @addToClass(AST.Break)
    def printTree(self):
        global level
        ret = ""
        tmp = getIndent()
        ret += tmp + "BREAK"
        return ret


    @addToClass(AST.ComInstructions)
    def printTree(self):
        global level
        ret = ""
        tmp = getIndent()
        ret += str(self.instrs)
        return ret


    @addToClass(AST.Const)
    def printTree(self):
        global level
        ret = ""
        tmp = getIndent()
        ret = tmp + str(self.value)
        return ret


    # @addToClass(AST.BracExpr)
    # def printTree(self):
    #     global level
    #     ret = ""
    #     tmp = getIndent()
    #     ret += str(self.left)
    #     return ret


    @addToClass(AST.BinExpr)
    def printTree(self):
        global level
        ret = ""
        tmp = getIndent()
        level += 1
        ret += tmp + str(self.op) + "\n" + str(self.left) + "\n" + str(self.right)
        level -= 1
        return ret


    @addToClass(AST.Condition)
    def printTree(self):
        global level
        ret = ""
        tmp = getIndent()
        level += 1
        ret += tmp +str(self.op) +"\n" + str(self.left) + "\n" + str(self.right)
        level -= 1
        return ret


    @addToClass(AST.Variable)
    def printTree(self):
        global level
        ret = ""
        tmp = getIndent()
        ret = tmp + str(self.ID)
        return ret


    @addToClass(AST.Matrix_operation)
    def printTree(self):
        global level
        ret = ""
        tmp = getIndent()
        level += 1
        ret = tmp + str(self.dot_oper) + "\n" + str(self.matrix1) + "\n" + str(self.matrix2)
        level -= 1
        return ret


    @addToClass(AST.Dot_operation)
    def printTree(self):
        return str(self.dot_oper)


    @addToClass(AST.Matrix)
    def printTree(self):
        return str(self.matrix)


    @addToClass(AST.Matrix_transposed)
    def printTree(self):
        global level
        ret = ""
        tmp = getIndent()
        level += 1
        ret = tmp + "TRANSPOSE" + "\n" +  str(self.id)
        level -= 1
        return ret


    @addToClass(AST.Minus_matrix)
    def printTree(self):
        global level
        ret = ""
        tmp = getIndent()
        level += 1
        ret = tmp + "UNARY MINUS" + "\n" + str(self.id)
        level -= 1
        return ret


    @addToClass(AST.Matrix_function)
    def printTree(self):
        global level
        ret = ""
        tmp = getIndent()
        level += 1
        ret = tmp + str(self.func) + "\n" + str(self.arg)
        level -= 1
        return ret
