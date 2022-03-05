from Instruction import Instruction as Instr
from mnemonics import GenerateInstruction
from sys import argv
import Utility

if len(argv) <= 1:
    quit(0)

contents = Utility.ReadFile(argv[1]).replace('\n\n', '\n').split('\n')

output = []

for line in contents:
    output.append(GenerateInstruction(line).Assemble())
    print(output[-1])
print()
final = ""
for item in output:
    final += hex(int(item, 2)).replace('0x', '') + ' '
    print(hex(int(item, 2)).replace('0x', ''))

Utility.WriteFile(argv[1].split('.')[0]+".rom", final)






