#!/usr/bin/python


# do analizatora semantycznego
import sys
import ply.yacc as yacc
from Mparser import Mparser
from TreePrinter import TreePrinter
from TypeChecker import TypeChecker

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    Mparser = Mparser()
    parser = yacc.yacc(module=Mparser)
    text = file.read()

    ast = parser.parse(text, lexer=Mparser.scanner)

    # Below code shows how to use visitor
    typeChecker = TypeChecker()   
    typeChecker.visit(ast)







# # do drzewa:
# import sys
# import ply.yacc as yacc
# from Mparser import Mparser
# import TreePrinter


# if __name__ == '__main__':

#     try:
#         filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
#         file = open(filename, "r")
#     except IOError:
#         print("Cannot open {0} file".format(filename))
#         sys.exit(0)

#     Mparser = Mparser()
#     parser = yacc.yacc(module=Mparser)
#     text = file.read()
#     ast = parser.parse(text, lexer=Mparser.scanner)
#     # ast.printTree()




# do parsera:

# import sys
# import scanner
# import ply.yacc as yacc
# from Mparser import Mparser

# if __name__ == '__main__':

#     sys.setrecursionlimit(10000)

#     try:
#         filename = sys.argv[1] if len(sys.argv) > 1 else "example1.m"
#         file = open(filename, "r")
#     except IOError:
#         print("Cannot open {0} file".format(filename))
#         sys.exit(0)

#     Mparser = Mparser()
#     parser = yacc.yacc(module=Mparser)
#     text = file.read()
#     parser.parse(text, lexer=Mparser.scanner)

#     # parser = Mparser.parser
#     # text = file.read()
#     # parser.parse(text, lexer=scanner.lexer)






# do scannera:

# import sys
# import ply.lex as lex
# from scanner import Scanner

# if __name__ == '__main__':

#     try:
#         filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
#         file = open(filename, "r")
#     except IOError:
#         print("Cannot open {0} file".format(filename))
#         sys.exit(0)

#     text = file.read()

#     scanner1 = Scanner()
#     scanner1.build()
#     scanner1.input(text)
#     while True:
#         tok = scanner1.token()
#         if not tok: 
#             break    # No more input
#         column = scanner1.find_tok_column(text, tok)
#         print("(%d,%d): %s(%s)" %(tok.lineno, column, tok.type, tok.value))
