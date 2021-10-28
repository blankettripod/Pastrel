from Instruction import *


def GenerateInstruction(mnemonic="nop") -> Instruction:
    instr = Instruction()

    parts = mnemonic.split(' ')
    if len(parts) < 2:
        parts += ["", ""]

    command = parts[0]
    args = parts[1:]

    args2 = []
    args3 = []

    def formatArg(item) -> str:
        return item.replace(",", "").replace("0x", "").replace("h", "").replace("0b", "").replace("b", "")

    for arg in args:
        if arg == '': continue

        arg = formatArg(arg.upper())

        if arg.upper() in P_REGISTERS.keys():
            args2.append(str(P_REGISTERS[arg.upper()]))
        else:
            args2.append(arg)

    for arg in args2:
        if arg == '': continue

        arg = formatArg(arg.upper())

        if arg.lower() in I_ALU_OPERATIONS.keys():
            args3.append(str(I_ALU_OPERATIONS[arg.lower()]))
        else:
            args3.append(arg)

    print(args)
    print(args3)
    args2 = []

    for arg in args3:
        args2.append(int(formatArg(arg.upper())))

    params: list[Parameter] = []

    for i in range(len(args)):
        if formatArg(args[i].upper()) in P_REGISTERS.keys():
            params.append(Parameter("register", "register", args2[i]))

        elif 'h' in args[i] or '0x' in args[i]:
            params.append(Parameter("address", "hexadecimal", args2[i]))

        elif '0b' in args[i] or 'b' in args[i]:
            params.append(Parameter("address", "binary", args2[i]))

        else:
            params.append(Parameter("address", "decimal", args2[i]))

    if command in I_INSTRUCTIONS.keys():
        instr = I_INSTRUCTIONS[command](*params)

    return instr
