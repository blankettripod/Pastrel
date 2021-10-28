from Utility import *


class Parameter:
    def __init__(self, pType: str = "unknown", _T: any = 'null', value=None):
        self.publicType = pType
        self.type = _T
        self.value = value

    @staticmethod
    def AsRegister(param) -> str:
        if param.type == 'Register':
            return param.value
        elif param.type == 'Hexadecimal':
            return P_REGISTERS[HexToDec(param.value)]
        elif param.type == 'Binary':
            return P_REGISTERS[BinToDec(param.value)]
        elif param.type == 'Decimal':
            return P_REGISTERS[param.value]

    @staticmethod
    def AsHexadecimal(param) -> hex:
        if param.type == 'Register':
            return DecToHex(P_REGISTERS[param.value])
        elif param.type == 'Hexadecimal':
            return param.value
        elif param.type == 'Binary':
            return BinToHex(param.value)
        elif param.type == 'Decimal':
            return DecToHex(param.value)

    @staticmethod
    def AsBinary(param) -> bin:
        if param.type == 'Register':
            return DecToBin(P_REGISTERS[param.value])
        elif param.type == 'Hexadecimal':
            return HexToBin(param.value)
        elif param.type == 'Binary':
            return param.value
        elif param.type == 'Decimal':
            return DecToBin(param.value)

    @staticmethod
    def AsDecimal(param) -> int:
        if param.type == 'Register':
            return P_REGISTERS[param.value]
        elif param.type == 'Hexadecimal':
            return HexToDec(param.value)
        elif param.type == 'Binary':
            return param.value
        elif param.type == 'Decimal':
            return param.value

    def __getattr__(self, item):
        return P_CONVERSIONS[item](self)


P_REGISTERS = {
    'RAX': 0,
    'RBX': 1,
    'RCX': 2,
    'RDX': 3,
}

P_CONVERSIONS = {
    'Register': Parameter.AsRegister,
    'Hexadecimal': Parameter.AsHexadecimal,
    'Binary': Parameter.AsBinary,
    'Decimal': Parameter.AsDecimal,
}
