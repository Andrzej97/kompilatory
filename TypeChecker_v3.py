#!/usr/bin/python

class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)


    def generic_visit(self, node):        # Called if no explicit visitor function exists for a node.
        print("(%d,%d): %s(%s)" %(node.lineno, node.lineno, node.type, node.value))
        print("UNKNOWN STRUCTURE")
        error_found = 1



class TypeChecker(NodeVisitor):

    error_found = 0;

    returnedType = {'int' : {}, 'float' : {}, 'string' : {}}
    for i in returnedType.keys():
        returnedType[i] = {}
        for j in returnedType.keys():
            returnedType[i][j] = {}
            for k in ['+','-','/','*','%']:
                returnedType[i][j][k] = []

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

    funs = {}

    where_declared = {}

    current_function = '*'

    scope_number = 0

    loop_number = 0

    comp = 0

    tmp_dec = {}


    def visit_Program(self, node):
        self.visit(node.insts)
        return self.where_declared


    def visit_Instructions(self, node):
        for ins in node.instrs:
            self.visit(ins)


    def visit_Print(self, node):
        if self.visit(node.expr) not in ('int','float','string'):
            print("CANNOT PRINT", node.expr)
            self.error_found = 1


    def visit_Assignment(self, node):
        if node.id in self.where_declared.keys():   
            if self.current_function in self.where_declared[node.id].keys():
                type1 = self.where_declared[node.id][self.current_function]
            elif '*' in self.where_declared[node.id].keys():
                type1 = self.where_declared[node.id]['*']
            else:
                type1 = 'undeclared'
                # print("UNDECLARED VARIABLE",node.id)
                # self.error_found = 1
        else:
            type1 = 'undeclared'
            # print("UNDECLARED VARIABLE",node.id)
            # self.error_found = 1
        type2 = self.visit(node.expr)
        if type1 != 'undeclared' and type1 != type2:
            print("TYPE MISMATCH IN ASSIGNMENT\n")
            self.error_found = 1



    def visit_Expressions(self, node):
        tmp = []
        for expr in node.exprs: 
            tmp.append(self.visit(expr))
        return tmp


    def visit_Matrix_function(self, node):
        if self.visit(node.arg) != 'int':
            print("Matrix function takes not int")
            self.error_found = 1


    def visit_Const(self, node):     
        if type(node.value) == str:
            return 'string'
        if type(node.value) == int:
            return 'int'
        if type(node.value) == float:
            return 'float'


    def visit_While(self, node):
        self.visit(node.cond)
        self.loop_number += 1
        self.visit(node.stmt)
        self.loop_number -= 1

    def visit_For(self, node):
        self.visit(node.id)
        self.visit(node.range)
        self.loop_number += 1
        self.visit(node.inst)
        self.loop_number -= 1

    def visit_Range(self, node):
        from_type = self.visit(node.range_from)
        if from_type != 'undeclared' and from_type != 'int':
            print("Range from should evaluate to int")
            self.error_found = 1
        to_type = self.visit(node.range_to)
        if to_type != 'undeclared' and to_type != 'int':
            print("Range to should evaluate to int")
            self.error_found = 1

    def visit_Continue(self, node):
        if self.loop_number <= 0:
            print("Continue used outside loop")
            self.error_found = 1

    def visit_Break(self, node):
        if self.loop_number <= 0:
            print("Break used outside loop")
            self.error_found = 1

    def visit_Condition(self, node):
        if self.returnedTypeRelative[self.visit(node.left)][self.visit(node.right)] == 'err':
            print("TYPE MISMATCH IN CONDITION\n")
            self.error_found = 1
        if self.returnedTypeRelative[self.visit(node.left)][self.visit(node.right)] != 'int':
            print("CONDITION MUST BE INT")
            self.error_found = 1


    def visit_ComInstructions(self, node):
        # self.tmp_dec = self.where_declared
        # self.comp = 1
        self.visit(node.instrs)
        # self.comp = 0
        # self.where_declared = self.tmp_dec

    def visit_BinExpr(self, node):
        type1 = self.visit(node.left)     
        type2 = self.visit(node.right)    
        op    = node.op;
        if self.returnedType[type1][type2][op] == 'err':
            print("TYPE MISMATCH IN BIN EXPR\n")
            self.error_found = 1;
        return self.returnedType[type1][type2][op]

    # def visit_Variable(self, node):
    #     if node.ID in self.where_declared.keys():
    #         if self.current_function in self.where_declared[node.ID].keys():
    #             return self.where_declared[node.ID][self.current_function]
    #         elif '*' in self.where_declared[node.ID].keys():
    #             return self.where_declared[node.ID]['*']
    #         else:
    #             print("UNDECLARED VARIABLE IN THIS FUN")
    #             self.error_found = 1
    #     else:
    #         print("UNDECLARED VARIABLE", node.ID)
    #         self.error_found = 1

# to jest do poprawy
    def visit_Variable(self, node):
        return 'int'



    def visit_Return(self, node):
        self.visit(node.ret)

