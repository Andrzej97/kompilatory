#!/usr/bin/python

# czy trzeba szczegolowo sprawdzac returna -> dozwolic wtedy wgl w parserze funkcje i inne?

from SymbolTable import SymbolTable
import re
import AST

class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)


    def generic_visit(self, node):        # Called if no explicit visitor function exists for a node.
        print("UNKNOWN STRUCTURE")
        error_found = 1

    # def generic_visit(self, node):        # Called if no explicit visitor function exists for a node.
    #     if isinstance(node, list):
    #         for elem in node:
    #             self.visit(elem)
    #     else:
    #         for child in node.children:
    #             if isinstance(child, list):
    #                 for item in child:
    #                     if isinstance(item, AST.Node):
    #                         self.visit(item)
    #             elif isinstance(child, AST.Node):
    #                 self.visit(child)


class TypeChecker(NodeVisitor):

    symbolTable = SymbolTable()

    # error_found = 0;

    returnedType = {'int' : {}, 'float' : {}, 'string' : {}}
    for i in returnedType.keys():
        returnedType[i] = {}
        for j in returnedType.keys():
            returnedType[i][j] = {}
            for k in ['+','-','/','*','%']:
                returnedType[i][j][k] = 'err'

    returnedType['int']['float']['+'] = 'float'
    returnedType['int']['int']['+'] = 'int'
    returnedType['float']['float']['+'] = 'float'
    returnedType['float']['int']['+'] = 'float'
    returnedType['string']['string']['+'] = 'string'
    returnedType['int']['float']['-'] = 'float'
    returnedType['int']['int']['-'] = 'int'
    returnedType['float']['float']['-'] = 'float'
    returnedType['float']['int']['-'] = 'float'
    returnedType['int']['float']['*'] = 'float'
    returnedType['int']['int']['*'] = 'int'
    returnedType['float']['float']['*'] = 'float'
    returnedType['float']['int']['*'] = 'float'
    returnedType['string']['int']['*'] = 'string'
    returnedType['int']['float']['/'] = 'float'
    returnedType['int']['int']['/'] = 'int'
    returnedType['float']['float']['/'] = 'float'
    returnedType['float']['int']['/'] = 'float'
    returnedType['int']['int']['%'] = 'int'


    returnedTypeRelative = {'int' : {}, 'float' : {}, 'string' : {}}
    for i in returnedTypeRelative.keys():
        returnedTypeRelative[i] = {}
        for j in returnedTypeRelative.keys():
            returnedTypeRelative[i][j] = 'err'

    returnedTypeRelative['int']['float'] = 'int'
    returnedTypeRelative['int']['int'] = 'int'
    returnedTypeRelative['float']['float'] = 'int'
    returnedTypeRelative['float']['int'] = 'int'
    returnedTypeRelative['string']['string'] = 'int'

    # funs = {}

    # where_declared = {}

    # current_function = '*'

    # scope_number = 0

    # loop_number = 0

    # comp = 0

    # tmp_dec = {}


    def visit_Program(self, node):
        self.visit(node.insts)


    def visit_Instructions(self, node):
        for instruction in node.instrs:
            self.visit(instruction)

# # still to develop
# # zrobic moze tak zeby wypisywalo, ze nie umie printowac macierzy - potrzebna integracja z typem jaki bedzie zwracac macierz
#     def visit_Print(self, node):
#         # print(self.symbolTable.scope)
#         array_to_print = self.visit(node.expr)
#         print('arr to print:', array_to_print)
#         for elem in array_to_print:
#             # print('elem:', elem)
#             # print(type(elem))
#             # print(self.symbolTable.get(elem))
#             if self.symbolTable.get(elem) not in ('int','float','string'):
#                 print("CANNOT PRINT", node.expr)
#                 self.error_found = 1



# still to develop
# zrobic moze tak zeby wypisywalo, ze nie umie printowac macierzy - potrzebna integracja z typem jaki bedzie zwracac macierz
    def visit_Print(self, node):
        # print(self.symbolTable.scope)
        array_to_print = self.visit(node.expr)
        # print('arr to print:', array_to_print)
        for elem in array_to_print:
            # print('elem:', elem)
            # print(type(elem))
            # print(self.symbolTable.get(elem))
            if elem not in ('int','float','string'):
                print("CANNOT PRINT", node.expr)
                self.error_found = 1

# # still to develop
# # zastanowic sie, przetestowac czy dla 'ref' wszystko tez bedzie dzialac
#     def visit_Assignment(self, node):
#         id = self.visit(node.id)
#         oper = self.visit(node.oper)[0]
#         expr = self.visit(node.expr)
#         if oper == '=':
#             if isinstance(node.id, AST.Ref):
#                 if id != 'wrong_ref' and id != expr:
#                     print('Error: MISMATCH in types in matrix reference assignment: left:', id, 'right:', expr)
#             # print(isinstance(node.id, AST.Ref))
#             # print(id, expr)
#             else:
#                 if expr == "wrong_matrix":
#                     print(" - ", id)
#                 else:
#                     # print('robie put', id, expr)
#                     # print('assignment id:', id)
#                     # print('id type', type(id))
#                     self.symbolTable.put(str(node.id), expr)
#                     # print(self.symbolTable.get(id))

#         else:
#             actual_type = self.symbolTable.get(id)
#             if actual_type == "none":
#                 print("Error:", id, oper, "\b=", node.expr, "\tused without previous assignment to variable", id)
#             else:   
#                 # print("actual type:", self.symbolTable.get(id))
#                 # print(id, expr, )
#                 ret_type = self.returnedType[actual_type][expr][oper]
#                 if self.returnedType[actual_type][expr][oper] == 'err':
#                     print("Error: MISMATCH TYPE in", id, oper, "\b=", expr, "\b. Previous type was", actual_type)


# still to develop
# zastanowic sie, przetestowac czy dla 'ref' wszystko tez bedzie dzialac
    def visit_Assignment(self, node):
        id = self.visit(node.id)
        oper = self.visit(node.oper)[0]
        expr = self.visit(node.expr)
        if oper == '=':
            if isinstance(node.id, AST.Ref):
                if id != 'wrong_ref' and id != expr:
                    print('Error: MISMATCH in types in matrix reference assignment: left:', id, 'right:', expr)
            # print(isinstance(node.id, AST.Ref))
            # print(id, expr)
            else:
                if expr == "wrong_matrix":
                    print(" - ", node.id)
                else:
                    # print('robie put', id, expr)
                    # print('assignment id:', id)
                    # print('id type', type(id))
                    self.symbolTable.put(str(node.id), expr)
                    # print(self.symbolTable.get(id))

        else:
            if id == "none":
                print("Error:", node.id, oper, "\b=", node.expr, "\tused without previous assignment to variable", node.id)
            else:   
                # print("actual type:", self.symbolTable.get(id))
                # print(id, expr, )
                ret_type = self.returnedType[id][expr][oper]
                if self.returnedType[id][expr][oper] == 'err':
                    print("Error: MISMATCH TYPE in", node.id, oper, "\b=", expr, "\b. Previous type was", id)



    # def visit_Ref(self, node):
    #     # self.symbolTable.print_symbols()
    #     # print('ref:', node.id)
    #     ref_type = self.symbolTable.get(self.visit(node.id))
    #     # print('ref type:', ref_type)
        
    #     id_sizes = re.sub("[x]", " ", ref_type).split()
    #     id_sizes.pop(len(id_sizes) - 1)
    #     for i in range(0, len(id_sizes)):
    #         id_sizes[i] = int(id_sizes[i])

    #     ref_vector = node.vector.exprs
    #     # print('ref_vector:', ref_vector)
    #     ref_sizes = []
    #     for i in ref_vector:
    #         # print(i.value)
    #         ref_sizes.append(i.value)
        
    #     # print('id_sizes:', id_sizes)
    #     # print('ref_sizes:', ref_sizes)

    #     if len(id_sizes) < len(ref_sizes):
    #         print('Error:\tmatrix wrong reference. Real size:', id_sizes, 'while referenced to:', ref_sizes)
    #         return "wrong_ref"
    #     else:
    #         # print(len(ref_sizes))
    #         for i in range(0, len(ref_sizes)):
    #             # print(' in for')
    #             if ref_sizes[i] >= id_sizes[i]:
    #                 print('Error:\tmatrix wrong reference. Real size:', id_sizes, 'while referenced to:', ref_sizes)
    #                 return "wrong_ref"
    #     dimensions_to_skip = len(ref_sizes)
    #     id_sizes = re.sub("[x]", " ", ref_type).split()
    #     # print(id_sizes)
    #     ret_type = ''
    #     for i in range(len(id_sizes), dimensions_to_skip, -1):
    #         ret_type = 'x' + id_sizes[i - 1] + ret_type
    #     # ret_type.pop(0)
    #     return ret_type[1:len(ret_type)]


    def visit_Ref(self, node):
        # self.symbolTable.print_symbols()
        # print('ref:', node.id)
        ref_type = self.visit(node.id)
        # print('ref type:', ref_type)
        
        id_sizes = re.sub("[x]", " ", ref_type).split()
        id_sizes.pop(len(id_sizes) - 1)
        for i in range(0, len(id_sizes)):
            id_sizes[i] = int(id_sizes[i])

        ref_vector = node.vector.exprs
        # print('ref_vector:', ref_vector)
        ref_sizes = []
        for i in ref_vector:
            # print(i.value)
            ref_sizes.append(i.value)
        
        # print('id_sizes:', id_sizes)
        # print('ref_sizes:', ref_sizes)

        if len(id_sizes) < len(ref_sizes):
            print('Error:\tmatrix wrong reference. Real size:', id_sizes, 'while referenced to:', ref_sizes)
            return "wrong_ref"
        else:
            # print(len(ref_sizes))
            for i in range(0, len(ref_sizes)):
                # print(' in for')
                if ref_sizes[i] >= id_sizes[i]:
                    print('Error:\tmatrix wrong reference. Real size:', id_sizes, 'while referenced to:', ref_sizes)
                    return "wrong_ref"
        dimensions_to_skip = len(ref_sizes)
        id_sizes = re.sub("[x]", " ", ref_type).split()
        # print(id_sizes)
        ret_type = ''
        for i in range(len(id_sizes), dimensions_to_skip, -1):
            ret_type = 'x' + id_sizes[i - 1] + ret_type
        # ret_type.pop(0)
        return ret_type[1:len(ret_type)]


    def visit_Assign_operator(self, node):
        return node.oper


    def visit_Vector(self, node):
        elem_type = self.visit(node.expressions)
        # print('elemType:', elem_type)
        first_type = elem_type[0]
        for elem in elem_type:
            if elem != first_type:
                print("Error: Incompatible types in matrix:", elem_type, end='')
                return "wrong_matrix"
        matrix_len = len(node.expressions.exprs)
        # print(node.expressions.exprs)
        # print(len(node.expressions.exprs))
        return str(matrix_len) + 'x' + first_type


    def visit_Expressions(self, node):
        tmp = []
        for expr in node.exprs: 
            tmp.append(self.visit(expr))
        return tmp


    def visit_Choice(self, node):
        self.symbolTable.pushScope()
        self.visit(node.cond)
        self.visit(node.inst1)
        if node.inst2 is not None:
            self.visit(node.inst2)
        self.symbolTable.popScope()


    def visit_While(self, node):
        self.symbolTable.pushScope()
        self.visit(node.cond)
        self.symbolTable.pushLoop()
        self.visit(node.stmt)
        self.symbolTable.popLoop()
        self.symbolTable.popScope()


    def visit_For(self, node):
        self.symbolTable.pushScope()
        # print(node.id)
        # print(type(node.id))
        self.symbolTable.put(str(node.id), 'int')
        # print(self.symbolTable.get(node.id))
        self.visit(node.range)
        # print(self.symbolTable.get(node.id))
        self.symbolTable.pushLoop()
        # print(self.symbolTable.get(node.id))
        self.visit(node.inst)
        # print(self.symbolTable.get(node.id))
        self.symbolTable.popLoop()
        self.symbolTable.popScope()


    def visit_Range(self, node):
        from_type = self.symbolTable.get(node.range_from)
        if from_type != 'none' and from_type != 'int':
            print("Range from should evaluate to int")
            self.error_found = 1
        to_type = self.symbolTable.get(node.range_to)
        # print('to_type', to_type)
        if to_type != 'none' and to_type != 'int':
            print("Range to should evaluate to int")
            self.error_found = 1


    def visit_Return(self, node):
        self.visit(node.ret)


    def visit_Continue(self, node):
        if self.symbolTable.loop <= 0:
            print("Continue used outside loop")


    def visit_Break(self, node):
        if self.symbolTable.loop <= 0:
            print("Break used outside loop")


    def visit_ComInstructions(self, node):
        self.symbolTable.pushScope()
        self.visit(node.instrs)
        self.symbolTable.popScope()


    def visit_Const(self, node):    
        if type(node.value) == str:
            return 'string'
        if type(node.value) == int:
            return 'int'
        if type(node.value) == float:
            return 'float'     


    def visit_BinExpr(self, node):
        # print(node.left)
        # type1 = self.symbolTable.get(str(node.left))
        type1 = self.visit(node.left)
        # print(type1)
        # print(node.right)     
        # type2 = self.symbolTable.get(str(node.right))    
        type2 = self.visit(node.right)
        # print(type2)
        op    = node.op;
        if type1 not in ('int','float','string') or type2 not in ('int','float','string'):
            if type1 != type2:
                print("TYPE MISMATCH IN BIN EXPR", type1, op, type2, " here: ", node.left, op, node.right)
                return 'wrong_bin_expr'
        elif self.returnedType[type1][type2][op] == 'err':
            print("TYPE MISMATCH IN BIN EXPR", type1, op, type2, " here: ", node.left, op, node.right)
            self.error_found = 1;
            return self.returnedType[type1][type2][op]


    def visit_Condition(self, node):
        type1 = self.symbolTable.get(str(node.left))
        type2 = self.symbolTable.get(str(node.right))
        if self.returnedTypeRelative[type1][type2] == 'err':
            print("TYPE MISMATCH IN CONDITION:", type1, node.op, type2, 'here:', node.left, node.op, node.right)
        if self.returnedTypeRelative[type1][type2] != 'int':
            # print(self.returnedTypeRelative[type1][type2])
            print("CONDITION MUST BE INT")


    # def visit_Variable(self, node):
    #     return node.ID

    def visit_Variable(self, node):
        return self.symbolTable.get(str(node.ID))



    def visit_Matrix_operation(self, node):
        type1 = self.symbolTable.get(str(node.matrix1))
        type2 = self.symbolTable.get(str(node.matrix2))
        # print(type1)
        # print(type2)
        if type1 != type2:
            print('Error: matrix operation on incompatible types:', type1, type2, 'here:', node.matrix1, node.dot_oper, node.matrix2)


    def visit_Dot_operation(self, node):
        return node.dot_oper


    def visit_Matrix(self, node):
        self.visit(node.matrix)


    def visit_Matrix_transposed(self, node):
        self.visit(node.id)


    def visit_Minus_transposed(self, node):
        self.visit(node.id)


    def visit_Matrix_function(self, node):
        size = node.arg
        return str(size) + 'x' + str(size) + 'xint'
    