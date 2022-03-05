from Instruction import *


def GenerateInstruction(mnemonic="nop") -> Instruction:
    instr = Instruction()

    if mnemonic.replace(' ', '').replace('\t', '') == "":
        mnemonic = "nop"

    parts = mnemonic.split(' ')
    if len(parts) < 2:
        parts += ["rax", "rax"]

    command = parts[0]
    args = parts[1:]

    args2 = []
    args3 = []

    def formatArg(item) -> str:
        return item.replace(",", "").replace("0X", "").replace("0B", "")

    for i in range(len(args)):
        if args[i] == '': continue

        args[i] = formatArg(args[i].upper())

        if args[i].upper() in P_REGISTERS.keys():
            args2.append(str(P_REGISTERS[args[i].upper()]))
        else:
            args2.append(args[i])

    for arg in args2:
        if arg == '': continue

        arg = formatArg(arg.upper())

        if arg.lower() in I_ALU_OPERATIONS.keys():
            args3.append(str(I_ALU_OPERATIONS[arg.lower()]))
        else:
            args3.append(arg)

    args2 = []

    for arg in args3:
        args2.append(int(formatArg(arg.upper())))

    params: list[Parameter] = []

    for i in range(len(args)):
        if formatArg(args[i].upper()) in P_REGISTERS.keys():
            params.append(Parameter("register", "Register", args2[i]))

        elif 'h' in args[i] or '0x' in args[i]:
            params.append(Parameter("address", "Hexadecimal", args2[i]))

        elif '0b' in args[i] or 'b' in args[i]:
            params.append(Parameter("address", "Binary", args2[i]))

        else:
            params.append(Parameter("address", "Decimal", args2[i]))

    if command in I_INSTRUCTIONS.keys():
        instr = I_INSTRUCTIONS[command](*params)

    return instr
