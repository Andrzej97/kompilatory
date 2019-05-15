
import AST
import SymbolTable
from Memory import *
from Exceptions import  *
from visit import *


class Interpreter(object):

    global_mem = MemoryStack(Memory())

    bin_op = {
        '+': lambda x, y: x + y,
        '*': lambda x, y: x * y,
        '-': lambda x, y: x - y,
        '/': lambda x, y: x / y,
        '==': lambda x, y: 1 if x == y else 0,
        '!=': lambda x, y: 1 if x != y else 0,
        '<': lambda x, y: 1 if x < y else 0,
        '<=': lambda x, y: 1 if x <= y else 0,
        '>': lambda x, y: 1 if x > y else 0,
        '>=': lambda x, y: 1 if x >= y else 0,
        '%': lambda x, y: x % y,
        '^': lambda x, y: x ^ y,
        '%': lambda x, y: x % y,
        '&': lambda x, y: x & y,
        '|': lambda x, y: x | y,
        '&&': lambda x, y: 1 if x and y else 0,
        '||': lambda x, y: 1 if x or y else 0,
        '<<': lambda x, y: x << y,
        '>>': lambda x, y: x >> y       
    }


    @on('node')
    def visit(self, node):
        pass


    @when(AST.Program)
    def visit(self, node):
        node.insts.accept(self)


    @when(AST.Instructions)
    def visit(self, node):
        for i in node.instrs:
            i.accept(self)


    @when(AST.Print)
    def visit(self, node):
        to_print = node.expr.accept(self)
        for elem in to_print:
            print(elem)
        return None


    @when(AST.Assignment)
    def visit(self, node):
        value = node.expr.accept(self)
        iid =str(node.id)
        if isinstance(node.id, AST.Ref):
            (ref_matrix, ref_vector) = node.id.accept(self)
            if len(ref_vector) == 1:
                ref_matrix[ref_vector[0]] = value;
            elif len(ref_vector) == 2:
                ref_matrix[ref_vector[0]][ref_vector[1]] = value;
            elif len(ref_vector) == 3:
                ref_matrix[ref_vector[0]][ref_vector[1]][ref_vector[2]] = value;
            elif len(ref_vector) == 4:
                ref_matrix[ref_vector[0]][ref_vector[1]][ref_vector[2]][ref_vector[3]] = value;
        else:
            left_value = node.id.accept(self)
            if(left_value is not None):
                if str(node.oper)[0] == '+':
                    self.global_mem.set(iid, value + left_value)
                elif str(node.oper)[0] == '-':
                    self.global_mem.set(iid, value - left_value)
                elif str(node.oper)[0] == '*':
                    self.global_mem.set(iid, value * left_value)
                elif str(node.oper)[0] == '/':
                    self.global_mem.set(iid, value / left_value)
                else:
                    if self.global_mem.get(iid) is not None:
                        self.global_mem.set(iid, value)
                    else:
                        self.global_mem.insert(iid, value)
            else:
                self.global_mem.insert(iid, value)
        return None


    @when(AST.Ref)
    def visit(self, node):
        ref_matrix = self.global_mem.get(str(node.id))
        ref_vector = node.vector.accept(self)
        return (ref_matrix, ref_vector)


    @when(AST.Vector)
    def visit(self, node):
        return node.expressions.accept(self)


    @when(AST.Expressions)
    def visit(self, node):
        args = []
        for a in node.exprs:
            args.append(a.accept(self))
        return args


    @when(AST.Choice)
    def visit(self, node):
        condition_value = node.cond.accept(self)
        if(condition_value):
            node.inst1.accept(self)
        elif(node.inst2 is not None):
            node.inst2.accept(self)


    @when(AST.While)
    def visit(self, node):
        while(node.cond.accept(self)):
            try:
                node.stmt.accept(self)
            except BreakException:
                break
            except ContinueException:
                continue


    @when(AST.For)
    def visit(self, node):
        (start, end) = node.range.accept(self)
        self.global_mem.insert(str(node.id), start)
        for i in range(start, end + 1):
            self.global_mem.set(str(node.id), i)
            try:
                node.inst.accept(self)
            except BreakException:
                break
            except ContinueException:
                continue
        

    @when(AST.Range)
    def visit(self, node):
        start = node.range_from.accept(self)
        end = node.range_to.accept(self)
        return (start, end)


    @when(AST.Return)
    def visit(self, node):
        value = node.ret.accept(self)
        if type(value) == list:
            value = self.global_mem.get(value[0])
        raise ReturnValueException(value)


    @when(AST.Continue)
    def visit(self, node):
        raise ContinueException


    @when(AST.Break)
    def visit(self, node):
        raise BreakException


    @when(AST.ComInstructions)
    def visit(self, node):
        self.global_mem.push(Memory())
        try:
            node.instrs.accept(self)
        except ReturnValueException as r_ex:
            self.global_mem.pop()
            raise ReturnValueException(r_ex.value)
        except BreakException as b_ex:
            self.global_mem.pop()
            raise BreakException
        except ContinueException as c_ex:
            self.global_mem.pop()
            raise ContinueException
        self.global_mem.pop()


    @when(AST.Const)
    def visit(self, node):
        return node.value


    @when(AST.BinExpr)
    def visit(self, node):
        left = node.left.accept(self)
        right = node.right.accept(self)        
        return self.bin_op[node.op](left, right)


    @when(AST.Condition)
    def visit(self,node):
        left = node.left.accept(self)
        right = node.right.accept(self) 
        return self.bin_op[node.op](left, right)


    @when(AST.Variable)
    def visit(self, node):
        return self.global_mem.get(node.ID)
        

    @when(AST.Matrix_function)
    def visit(self, node):
        matrix = []
        dimensions = node.arg.accept(self)
        dimensions_len = len(dimensions)
        if dimensions_len == 1:
            for i in range(0, dimensions[0]):
                if node.func == "zeros":
                    matrix.append(0)
                elif node.func == "ones":
                    matrix.append(1)
                elif node.func == "eye":
                    if i == 0:
                        matrix.append(1)
                    else:
                        matrix.append(0)
        elif dimensions_len == 2:
            for i in range(0, dimensions[0]):
                vector = []
                for j in range(0, dimensions[1]):
                    if node.func == "zeros":
                        vector.append(0)
                    elif node.func == "ones":
                        vector.append(1)
                    elif node.func == "eye":
                        if i == j:
                            vector.append(1)
                        else:
                            vector.append(0)
                matrix.append(vector)
        return matrix
