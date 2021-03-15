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
    def __init__(self, tpe, value=None, start=0, stop=0):
        self.type = tpe
        self.value = value
        self.start = start
        self.stop = stop
    
    def __repr__(self):
        return f"Node: type={self.type}, value={self.value}"


class Parser:
    def __init__(self, tokens, code=''):
        self.tokens = tokens
        self.tree = []
        self.errors = []
        self.line = 0
        self.lines = []
        self.i = 0
        self.code = code

    def statement(self):
        return self.expression()

         
    def expression(self):
        if self.i < len(self.tokens):# have we reached the end of the file?
            
            if self.tokens[self.i].type in P_NUMBERS: # the current token is a number

                left = self.tokens[self.i]
                left = Node(left.type, left.value, left.start, left.stop)
                self.i += 1

                if self.i < len(self.tokens): # is this the end of the file?

                    if self.tokens[self.i].type in P_OPERATORS: # is this a bin_op?

                        op = self.tokens[self.i]
                        self.i += 1

                        right = self.expression()

                        if right.type == 'err': # something bad happened
                            return right

                        if right.type == 'binary_operation_node':
                            if op.type in ['*', '/'] and right.value[1].type in ['-', '+']: # if we outrank the bin op, swap the nodes to account for bodmas
                                
                                left = Node('binary_operation_node', [left, op, right.value[0]])
                                op = right.value[1]
                                right = right.value[2]
                                return Node('binary_operation_node', [left, op, right], left.start, right.stop) # bin op with swapped nodes (e.g. 1*(2+3) into (1*2)+3 )

                            else: # regular bin op
                                return Node('binary_operation_node', [left, op, right], left.start, right.stop)
                            
                        elif right.type == '(binary_operation_node': # dont do bodmas as a parenthes was used
                            right.type = right.type[1:]
                            return Node('binary_operation_node', [left, op, right], left.start, right.stop)
                        else: # also just a regular bin op node
                            return Node('binary_operation_node', [left, op, right], left.start, right.stop)

                    else:
                        return left # not end of file but the next token is not part of a binary operation
                
                else:
                    return left # end of file; return the found number
            
            elif self.tokens[self.i].type == '-': # un_op_node
                op = self.tokens[self.i]
                self.i += 1

                right = self.expression()
                if right.type == 'err':
                    return right
                
                return Node('unary_operation_node', right)

            elif self.tokens[self.i].type == 'identifier': # variable access or function call
                name = self.tokens[self.i].value
                self.i += 1

                if self.i < len(self.tokens): # may be a function call
                    print(f"possible function call {self.tokens[self.i].type}")
                    if self.tokens[self.i].type == '(': # definitely a function call
                        print("definitely a function call")
                        params = []
                        self.i += 1

                        while self.i < len(self.tokens) and self.tokens[self.i].type != ')': # get all the parameters inside the function call
                            param = self.expression()

                            if param.type == 'err': # something bad happened
                                return Node('err')

                            params.append(param) # add the found parameter to the list

                            if self.tokens[self.i].type == ',': # get next parameter
                                self.i += 1
                                continue

                            elif self.tokens[self.i].type == ')': # end of function call
                                break

                            else:
                                self.errors.append(Error.Error(f"expected ',' found {self.tokens[self.i].type}", self.line, self.tokens[self.i].start, self.tokens[self.i].stop))
                                self.i += 1
                                return Node('err')
                        
                        return Node('function_call_node', [name, params])

                    else: # just a regular variable access
                        return Node('identifier', [name])

                else: # also just a regular variable access. but its the end of the file
                    return Node('identifier', [name])

            elif self.tokens[self.i].type == '(': # bodmas parenthes
                self.i += 1
                exp = self.expression()
                exp.type = '('+exp.type
                if not self.i < len(self.tokens) or self.tokens[self.i].type != ')': # matching parenthes not found
                    self.errors.append(Error.Error(f"expected ')' found {self.tokens[self.i-1].type}", self.line, self.tokens[self.i-1].start, self.tokens[self.i-1].stop, self.code))
                    return Node('err')
                return exp

            elif self.tokens[self.i].type == 'newline': # newline should be passed
                self.line += 1
                self.i += 1
                return self.expression()

            else: # this token wasn't expected
                self.errors.append(Error.Error(f"unexpected token in expression {self.tokens[self.i].type}", self.line, self.tokens[self.i].start, self.tokens[self.i].stop, self.code))
                return Node('err', None, self.tokens[self.i-1].stop+1, self.tokens[self.i-1].stop+1)

        else: # end of file
            self.errors.append(Error.Error("expected expression instead of end of file", self.line, len(self.code), len(self.code)))
            return Node('err') # this is returned so that the parent call doesnt break from Nonetype things
        

    def Parse(self):
        i = 0

        self.tree.append(self.statement())
           