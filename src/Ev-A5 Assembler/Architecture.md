# Envy CPU architecture
##About
this document contains all the information about the binary code that Earch5 and above will use

the binary is displayed in the following format:

`OPCODE` `MNEMONIC` `ARGUMENTS` `DESCRIPTION`

### Operation code
this is a hexadecimal number that is used to determine what instruction is to be executed
### Mnemonic
this is a 3 or 4 letter representation of what the instruction does. this is what is used by an assembler to assemble the code
### Arguments
this is what arguments are to be supplied to the instruction. they can be several types depending on the instruction and the context

these are as follows:

1. Hexadecimal 0xN
2. Binary 0bN
3. Decimal N
4. Register
   1. RAX
   2. RBX
   3. RCX
   4. RDX
5. Memory Location Argument

### Description 
this will provide some context as to what the instruction does and how to use it

## Binary Instruction Layout
from the left it goes



`bits 0-5`: opcode

`bits 6-7`: Register Read 2

`bits 8-9`: Register Read 1

`bits 10-11`: Register Write

`bits 12-15`: ALU Operation

`bits 16-20`: ALU flags

`bit  21`: immediate flag

`bits 22-31`: address / immediate


## Instruction Set Architecture
### CPU Instructions
   `0` `NOP` `none` `Empty instruction. this is ignored by the cpu and optimised by the assembler`

   `1` `LDR` `REGISTER / i+addr` ` loads value from either an address or from immediate into a register`

   `2` `STR` `REGISTER` `Stores value from register into memory location`

   `3` `MOV` `REGISTER, REGISTER` `Moves value from one register to another`
   
   `4` `ALU` `OP, REGISTER, (REGISTER / i+addr)` `does an alu operation on either a register and a register or a register and an immediate value`
   
   `5` `JMP/(J+flag)` `i+addr / REGISTER` `jumps to the address pointed to by either immediate value or indirectly by register`
   
   `6` `CIN` `REGISTER, (REGISTER / i+addr)` `stores value gathered from a port specified from either a register or an immediate`

   `7` `OUT` `(REGISTER / i+addr), REGISTER` `sends value gathered to a port specified from either a register or an immediate`
### ALU Instructions

   `0` `ADD`
   `1` `SUB`
   `2` `MUL`
   `3` `DIV`
   `4` `LOR`
   `5` `AND`
   `6` `XOR`
   `7` `NOT`
   `8` `LSF`
   `9` `RSH`