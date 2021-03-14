import Parser
import Error

S_CONDITIONAL_OPERATORS = [
    '==',
    '!=',
    '>=',
    '<=',
    '>',
    '<',
    '!'
]

S_NUMBER_TYPES = [
    'int',
    'float',
    'double'
]

S_NUMBER_OPERATORS = [
    '+',
    '-',
    '*',
    '/'
]

S_OPERATOR_VERBS = {
    '+': 'addition',
    '-': 'subtraction',
    '*': 'multiplication',
    '/': 'division',
    '==': 'comparison',
    '!=': 'comparison',
    '>=': 'comparison',
    '<=': 'comparison',
    '>': 'comparison',
    '<': 'comparison',
    '!': 'comparison'

}

class checker:
    def __init__(self, tree):
        self.tree = tree
        self.errors = []

    def check(self):
        for part in self.tree:
            _ = self.visit(part)

    def visit(self, node):
        if node.type in S_NUMBER_TYPES:
            return node.type
        elif node.type == 'identifier':
            return node.type
        elif node.type == 'binary_operation_node':
            left = self.visit(node.value[0])
            right = self.visit(node.value[2])
            if left == right:
                if node.value[1].type in S_CONDITIONAL_OPERATORS:
                    return 'bool'
                return left
            else:
                self.errors.append(Error.Error(f"invalid {S_OPERATOR_VERBS[node.value[1].type]} between {left} and {right}", 0))
                return 'void'
