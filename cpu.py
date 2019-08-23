"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.fl = [0] * 8

    def load(self, filename):
        """Load a program into memory."""

        try:
            address = 0

            with open(filename) as f:
                for line in f:

                    # parse each line
                    # split before and after each comment symbol
                    comment_split = line.split("#")

                    # remove white space 
                    instruction = comment_split[0].strip()

                    # ignore blanks spaces
                    if instruction == "":
                        continue

                    # convert to binary integer
                    value = int(instruction, 2)

                    # set binary value at current mem address
                    self.ram[address] = value

                    address += 1

        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} not found")
            sys.exit(2)

    def ram_read(self, MAR):
        return self.ram[MAR]


    def ram_write(self, MDR, MAR):
        self.ram[MAR] = MDR

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]

        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]

        elif op == "CMP":
            
            if self.reg[reg_a] < self.reg[reg_b]:
                self.fl[-3] = 1
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.fl[-2] = 1
            elif self.reg[reg_a] == self.reg[reg_b]:
                self.fl[-1] = 1

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

    def run(self):
        """Run the CPU."""
        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001
        MUL = 0b10100010
        CMP = 0b10100111
        JMP = 0b01010100
        JEQ = 0b01010101
        JNE = 0b01010110

        running = True

        while running:
            # self.IR = self.ram[self.PC]
            
            command = self.ram[self.pc]
        

            if command == LDI:
                # print("LDI")
                reg_a = self.ram_read(self.pc + 1)
                reg_b = self.ram_read(self.pc + 2)
                self.reg[reg_a] = reg_b
                self.pc += 3

            elif command == PRN:
                # print("PRN")
                reg = self.ram_read(self.pc + 1)
                print(self.reg[reg])
                self.pc += 2

            elif command == MUL:
                # print("MUL")
                reg_a = self.ram_read(self.pc + 1)
                reg_b = self.ram_read(self.pc + 2)
                self.alu("MUL", reg_a, reg_b)
                self.pc += 3
            
            elif command == CMP:
                reg_a = self.ram_read(self.pc + 1)
                reg_b = self.ram_read(self.pc + 2)
                self.alu("CMP", reg_a, reg_b)
                self.pc += 3
            
            elif command == JMP:
                register = self.reg[self.ram_read(self.pc + 1)]
                self.pc = register
            
            elif command == JEQ:
                register = self.reg[self.ram_read(self.pc + 1)]
                if self.fl[-1] == 1:
                    self.pc = register
                else:
                    self.pc += 2

            elif command == JNE:
                register = self.reg[self.ram_read(self.pc + 1)]
                if self.fl[-1] == 0:
                    self.pc = register
                else:
                    self.pc += 2

            elif command == HLT:
                running = False
    
            else:
                print(f"Unknown command {command}")
                sys.exit(1)

