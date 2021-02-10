class Program:
    def __init__(self, functions):
        self.functions = functions

    def __repr__(self):
        return f'Program {len(self.functions)}'


class Function:
    def __init__(self, rt, n, p, b):
        self.returnType = rt
        self.name = n
        self.p = p
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
        self.tokens = tokens[0]
        self.i = -2
        self.tree = []

    def __getattr__(self, item):
        return self.tree[item]

    def current(self):
        return self.tokens[self.i]

    def advance(self):
        self.i += 1
        if self.i >= len(self.tokens):
            return False
        return True

    def next(self):
        if self.advance():
            return self.current()
        return False

    def parse(self):
        if self.advance():
            parsed = [self.program()]
            return parsed

    def program(self):
        functions = []
        while self.advance():
            functions.append(self.function())
        return functions

    def function(self):
        vtype = self.current()
        if not self.advance():
            return None
        name = self.current()
        if not self.advance():
            return None

        params = []
        while self.next().type != ')':
            params.append(self.variable())

        if not self.advance():
            return None

        body = []
        if self.current().type == '{':
            while self.next().type != '}':
                body.append(self.statement())
                if not self.advance():
                    break

        return Function(vtype, name, params, body)

    def statement(self):
        if self.current().type == 'Identifier':
            if self.advance():
                if self.current().type == '(':
                    self.i -= 1
                    return self.function_call()
                elif self.current().type == '=' :
                    self.i -= 1
                    return self.variable()
                else:
                    self.i -= 1

                if self.current().value == 'return':
                    return ReturnStatement(self.expression())
                elif self.current().value == 'if':
                    if self.next().type == '(':
                        condition = self.condition()
                        if self.next().type == ')':
                            if self.next().type == '{':
                                statements = []
                                while self.next().type != '}':
                                    statements.append(self.statement())
                                return IfStatement(condition ,statements)
                elif self.current().value == 'else':
                    if self.next().value == 'if':
                        self.advance()
                        return ElseStatement(self.statement())
                    elif self.current().type == '{':
                        statements = []
                        while self.next().type != '}':
                            statements.append(self.statement())
                        return ElseStatement(statements)




    def condition(self):
        return NotImplementedError()

    def expression(self):
        return NumberExpression(2)

    def variable(self):
        return NotImplementedError()

    def function_call(self):
        if self.advance():
            params = []
            while self.next().type != ')':
                params.append(self.expression())
                if self.advance():
                    if self.current().type == ',':
                        continue
                    else:
                        self.i -= 1

    def binopnode(self):
        return NotImplementedError()

    def unopnode(self):
        return NotImplementedError()

    def string(self):
        return NotImplementedError()

    def number(self):
        return NotImplementedError()
