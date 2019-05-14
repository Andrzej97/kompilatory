
# import AST
# import SymbolTable
# from Memory import *
# from Exceptions import  *
# from visit import *
# import sys

# sys.setrecursionlimit(10000)

# class Interpreter(object):


#     @on('node')
#     def visit(self, node):
#         pass

#     @when(AST.BinExpr)
#     def visit(self, node):
#         r1 = node.left.accept(self)
#         r2 = node.right.accept(self)
#         # try sth smarter than:
#         # if(node.op=='+') return r1+r2
#         # elsif(node.op=='-') ...
#         # but do not use python eval

#     @when(AST.Assignment)
#     def visit(self, node):
#         pass
#     #
#     #

#     # # simplistic while loop interpretation
#     # @when(AST.WhileInstr)
#     # def visit(self, node):
#     #     r = None
#     #     while node.cond.accept(self):
#     #         r = node.body.accept(self)
#     #     return r









import AST
import SymbolTable
from Memory import *
from Exceptions import  *
from visit import *


class Interpreter(object):


    types_table = {'*' : {}}
    current_function = '*'

    global_mem = MemoryStack(Memory())
    function_mem = MemoryStack()
    # function_ptr = FunctionPointer()    

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
        # print("when on AST.Program")
        node.insts.accept(self)


    @when(AST.Instructions)
    def visit(self, node):
        for i in node.instrs:
            i.accept(self)


    @when(AST.Print)
    def visit(self, node):
        # print("when on AST.Print")
        to_print = node.expr.accept(self)
        # print(to_print)
        # print(to_print)
        # if type(to_print) == str:
        #     print(to_print.replace("\"",""))
        # else:
        #     print(to_print)
        for elem in to_print:
            print(elem)
        return None


# TO_DO: popatrzec, czy to dobrze, jak to dziala dla ref
    @when(AST.Assignment)
    def visit(self, node):
        # print("assignment expr type: ", type(node.expr))
        # print("assignment accept expr type: ", type( node.expr.accept(self)))
        # if type(node.expr) in [str,int,float]:
        #     value = node.expr
        # else:
        #     value = node.expr.accept(self)
        
        # print("assignment: now calculating value:")
        value = node.expr.accept(self)
        # print("assignment: value:", value)

        # print("assignment: type(node.id):", type(node.id))
        iid =str(node.id)
        # print("assignment: type(node.id)", type(node.id))
        # print("assignment: iid:", iid)
        # print("assignment: isinstance(node.id, AST.Variable):", isinstance(node.id, AST.Variable))
        # print(iid)
        # print(type(iid))
        # print(iid)
        if not isinstance(node.id, AST.Ref):
            # print("assignment: not ref")
            # print("iid:", iid)
            # print("node.id.accept(self):", node.id.accept(self))
            # print("type(node.id.accept(self)):", type(node.id.accept(self)))
            left_value = node.id.accept(self)
            if(left_value is not None):
                # print(node.oper)
                # print("type(node.oper)", type(node.oper))
                # print("assignment: not ref: not None")
                if str(node.oper)[0] == '+':
                    # self.function_mem.set(iid, value + left_value)
                    self.global_mem.set(iid, value + left_value)
                    # print(value + left_value)
                elif str(node.oper)[0] == '-':
                    self.global_mem.set(iid, value - left_value)
                elif str(node.oper)[0] == '*':
                    self.global_mem.set(iid, value * left_value)
                elif str(node.oper)[0] == '/':
                    self.global_mem.set(iid, value / left_value)
                else:
                    self.global_mem.set(iid, value)
            else:
                # id = str(node.id)
                # print("assignment: id:", id)
                # print("assignment: type(id):", type(id))
                # print("assignment: type(iid):", type(iid))
                # print("assignment global set node.id:", iid, "value:", value)
                # self.global_mem.set(iid, value)
                self.global_mem.set(iid, value)
        else:

            # print("assignment: ref case: id", node.id.id)
            ref_matrix = []
            if(self.function_mem.get(str(node.id.id), True) is not None):
                ref_matrix =  self.function_mem.get(str(node.id.id))
            else:
                ref_matrix = self.global_mem.get(str(node.id.id))
            # print("ref_matrix:", ref_matrix)
            # print("ref_matrix type: ", type(ref_matrix))
            ref_vector = node.id.vector.accept(self)
            # print("assignment: ref_vector", ref_vector)
            # print("type(ref_vector)", type(ref_vector))
            # ref_matrix[0][0] = 1;
            # only few dimensions served:
            if len(ref_vector) == 1:
                ref_matrix[ref_vector[0]] = value;
            elif len(ref_vector) == 2:
                ref_matrix[ref_vector[0]][ref_vector[1]] = value;
            elif len(ref_vector) == 3:
                ref_matrix[ref_vector[0]][ref_vector[1]][ref_vector[2]] = value;
            elif len(ref_vector) == 4:
                ref_matrix[ref_vector[0]][ref_vector[1]][ref_vector[2]][ref_vector[3]] = value;

        return None


    @when(AST.Matrix_function)
    def visit(self, node):
        # print("matrix function node.func:", node.func)
        # print(type(node.func))
        # print("matrix function node.arg:", node.arg)
        # print("matrix function type of node.arg", type(node.arg))
        # print("matrix function type of node.arg.accept(self)", type(node.arg.accept(self)))
        matrix = []
        dimensions = node.arg.accept(self)
        dimensions_len = len(dimensions)
        # print(dimensions_len)
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
            # print(matrix)
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
                # print("vector:", vector)
                matrix.append(vector)
        # for size in dimensions:
        #     print(size)
        #     for i in range(0, size):
        #         matrix.append([])
        #     print(matrix)
        return matrix


    @when(AST.Vector)
    def visit(self, node):
        # print("vector", node.expressions.accept(self))
        return node.expressions.accept(self)

    @when(AST.Expressions)
    def visit(self, node):
        args = []
        # print("in AST.Expressions", node.exprs)
        for a in node.exprs:
            args.append(a.accept(self))
        return args


    @when(AST.Const)
    def visit(self, node):
        return node.value
        # print(node.value)
        # if node.value.isdigit():
        #     return int(node.value)
        # elif node.value.replace(".","",1).isdigit():
        #     return float(node.value)
        # else:
        #     return str(node.value)



    @when(AST.Variable)
    def visit(self, node):
        # if(self.function_mem.get(node.ID, True) is not None):
        #     if type(self.function_mem.get(node.ID)) in (int,str,float):
        #         return self.function_mem.get(node.ID)
        #     return self.function_mem.get(node.ID).accept(self)
        # else:
        #     if type(self.global_mem.get(node.ID)) in (int,str,float):
        #         return self.global_mem.get(node.ID)
        #     return self.global_mem.get(node.ID).accept(self)
        if(self.function_mem.get(node.ID, True) is not None):
            # if type(self.function_mem.get(node.ID)) in (int,str,float):
            # print("variable, get")
            return self.function_mem.get(node.ID)
            # return self.function_mem.get(node.ID).accept(self)
        else:
            # if type(self.global_mem.get(node.ID)) in (int,str,float):
            # print("variable, get")
            # print("variable, node.ID", node.ID)
            # print("variable, get returns:", self.global_mem.get(node.ID))
            return self.global_mem.get(node.ID)
            # return self.global_mem.get(node.ID).accept(self)



    @when(AST.Choice)
    def visit(self, node):
        # print("interpreter ast.choice")
        condition_value = node.cond.accept(self)
        # print("choice: condition_value:", condition_value)
        if(condition_value):
            node.inst1.accept(self)
        elif(node.inst2 is not None):
            # print("Choice, elif")
            # print("choice: elif: node.inst2:", node.inst2)
            # print("choice: elif: type(node.inst2):", type(node.inst2))
            node.inst2.accept(self)


    @when(AST.Condition)
    def visit(self,node):
        # print("interpreter: ast.condition")
        left = node.left.accept(self)
        right = node.right.accept(self) 
        # print("condition: left:", left) 
        # print("condition: type(left):", type(left)) 
        # print("condition: right:", right)  
        # print("condition: type(right):", type(right))
        # print("condition: node.op:", node.op)
        # print("condition: type(node.op):", type(node.op)) 
        # print("returned by condition: ", self.bin_op[node.op](left, right))     
        return self.bin_op[node.op](left, right)


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
        start = node.range.range_from.accept(self)
        # print("start:", start)
        end = node.range.range_to.accept(self)
        # print("end:", end)
        # iterator = str(node.id)
        for i in range(start, end + 1):
            self.global_mem.set(str(node.id), i)
            try:
                node.inst.accept(self)
            except BreakException:
                break
            except ContinueException:
                continue
        # while(node.cond.accept(self)):
        #     try:
        #         node.inst.accept(self)
        #     except BreakException:
        #         break
        #     except ContinueException:
        #         continue


    @when(AST.Continue)
    def visit(self, node):
        raise ContinueException

    @when(AST.Break)
    def visit(self, node):
        raise BreakException


    @when(AST.BinExpr)
    def visit(self, node):
        left = node.left.accept(self)
        right = node.right.accept(self)        
        return self.bin_op[node.op](left, right)



    # @when(AST.Declarations)
    # def visit(self, node):
    #     for d in node.decls:
    #         d.accept(self)

    # @when(AST.Declaration)
    # def visit(self, node):
    #     self.tmp_type = node.type
    #     node.val.accept(self)

    # @when(AST.Inits)
    # def visit(self, node):
    #     for i in node.inits:
    #         i.accept(self)

    # @when(AST.Init)
    # def visit(self, node):
    #     self.types_table[self.current_function][node.id] = self.tmp_type
    #     self.global_mem.insert(node.id, node.val)

    # @when(AST.Functions)
    # def visit(self, node):
    #     for f in node.funcs:
    #         f.accept(self)

    # @when(AST.Function)
    # def visit(self, node):
    #     self.current_function = node.name
    #     self.types_table[self.current_function] = {}
    #     self.function_ptr.put(node.name, node.instrs, node.args)

    # @when(AST.Arguments)
    # def visit(self, node):
    #     args = []
    #     for a in node.args:
    #         args.append(a.accept(self))

    #     return args

    # @when(AST.Argument)
    # def visit(self, node):
    #     return node.id



    # @when(AST.Repeate)
    # def visit(self, node):
    #     while(True):
    #         try:
    #             if(node.cond.accept(self)):
    #                 break
    #             node.stmt.accept(self)
    #         except BreakException:
    #             break
    #         except ContinueException:
    #             continue
            

    # @when(AST.Return)
    # def visit(self, node):
    #     current_function = '*'
    #     value = node.ret.accept(self)
    #     if type(value) == list:
    #         value = self.function_mem.get(value[0])

    #     raise ReturnValueException(value)





    # @when(AST.Call)
    # def visit(self, node):
    #     if node.args == None:
    #         args = []
    #     else:
    #         args = node.args.accept(self)
    #     f_mem = Memory()
    #     f_ptr = self.function_ptr.get(node.name)
    #     if f_ptr['args'] != None:
    #         for i in range(len(f_ptr['args'].accept(self))):
    #             f_mem.put(f_ptr['args'].accept(self)[i], args[i])

    #     self.function_mem.push(f_mem)

    #     f_ptr['ptr'].in_function = True

    #     try:
    #         f_ptr['ptr'].accept(self)
    #     except ReturnValueException as r_ex:
    #         self.function_mem.pop()
    #         return r_ex.value





    # @when(AST.Integer)
    # def visit(self, node):
    #     return node.value

    # @when(AST.Float)
    # def visit(self, node):
    #     return node.value

    # @when(AST.String)
    # def visit(self, node):
    #     return node.value

    # @when(AST.CallArgument)
    # def visit(self,node):
    #     if type(self.function_mem.get(node.id)) in [int, str, float]:
    #         return self.function_mem.get(node.id)
    #     else:
    #         return self.function_mem.get(node.id).accept(self)

    # @when(AST.Argument)
    # def visit(self, node):
    #     self.types_table[self.current_function][node.id] = node.type
    #     return node.id


    # @when(AST.BracExpr)
    # def visit(self, node):
    #     return node.left.accept(self)

    # @when(AST.UnExpr)
    # def visit(self, node):
    #     return node.right