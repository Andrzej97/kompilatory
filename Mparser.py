#!/usr/bin/python

# argument macierzowych funkcji nie intnum a expression(ale tez nie kazde expression jest w porzadku)? - kwestia konwencji
# DONE. dopuszczone kazde expression, nieprawidlowe bede wychwycone w analizatorze syntaktycznym

# unarny minus - dodac lacznosc? priorytet?

from scanner import Scanner
import AST

class Mparser(object):

    def __init__(self):
        self.scanner = Scanner()
        self.scanner.build()
        self.args  = {}
        self.const = {}

    tokens = Scanner.tokens

    precedence = (
       ("nonassoc", 'IFX'),
       ("nonassoc", 'ELSE'),
       ("nonassoc", 'LT', 'GT', 'EQ', 'NE', 'LE', 'GE'),
       ("left", '+', '-'),
       ("left", '*', '/'),
       ("left", 'DOTADD', 'DOTSUB'),
       ("left", 'DOTMUL', 'DOTDIV'),
    )


    def p_error(self, p):
        if p:
            print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(p.lineno, self.scanner.find_tok_column(p), p.type, p.value))
        else:
            print('At end of input')


    def p_program(self, p):
        """program : instructions"""

        p[0] = AST.Program(p[1])
        print(p[0])
                

    def p_instructions(self, p):
        """instructions : instructions instruction
                        | instruction """

        if len(p) == 3:
            p[1].instrs.append(p[2])
            p[0] = p[1]
        else:
            p[0] = AST.Instructions(p[1])
    

    def p_instruction(self, p):
        """instruction : print_instr
                       | assignment
                       | choice_instr
                       | while_instr
                       | for_instr 
                       | return_instr
                       | break_instr
                       | continue_instr
                       | compound_instr"""

        p[0] = p[1]


    def p_print_instr(self, p):
        """print_instr : PRINT expr_list ';'
                       | PRINT error ';' """

        p[0] = AST.Print(p[2])


    def p_assignment(self, p):
        """assignment : id assign_operator expression ';' 
                      | ref assign_operator expression ';' """

        p[0] = AST.Assignment(p[1], p[2], p[3])
  

    def p_ref(self, p):
        """ref : id '[' expr_list ']' """

        p[0] = AST.Ref(p[1], p[3])


    def p_assign_operator(self, p):
        """assign_operator : '='
                           | ADDASSIGN
                           | SUBASSIGN
                           | MULASSIGN
                           | DIVASSIGN"""

        p[0] = AST.Assign_operator(p[1])


    def p_vector(self, p):
        """vector : '[' expressions ']' """

        p[0] = AST.Vector(p[2])


    def p_expressions_or_vectors(self, p):
        """expressions : expression
                       | expressions ',' expression """

        if len(p) == 4:
            p[1].exprs.append(p[3])
            p[0] = p[1]
        else:
            p[0] = AST.Expressions(p[1])


    def p_choice_instr(self, p):
        """choice_instr : IF '(' condition ')' instruction  %prec IFX
                        | IF '(' condition ')' instruction ELSE instruction
                        | IF '(' error ')' instruction  %prec IFX
                        | IF '(' error ')' instruction ELSE instruction """

        if len(p) == 6:
            p[0] = AST.Choice(p[3], p[5])
        else:
            p[0] = AST.Choice(p[3], p[5], p[7])
    

    def p_while_instr(self, p):
        """while_instr : WHILE '(' condition ')' instruction
                       | WHILE '(' error ')' instruction """

        p[0] = AST.While(p[3],p[5])


    def p_for_instr(self, p):
        """for_instr : FOR id '=' range instruction"""

        p[0] = AST.For(p[2], p[4], p[5])


    def p_range(self, p):
        """range : expression ':' expression"""
          
        p[0] = AST.Range(p[1], p[3])


    def p_return_instr(self, p):
        """return_instr : RETURN expression ';' """

        p[0] = AST.Return(p[2])


    def p_continue_instr(self, p):
        """continue_instr : CONTINUE ';' """

        p[0] = AST.Continue()
    

    def p_break_instr(self, p):
        """break_instr : BREAK ';' """

        p[0] = AST.Break()
    

    def p_compound_instr(self, p):
        """compound_instr : '{' instructions '}' """

        p[0] = AST.ComInstructions(p[2])

    
    def p_condition(self, p):
        """condition : expression"""

        p[0] = p[1]


    def p_const(self, p):
        """const : INTNUM
                 | FLOATNUM
                 | STRING"""

        p[0] = AST.Const(p[1])


    def p_expression(self, p):
        """expression : const
                      | id
                      | ref
                      | vector
                      | matrix_operation
                      | matrix_function
                      | minus_matrix
                      | matrix_transposed
                      | expression '+' expression
                      | expression '-' expression
                      | expression '*' expression
                      | expression '/' expression
                      | expression EQ expression
                      | expression NE expression
                      | expression LT expression
                      | expression GT expression
                      | expression LE expression
                      | expression GE expression
                      | '(' expression ')'
                      | '(' error ')'"""

        if len(p) == 2:          
            p[0] = p[1]
        elif len(p) == 4:
            if p[1] == '(':
                 p[0] = p[2]
            else:
                 if p[2] in ['+','-','*','/']:
                       p[0] = AST.BinExpr(p[1],p[2],p[3])
                 else:
                       p[0] = AST.Condition(p[1],p[2],p[3])


    def p_id(self, p):
        """id : ID"""

        p[0] = AST.Variable(p[1], 0)


    def p_matrix_operation(self, p):
        """matrix_operation : matrix dot_operation matrix"""

        p[0] = AST.Matrix_operation(p[1], p[2], p[3])


    def p_dot_operation(self, p):
        """dot_operation : DOTADD
                         | DOTSUB
                         | DOTMUL
                         | DOTDIV"""

        p[0] = AST.Dot_operation(p[1])


    def p_matrix(self, p):
        """matrix : id
                  | minus_matrix
                  | matrix_transposed"""

        p[0] = AST.Matrix(p[1])


    def p_matrix_transposed(self, p):
        """matrix_transposed : matrix "'" """

        p[0] = AST.Matrix_transposed(p[1])


    def p_minus_matrix(self, p):
        """minus_matrix : "-" matrix """

        p[0] = AST.Minus_matrix(p[2])


    def p_matrix_function(self, p):
        """matrix_function : ZEROS '(' expressions ')'
                           | ONES '(' expressions ')'
                           | EYE  '(' expressions ')' """

        p[0] = AST.Matrix_function(p[1], p[3])


    def p_expr_list(self, p):
        """expr_list : expr_list ',' expression
                     | expression """

        if len(p) == 4:
            p[1].exprs.append(p[3])
            p[0] = p[1]
        else:
            p[0] = AST.Expressions(p[1])
    