"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        self.ram = [0] * 256
        self.register = [0] * 8
        self.pc = 0
        self.flag = False
        self.l_flag = False
        self.g_flag = False

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr

    def load(self, argfile):
        """Load a program into memory."""

        address = 0
        program = []

        f = open(f'examples/{argfile}', 'r')
        commands = f.read().split('\n')
        f.close()

        # Pull the binary and convert it from string
        for command in commands:
            if len(command) >= 8:
                binary = command[:8]
                try:
                    program.append(int(binary, base=2))
                except:
                    pass


        for instruction in program:
            self.ram_write(address, instruction)
            address += 1
        # For now, we've just hardcoded a program:

        #program = [
        #    # From print8.ls8
        #    0b10000010, # LDI R0,8
        #    0b00000000,
        #    0b00001000,
        #    0b01000111, # PRN R0
        #    0b00000000,
        #    0b00000001, # HLT
        #]


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]

        elif op == "CMP":
            if self.register[reg_a] == self.register[reg_b]:
                self.flag = True
                print(f"CMP is {self.flag}")
            elif self.register[reg_a] < self.register[reg_b]:
                self.l_flag = True
                print(f"CMP is {self.flag}")
            elif self.register[reg_a] > self.register[reg_b]:
                self.g_flag = True
                print(f"CMP is {self.flag}")



    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001
        MUL = 0b10100010
        PUSH = 0b01000101
        POP = 0b01000110
        CALL = 0b01010000
        RET = 0b00010001
        ADD = 0b10100000
        CMP = 0b10100111
        JMP = 0b01010100
        JEQ = 0b01010101
        JNE = 0b01010110  
        

        running = True

        while running:
            instruction = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if instruction == LDI:
                self.register[operand_a] = operand_b
                self.pc += 3

            elif instruction == PRN:
                print(f"PRN {self.register[operand_a]}")
                self.pc += 2

            elif instruction == HLT:
                running = False

            elif instruction == MUL:
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3

            elif instruction == ADD:
                self.alu("ADD",operand_a, operand_b)
                self.pc += 3

            elif instruction == PUSH:
                self.register[self.sp] -= 1
                regnum = self.ram[self.pc + 1]
                value = self.register[regnum]
                self.ram[self.register[self.sp]] = value
                print(f"PUSH {self.register[operand_a]}")
                self.pc += 2

            elif instruction == POP:
                value = self.ram[self.register[self.sp]]
                regnum = self.ram[self.pc + 1]
                self.register[regnum] = value
                print(f"POP {self.register[regnum]}")
                self.register[self.sp] += 1
                self.pc += 2

            elif instruction == CMP:
                #Compare the values in two registers. compare = logic = do in alu
                if self.alu("CMP", operand_a, operand_b) is True:
                    print(f"Flag set to {self.flag}")
                    self.pc += 3
                else:
                    print(f"CMP, Comparison {self.flag}, Flag set to {self.flag}")
                    self.pc += 3

            elif instruction == JMP:
                #Jump to the address stored in the given register.
                jumper = self.register[operand_a]
                self.pc = jumper
                print(f"Jumped to {jumper}")

            elif instruction == JEQ:
                #If equal flag is set (true), jump to the address stored in the given register.
                if self.flag == True:
                    jumper = self.register[operand_a]
                    self.pc = jumper
                    print(f"JEQ equal is {self.flag} jumped to {jumper}")
                else:
                    self.pc += 2

            elif instruction == JNE: 
                #If E flag is clear (false, 0), jump to the address stored in the given register.
                if self.flag == False:
                    jumper = self.register[operand_a]
                    self.pc = jumper
                    print(f"JNE, NOT EQUAL, flag is {self.flag}, Jumped to {jumper}")
                else:
                    self.pc += 2        
            
