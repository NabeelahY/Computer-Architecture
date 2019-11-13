"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0
        self.sp = 0

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:
        program = []
        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        if len(sys.argv) != 2:
            print("usage: ls8.py <filename>")
            sys.exit(1)


        try:
            with open(sys.argv[1]) as file:
                for line in file:
                    comment_split = line.split("#")

                    num = comment_split[0].strip()

                    if len(num) == 0:
                        continue

                    value = int(num, 2)
                    program.append(value)

        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} not found")
            sys.exit(2)

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

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

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    def run(self):
        """Run the CPU."""
        PRN = 0b01000111
        LDI = 0b10000010
        HLT = 0b00000001
        MUL = 0b10100010
        PUSH = 0b01000101
        POP = 0b01000110

        running = True

        while running:
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            if IR == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3

            elif IR == PRN:
                print(self.reg[operand_a])
                self.pc += 2

            elif IR == MUL:
                print(self.reg[operand_a] * self.reg[operand_b])
                self.pc += 3

            elif IR == PUSH:
                val = self.reg[operand_a]
                self.reg -= 1
                self.ram_write(self.reg, val)
                self.pc += 3

            elif IR == POP:
                val = self.reg[operand_a]
                self.reg += 1
                self.ram_write(self.reg, val)
                self.pc += 3

            elif IR == HLT:
                running = False


