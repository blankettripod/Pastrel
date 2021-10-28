def ReadFile(name: str = None) -> str:
    if name is None:
        return ''

    file = open(name, 'r+')
    contents = file.read()

    while not file.closed:
        file.close()

    return contents


def WriteFile(name: str = None, contents: str = ''):
    if name is None:
        return

    file = open(name, 'w+')
    file.write(contents)

    while not file.closed:
        file.close()


def AppendFile(name: str = None, contents: str = ''):
    if name is None:
        return

    file = open(name, 'a+')
    file.write(contents)

    while not file.closed:
        file.close()


def HexToDec(hexNum: str = '') -> int:
    return int(hexNum.replace('0x', '').replace('h', ''), 16)


def DecToHex(decNum: int = 0) -> str:
    return hex(decNum).replace('0x', '').replace('h', '')


def BinToDec(binary: str) -> int:
    return int(binary.replace('0b', '').replace('b', ''), 2)


def BinToHex(binary: str = '') -> str:
    return DecToHex(BinToDec(binary))


def HexToBin(hexadecimal: str = '') -> str:
    return bin(HexToDec(hexadecimal)).replace('0b', '').replace('b', '')


def DecToBin(decimal: int = 0) -> str:
    return bin(decimal).replace('0b', '').replace('b', '')


def EnsureBinary(strInput="", digits=0) -> bin:
    return ((digits*"0")+strInput)[-digits:]
