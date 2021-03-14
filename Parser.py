import Token
import Error

P_NUMBERS = [
    'int',
    'float',
    'double'
]

P_OPERATORS = [
    '+',
    '-',
    '*',
    '/'
]

P_FINAL = [
    'int',
    'float',
    'double',
    'identifier'
]

class Node:
    def __init__(self, tpe, value):
        self.type = tpe
        self.value = value
    
    def __repr__(self):
        return f"Node: type = {self.type} value = {self.value}"


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tree = []
        self.errors = []
        self.i = 0

    def expression(self):
        if self.tokens[self.i].type in P_NUMBERS:
            if self.i+1 < len(self.tokens):
                left = self.tokens[self.i]
                if left.type in P_NUMBERS:
                    left = Node(left.type, left.value)
                op = self.tokens[self.i+1]
                if not op.type in P_OPERATORS:
                    self.errors.append(Error.Error("invalid expression", self.line))
                self.i += 2
                right = self.expression()

                if right is not None:
                    if right.type == 'binary_operation_node':

                        if op.type == right.value[1].type:
                            print(f"1 {op}")
                            return Node('binary_operation_node', [left, op, right])

                        elif op.type in ['*', '/'] and right.value[1].type in ['-', '+']:
                            left = Node('binary_operation_node', [left, op, right.value[0]])
                            op = right.value[1]
                            right = right.value[2]
                            self.i += 1
                            return Node('binary_operation_node', [left, op, right])

                        else:
                            return Node('binary_operation_node', [left, op, right])  

                    else:
                        print(f"4 {op}")
                        return Node('binary_operation_node', [left, op, right])

                else:
                    return Node(left.type, left.value)

            else:
                return Node(self.tokens[self.i].type, self.tokens[self.i].value)

        elif self.tokens[self.i].type == 'identifier':
            return Node('identifier', self.tokens[self.i].value)

    def Parse(self):
        self.tree.append(self.expression())
           