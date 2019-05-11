#!/usr/bin/python


class SymbolTable(object):


    def __init__(self): # parent scope and symbol table name
        self.symbols = {}
        self.scope = 0
        self.loop = 0
    #
    # def __init__(self, parent, name): # parent scope and symbol table name
    #     self.symbols = {}
    # #

    def put(self, name, type): # put variable symbol or fundef under <name> entry
        self.symbols[(name, self.scope)] = type
    #

    def get(self, name): # get variable symbol or fundef from <name> entry
        for i in range(self.scope, -1, -1):
            # print("i am in for")
            # print((name, i))
            # print(self.symbols.keys())
            if (name, i) in self.symbols.keys() and self.symbols[(name, i)] != "none":
                # print("in if")
                return self.symbols[(name, i)] 
        return "none"
    #     if (name, self.scope) not in self.symbols.keys():
    #         return "none"
    #     return self.symbols[(name, self.scope)]
    # #

    def print_symbols(self):
        for i in self.symbols.keys():
            print(i, self.symbols[i])

    def getParentScope(self):
        pass
    #

    def pushScope(self):
        self.scope += 1
    #

    def popScope(self):
        # print("elems before popScoe:")
        # self.print_symbols()
        for key in self.symbols.keys():
            if key[1] == self.scope:
                self.symbols[key] = "none"
        self.scope -= 1
        # print("elems after popScoe:")
        # self.print_symbols()
    #

    def pushLoop(self):
        self.loop += 1
    #

    def popLoop(self):
        self.loop -= 1
    #