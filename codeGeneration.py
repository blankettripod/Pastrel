import Parser
import Error

C_OPERATORS = {
    '+': 'ADD',
    '-': 'SUB',
    '*': 'MUL',
    '/': 'DIV'
}

class Generator:
    def __init__(self, nodes):
        self.code = []
        self.memory = {}
        self.nodes = nodes
        self.i = 0

    def generate(self):
        for node in self.nodes:
            self.visit(node)

    def visit(self, node):
        if node.type in ['double', 'float']:
            raise NotImplementedError("Floats and Double are not supported by your processor")

        elif node.type == 'int':
            self.memory[len(self.memory)] = node.value
            return len(self.memory)-1

        elif node.type == 'identifier':
            self.memory[len(self.memory)] = 0
            return len(self.memory)-1

        elif node.type == 'binary_operation_node':
            left = self.visit(node.value[0])
            right = self.visit(node.value[2])
            self.code.append(f'{C_OPERATORS[node.value[1].type]} m{len(self.memory)} m{left} m{right}')
            self.memory[len(self.memory)] = 0
            return len(self.memory)-1

            
            

