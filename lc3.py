
from enum import Enum
class OPCODES(Enum):
    ADD = 0b0001
    AND = 0b0101
    BR = 0b0000
    JMP = 0b1100
    JSR = 0b0100
    LD = 0b0010
    LDI = 0b1010
    LDR = 0b0110
    LEA = 0b1110
    NOT = 0b1001
    RET = 0b1100
    RTI = 0b1000
    ST = 0b0011
    STR = 0b0111
    TRAP = 0b1111
    




    

    
class LC:
    def __init__(self):
        self.memory = [0 for _ in range(2 ** 16)]
        self.registers = [0 for _ in range(16)]
        self.br = 0  
        self.nzp = 0
        self.pc = 0
  

    def decode(self, instruction: int):
        opcode =  instruction >> 12
        match opcode:
            case OPCODES.ADD:
                dr = instruction >> 9 & (1 << 4) -1
                bit = (instruction >> 5) & 1 
                sr1 = instruction >> 6 & (1 << 4) -1
                if bit:
                   immediate = instruction & (1 << 6) -1 
                   self.addi(dr, sr1, immediate)
                else:
                    sr2 = instruction  & (1 << 4) -1 
                    self.addr(dr,sr1,sr2)
            case OPCODES.AND:
                dr = instruction >> 9 & (1 << 4) - 1
                bit = (instruction >> 5) & 1 
                sr1 = instruction >> 6 & (1 <<4) -1 
                if bit:
                   immediate = instruction & (1 <<6) -1 
                   self.andi(dr, sr1, immediate)
                else:
                    sr2 = instruction  & (1 <<4) -1 
                    self.andr(dr,sr1,sr2)
            case OPCODES.BR:
                nzpBits = (instruction >> 9) & (1 <<4) -1 
                offset = instruction & (1<<10) -1 
                self.branch(nzpBits, offset) 
            case OPCODES.JMP:
                sr = (instruction >> 6) & (1 <<4) -1
                self.jmp(sr)
            case OPCODES.JSR:
                bit = (instruction >> 11) & 1
                if bit:
                    offset = instruction & (1 <<12) -1
                    self.jsr(offset)
                else:
                    sr = (instruction >> 6) & (1 <<4) -1
                    self.jssr(sr)
            case OPCODES.LD:
                ...
            case OPCODES.LDI:
                ...
            case OPCODES.LDR:
                ...
            case OPCODES.LEA:
                ...
            case OPCODES.NOT:
                ...
            case OPCODES.RET:
                ...
            case OPCODES.RTI:
                ...
            case OPCODES.ST:
                ...
            case OPCODES.STR:
                ...
            case OPCODES.TRAP:
                ...
            case _:
                print("Opcode not implemented")
        self.pc+=1
    
    def addr(self,dr, sr1, sr2):
        self.registers[dr] = self.registers[sr1] + self.registers[sr2]
        self.setnzp(dr)

    def addi(self, dr, sr1, immval):
        self.registers[dr] = self.registers[sr1] + immval
        self.setnzp(dr)

    def andr(self, dr, sr1, sr2):
        self.registers[dr]  = self.registers[sr1] & self.registers[sr2]
        self.setnzp(dr)

    def andi(self, dr, sr1, immval):
        self.registers[dr]  = self.registers[sr1] & immval
        self.setnzp(dr)

    def setnzp(self, dr: int):
        if self.registers[dr] == 0:
            self.nzp = 0b010
        elif self.registers[dr] < 0:
            self.nzp = 0b100
        else:
            self.nzp = 0b001

    def branch(self, nzpBits, offset):
        if self.nzp & nzpBits:
            self.pc+=offset

    def jmp(self, sr):
        self.pc = self.registers[sr]
    
    def jsr(self, offset):
        self.registers[6] = self.pc
        self.pc = self.pc + offset

    def jssr(self, sr):
        self.registers[6] = self.pc
        self.pc = self.registers[sr]


