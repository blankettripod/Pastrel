from Instruction import Instruction as Instr
from mnemonics import GenerateInstruction

print("Testing Instruction Generation")

instruction = Instr(62, 1, 2, 0, 0, 3, 1, 1000)

print(instruction.Assemble())

print("Testing Mnemonic Assembling")

instruction = GenerateInstruction("ldr rax, rbx")

print(instruction.Assemble())


