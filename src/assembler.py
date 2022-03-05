def run():
    registers = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    flags = {
        "eq": False,
        "gt": False,
        "lt": False,
        "zr": False
    }
    memory = {}
    code = []

    file = open("code.cde", 'r')
    code = file.read().split('\n');
    file.close()
    code.append('HLT')

    file = open("memory.mem", 'r')
    mem = file.read().split('\n')
    for line in mem:
        if line != '':
            memory[int(line.split(' ')[0])] = int(line.split(' ')[1])
    file.close()

    pc = 0

    call_stack = []

    def check(num):
        if not num in memory.keys():
            memory[num] = 0

    while pc < len(code):
        command = code[pc].split(' ')[0]
        args = code[pc].split(' ')[1:]
        print(code[pc])
        if command == 'LDR':
            check(int(args[1]))
            registers[int(args[0])] = memory[int(args[1])]
        elif command == 'LRR':
            check(registers[int(args[1])])
            registers[int(args[0])] = memory[registers[int(args[1])]]
        elif command == 'SDR':
            memory[int(args[0])] = registers[int(args[1])]
        elif command == 'SRR':
            memory[registers[int(args[0])]] = registers[int(args[1])]
        elif command == 'MOV':
            registers[int(args[0])] = registers[int(args[1])]
        elif command == 'ADD':
            result = registers[int(args[0])] + registers[int(args[1])]
            if registers[int(args[0])] == registers[int(args[1])]:
                flags['eq'] = True
            if registers[int(args[0])] > registers[int(args[1])]:
                flags['gt'] = True
            if registers[int(args[0])] < registers[int(args[1])]:
                flags['lt'] = True
            if result == 0:
                flags['zr'] = True
            registers[int(args[0])] = result
        elif command == 'SUB':
            result = registers[int(args[0])] - registers[int(args[1])]
            if registers[int(args[0])] == registers[int(args[1])]:
                flags['eq'] = True
            if registers[int(args[0])] > registers[int(args[1])]:
                flags['gt'] = True
            if registers[int(args[0])] < registers[int(args[1])]:
                flags['lt'] = True
            if result == 0:
                flags['zr'] = True
            registers[int(args[0])] = result
        elif command == 'MUL':
            result = registers[int(args[0])] * registers[int(args[1])]
            if registers[int(args[0])] == registers[int(args[1])]:
                flags['eq'] = True
            if registers[int(args[0])] > registers[int(args[1])]:
                flags['gt'] = True
            if registers[int(args[0])] < registers[int(args[1])]:
                flags['lt'] = True
            if result == 0:
                flags['zr'] = True
            registers[int(args[0])] = result
        elif command == 'DIV':
            result = registers[int(args[0])] / registers[int(args[1])]
            if registers[int(args[0])] == registers[int(args[1])]:
                flags['eq'] = True
            if registers[int(args[0])] > registers[int(args[1])]:
                flags['gt'] = True
            if registers[int(args[0])] < registers[int(args[1])]:
                flags['lt'] = True
            if result == 0:
                flags['zr'] = True
            registers[int(args[0])] = result
        elif command == 'AND':
            result = registers[int(args[0])] & registers[int(args[1])]
            if registers[int(args[0])] == registers[int(args[1])]:
                flags['eq'] = True
            if registers[int(args[0])] > registers[int(args[1])]:
                flags['gt'] = True
            if registers[int(args[0])] < registers[int(args[1])]:
                flags['lt'] = True
            if result == 0:
                flags['zr'] = True
            registers[int(args[0])] = result
        elif command == 'OR':
            result = registers[int(args[0])] | registers[int(args[1])]
            if registers[int(args[0])] == registers[int(args[1])]:
                flags['eq'] = True
            if registers[int(args[0])] > registers[int(args[1])]:
                flags['gt'] = True
            if registers[int(args[0])] < registers[int(args[1])]:
                flags['lt'] = True
            if result == 0:
                flags['zr'] = True
            registers[int(args[0])] = result
        elif command == 'XOR':
            result = registers[int(args[0])] ^ registers[int(args[1])]
            if registers[int(args[0])] == registers[int(args[1])]:
                flags['eq'] = True
            if registers[int(args[0])] > registers[int(args[1])]:
                flags['gt'] = True
            if registers[int(args[0])] < registers[int(args[1])]:
                flags['lt'] = True
            if result == 0:
                flags['zr'] = True
            registers[int(args[0])] = result
        elif command == 'CMP':
            result = registers[int(args[0])] - registers[int(args[1])]
            if registers[int(args[0])] == registers[int(args[1])]:
                flags['eq'] = True
            if registers[int(args[0])] > registers[int(args[1])]:
                flags['gt'] = True
            if registers[int(args[0])] < registers[int(args[1])]:
                flags['lt'] = True
            if result == 0:
                flags['zr'] = True
        elif command == 'LSF':
            result = registers[int(args[0])] << registers[int(args[1])]
            if registers[int(args[0])] == registers[int(args[1])]:
                flags['eq'] = True
            if registers[int(args[0])] > registers[int(args[1])]:
                flags['gt'] = True
            if registers[int(args[0])] < registers[int(args[1])]:
                flags['lt'] = True
            if result == 0:
                flags['zr'] = True
            registers[int(args[0])] = result
        elif command == 'RSF':
            result = registers[int(args[0])] >> registers[int(args[1])]
            if registers[int(args[0])] == registers[int(args[1])]:
                flags['eq'] = True
            if registers[int(args[0])] > registers[int(args[1])]:
                flags['gt'] = True
            if registers[int(args[0])] < registers[int(args[1])]:
                flags['lt'] = True
            if result == 0:
                flags['zr'] = True
            registers[int(args[0])] = result
        elif command == 'JMP':
            pc = int(args[0])-1
        elif command == 'JEQ':
            if flags['eq']:
                pc = int(args[0])-1
        elif command == 'JNE':
            if not flags['eq']:
                pc = int(args[0])-1
        elif command == 'JGT':
            if flags['gt']:
                pc = int(args[0])-1
        elif command == 'JLT':
            if flags['lt']:
                pc = int(args[0])-1
        elif command == 'JIN':
            pc = registers[int(args[0])]-1
        elif command == 'CALL':
            call_stack.append(pc)
            pc = int(args[0])
        elif command == 'RET':
            if len(call_stack) > 0:
                pc = call_stack[-1]
                del call_stack[-1]
        elif command == 'CIN':
            memory[int(args[0])] = ord(input("")[0])
        elif command == 'COT':
            check(int(args[0]))
            print(chr(memory[int(args[0])]))
        elif command == 'NOP':
            pass
        elif command == 'HLT':
            print("halted")
        pc += 1

    print(registers)
    print(memory)

