from Utility import *
from Parameter import *


class Instruction:
    opcode: int
    rr2: int
    rr1: int
    rw: int
    aluOperation: int
    jmpflag: int
    immediate: int
    address: int

    def __init__(self, op=0, rr2=0, rr1=0, rw=0, aluop=0, jmpflag=0, immediate=0, address=0) -> None:
        self.opcode = op
        self.rr2 = rr2
        self.rr1 = rr1
        self.rw = rw
        self.aluOperation = aluop
        self.jmpflag = jmpflag
        self.immediate = immediate
        self.address = address

    def Assemble(self):
        binary = ""

        op = DecToBin(self.opcode)
        rr2 = DecToBin(self.rr2)
        rr1 = DecToBin(self.rr1)
        rw = DecToBin(self.rw)
        aluOperation = DecToBin(self.aluOperation)
        flags = DecToBin(self.jmpflag)
        immediate = DecToBin(self.immediate)
        address = DecToBin(self.address)

        binary += EnsureBinary(op, 6)
        binary += EnsureBinary(rr2, 2)
        binary += EnsureBinary(rr1, 2)
        binary += EnsureBinary(rw, 2)
        binary += EnsureBinary(aluOperation, 4)
        binary += EnsureBinary(flags, 5)
        binary += EnsureBinary(immediate, 1)
        binary += EnsureBinary(address, 10)

        return binary


class Nop(Instruction):
    def __init__(self, *args, **kwargs):
        super().__init__(0)


class LoadRegister(Instruction):
    def __init__(self, destination: Parameter, source: Parameter, *args, **kwargs):

        if source.publicType == "address":
            super().__init__(1, 0, 0,  Parameter.AsDecimal(destination),
                             0, 0, 1, Parameter.AsDecimal(source))

        else:
            super().__init__(1, 0, Parameter.AsDecimal(source), Parameter.AsDecimal(destination))


class StoreRegister(Instruction):
    def __init__(self, destination: Parameter, source: Parameter, *args, **kwargs):

        if destination.publicType == "address":
            super().__init__(2, Parameter.AsDecimal(source), 0, 0,
                             0, 0, 1, Parameter.AsDecimal(destination))

        else:
            super().__init__(2, 0, Parameter.AsDecimal(source), Parameter.AsDecimal(destination))


class MoveRegister(Instruction):
    def __init__(self, destination: Parameter, source: Parameter, *args, **kwargs):

        if destination.publicType == "address":
            super().__init__(3, 0, 0, Parameter.AsDecimal(destination), 0, 0, 1, Parameter.AsDecimal(source))

        else:
            super().__init__(3, Parameter.AsDecimal(source), 0, Parameter.AsDecimal(destination))


class AluOperation(Instruction):
    def __init__(self, operation: Parameter, source1: Parameter, source2: Parameter, destination: Parameter,
                 *args, **kwargs):

        if destination.publicType == "address":
            super().__init__(4, Parameter.AsDecimal(source1), Parameter.AsDecimal(source2), 0,
                             Parameter.AsDecimal(operation), 0, 1, Parameter.AsDecimal(destination))

        else:
            super().__init__(4, Parameter.AsDecimal(source1), Parameter.AsDecimal(source2),
                             Parameter.AsDecimal(destination))


class JumpOperation(Instruction):
    def __init__(self, jumpAddress: Parameter, flag: Parameter, *args, **kwargs):

        if jumpAddress.publicType == "address":
            super().__init__(5, 0, 0, 0,
                             0, Parameter.AsDecimal(flag), 1, Parameter.AsDecimal(jumpAddress))

        else:
            super().__init__(5, 0, Parameter.AsDecimal(jumpAddress), 0,
                             0, Parameter.AsDecimal(flag))


class CoreInOperation(Instruction):
    def __init__(self, port: Parameter, value: Parameter, *args, **kwargs):

        if port.publicType == "address":
            super().__init__(6, 0, 0,  Parameter.AsDecimal(value), 0, 0, 1, Parameter.AsDecimal(port))

        else:
            super().__init__(6, 0, Parameter.AsDecimal(port), Parameter.AsDecimal(value))


class CoreOutOperation(Instruction):
    def __init__(self, port: Parameter, value: Parameter, *args, **kwargs):

        if port.publicType == "address":
            super().__init__(6, Parameter.AsDecimal(value), 0, 0, 0, 0, 1, Parameter.AsDecimal(port))

        else:
            super().__init__(6, Parameter.AsDecimal(value), Parameter.AsDecimal(port))


I_INSTRUCTIONS = {
    "nop": Nop,
    "ldr": LoadRegister,
    "str": StoreRegister,
    "mov": MoveRegister,
    "alu": AluOperation,
    "jmp": JumpOperation,
    "cin": CoreInOperation,
    "out": CoreOutOperation,
}

I_ALU_OPERATIONS = {
    "add": 0,
    "sub": 1,
    "mul": 2,
    "div": 3,
    "lor": 4,
    "and": 5,
    "xor": 6,
    "not": 7,
    "lsf": 8,
    "rsf": 9,
}