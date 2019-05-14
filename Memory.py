# class FunctionPointer:

#     def __init__(self):
#         self.data = {}

#     def put(self, name, pointer, args):
#         d = {}
#         d['ptr'] = pointer
#         d['args'] = args
#         self.data[name] = d

#     def get(self, name):
#         return self.data[name]

class Memory:

    def __init__(self, name=None): # memory name
        self.data = {}
        
    def has_key(self, name):  # variable name
        pass

    def get(self, name):         # get from memory current value of variable <name>
        # print("in memory get")

        if(name in self.data.keys()):
            # print("Memory.get: in if")
            # print(self.data[name])
            return self.data[name]
        
        # print("Memory.get: after if")
        # print("name = ", name)
        # print("self.data.keys() = ", self.data.keys())
        return None

    def put(self, name, value):  # puts into memory current value of variable <name>
        # print("Memory.put, type(name)", type(name))
        self.data[name] = value

class MemoryStack:
                                                                             
    def __init__(self, memory=None): # initialize memory stack with memory <memory>
        self.stack = []
        if(memory is not None):
            self.stack.append(memory)

    def get(self, name, only_top=False):             # get from memory stack current value of variable <name>
        # print("in get")
        if(only_top is True):
            if(len(self.stack) == 0):
                return None

            return self.stack[len(self.stack)-1].get(name)
        # print("MemoryStack.get: only_top is False")
        for i in range(len(self.stack)-1, -1, -1):
            # print("MemoryStack.get: for interation i =", i)
            # print("name: ", name)
            result = self.stack[i].get(name)
            # print("MemoryStack.get: result", result)
            if(result is not None):
                return result

        return None

    def insert(self, name, value): # inserts into memory stack variable <name> with value <value>
        if(len(self.stack) > 0):
            self.stack[len(self.stack)-1].put(name, value)

    def set(self, name, value): # sets variable <name> to value <value>
        for i in range(len(self.stack)-1, -1, -1):
            # print("MemoryStack.set: for interation i =", i)
            result = self.stack[i].get(name)
            # print("MemoryStack.set: result:", result)
            # if(result is not None):
            #     self.stack[i].put(name, value)
            #     break
            # print("MemoryStack.set: put: stack[i]: i =", i, " name:", name, "value:", value)
            self.stack[i].put(name, value)
            # print("MemoryStack.set: Memory.get test after set: get(name):", self.stack[i].get(name))


    def push(self, memory): # push memory <memory> onto the stack
        self.stack.append(memory)

    def pop(self):          # pops the top memory from the stack
        del self.stack[-1]
