class Program:
    def __init__(self, functions):
        self.functions = functions

    def __repr__(self):
        return f'Program {len(self.functions)}'


class Function:
    def __init__(self, rt, n, b):
        self.returnType = rt
        self.name = n
        self.body = b


class AssignmentStatement:
    def __init__(self, rtype, name, value):
        self.type = rtype
        self.name = name
        self.value = value


class ReturnStatement:
    def __init__(self, expr):
        self.expression = expr


class IfStatement:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body


class ElseStatement:
    def __init__(self, body):
        self.body = body


class WhileStatement:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body


class ForStatement:
    def __init__(self, var, condition, increment, body):
        self.var = var
        self.condition = condition
        self.increment = increment
        self.body = body


class NumberExpression:
    def __init__(self, number):
        self.value = number


class StringExpression:
    def __init__(self, value):
        self.value = value


class BinOpNode:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class UnOpNode:
    def __init__(self, op, value):
        self.op = op
        self.value = value


class FunctionCall:
    def __init__(self, name, params):
        self.name = name
        self.params = params


class VariableAccess:
    def __init__(self, name):
        self.name = name


class Variable:
    def __init__(self, vtype, name, value=None):
        self.type = vtype
        self.name = name
        self.value = value


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.i = 0
        self.tree = []

    def parse(self):
        parsed = [self.program()]
        return parsed

    def program(self):
        functions = []
        while self.i < len(self.tokens):
            functions.append(self.function())
        return functions

    def function(self):
        type = self.tokens[self.i]
        self.i += 1
        name = self.tokens[self.i]
        self.i += 1

    def statement(self):
        pass

    def expression(self):
        pass

    def variable(self):
        pass

    def function_call(self):
        pass

    def binopnode(self):
        pass

    def unopnode(self):
        pass

    def string(self):
        pass

    def number(self):
        pass
