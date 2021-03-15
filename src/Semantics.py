S_LEGAL_OPERATIONS = [
    'int int',
    'double double',
    'float float',
    'double float',
    'float double',
    'float int',
    'double int'
    #int float is not allowed neither is int double
]

class Semantic_Analyser:
    def __init__(self, tree):
        self.tree = tree
        self.errors = []

    def check(self):
        pass

    def visit(self, node):
        if node.type == 'identifier':
            return 'int'
        
        elif node.type == 'unary_operation_node':
            return self.visit(node.value)

        elif node.type == 'binary_operation_node':
            pass
