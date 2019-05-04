class Node(object):
    def __str__(self):
        return self.printTree()

    def accept(self, visitor):
        return visitor.visit(self)


class Program(Node):
    def __init__(self, inst):
         self.insts = inst


class Instructions(Node):
    def __init__(self, instr):
        self.instrs = [instr]


class Print(Node):
    def __init__(self,expr):
        self.expr = expr


class Assignment(Node):
    def __init__(self, id, oper, expr):
        self.id = id
        self.oper = oper
        self.expr = expr


class Ref(Node):
    def __init__(self, id, vector):
        self.id = id
        self.vector = vector


class Assign_operator(Node):
    def __init__(self, oper):
        self.oper = oper


# class Vectors(Node):
#     def __init__(self, vectors):
#         self.vectors = [vectors]


class Vector(Node):
    def __init__(self, expressions):
        self.expressions = expressions


class Expressions(Node):
    def __init__(self, exprs):
        self.exprs = [exprs]


class Choice(Node):
    def __init__(self, cond, inst1, inst2=None):
        self.cond = cond
        self.inst1 = inst1
        self.inst2 = inst2


class While(Node):
    def __init__(self, cond, inst):
        self.cond = cond
        self.stmt = inst


class For(Node):
    def __init__(self, id, range, inst):
        self.id = id
        self.range = range
        self.inst = inst


class Range(Node):
    def __init__(self, range_from, range_to):
        self.range_from = range_from
        self.range_to = range_to


class Return(Node):
    def __init__(self,ret):
        self.ret = ret


class Continue(Node):
    def __init__(self):
        pass


class Break(Node):
    def __init__(self):
        pass


class ComInstructions(Node):
    def __init__(self,instr):
        self.instrs = instr


class Const(Node):
    def __init__(self, value):
        self.value = value


class BinExpr(Node):
    def __init__(self, left, op,right):
        self.op = op
        self.left = left
        self.right = right


# class BracExpr(Node):
#     def __init__(self, expr):
#         self.left = expr


class Condition(Node):
    def __init__(self, left, op,right):
        self.left = left
        self.op = op
        self.right = right


class Variable(Node):
     def __init__(self, ID, name):
        self.ID = ID
        self.name = name


class Matrix_operation(Node):
    def __init__(self, matrix1, dot_oper, matrix2):
        self.matrix1 = matrix1
        self.dot_oper = dot_oper
        self.matrix2 = matrix2


class Dot_operation(Node):
    def __init__(self, dot_oper):
        self.dot_oper = dot_oper


class Matrix(Node):
    def __init__(self, matrix):
        self.matrix = matrix


class Matrix_transposed(Node):
    def __init__(self, id):
        self.id = id


class Minus_matrix(Node):
    def __init__(self, id):
        self.id = id


class Matrix_function(Node):
    def __init__(self, func, arg):
        self.func = func
        self.arg = arg
