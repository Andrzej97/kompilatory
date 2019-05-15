
class Memory:

    def __init__(self, name=None): # memory name
        self.data = {}
        
    def has_key(self, name):  # variable name
        pass

    def get(self, name):         # get from memory current value of variable <name>
        if(name in self.data.keys()):
            return self.data[name]
        return None

    def put(self, name, value):  # puts into memory current value of variable <name>
        self.data[name] = value

class MemoryStack:
                                                                             
    def __init__(self, memory=None): # initialize memory stack with memory <memory>
        self.stack = []
        if(memory is not None):
            self.stack.append(memory)

    def get(self, name, only_top=False):             # get from memory stack current value of variable <name>
        if(only_top is True):
            if(len(self.stack) == 0):
                return None
            return self.stack[len(self.stack)-1].get(name)
        for i in range(len(self.stack)-1, -1, -1):
            result = self.stack[i].get(name)
            if(result is not None):
                return result
        return None

    def insert(self, name, value): # inserts into memory stack variable <name> with value <value>
        if(len(self.stack) > 0):
            self.stack[len(self.stack)-1].put(name, value)

    def set(self, name, value): # sets variable <name> to value <value>
        for i in range(len(self.stack)-1, -1, -1):
            result = self.stack[i].get(name)
            if(result is not None):
                self.stack[i].put(name, value)
                break

    def push(self, memory): # push memory <memory> onto the stack
        self.stack.append(memory)

    def pop(self):          # pops the top memory from the stack
        del self.stack[-1]
