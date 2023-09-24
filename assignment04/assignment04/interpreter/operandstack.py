class OperandStack:
    self.stack = []

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        return self.stack.pop()
    
    def peek(self):
        return self.stack[-1]
    
    def __str__(self):
        return str(self.stack)
