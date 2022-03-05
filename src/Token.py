T_TYPE_INT = 'int'
T_TYPE_LONG = 'long'
T_TYPE_HEX = 'hex'
T_TYPE_FLOAT = 'float'
T_TYPE_DOUBLE = 'double'
T_TYPE_STRING = 'string'
T_TYPE_NEWLINE = 'float'
T_TYPE_IDENTIFIER = 'identifier'
T_TYPE_ERROR = 'err'
T_TYPE_UNKNOWN = 'uk'
T_TYPE_ARITHMETIC = 'arithmetic'
T_TYPE_CONDITIONAL = 'conditional'
T_TYPE_KEYWORD = 'keyword'


class Token:
    type: str
    value: any

    def __init__(self, tokenType: str= "null", value=None) -> None:
        self.type = tokenType
        self.value = value

    def __repr__(self) -> str:
        return f"{self.type} Token,  {('value: ' + str(self.value)) if self.value is not None else ''}"


