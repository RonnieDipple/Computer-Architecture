"""CPU functionality."""

import sys
# Day 1: Get print8.ls8 running
#
# Inventory what is here
# Implement the CPU constructor
# Add RAM functions ram_read() and ram_write()
# Implement the core of run()
# Implement the HLT instruction handler
# Add the LDI instruction
# Add the PRN instruction

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256 # 256 bytes
        self.pc = 0
        self.reg = [0]* 8 # 8 Registers


    def load(self, program):
        """Load a program into memory."""

        address = 0

        # This is the hardcoded version of program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

        try:
            with open(program) as f:
                for line in f:

                    # Ignore comments
                    comment_split = line.split("#")

                    # Strip out whitespace
                    num = comment_split[0].strip()

                    # Ignore blank lines
                    if num == '':
                        continue

                    val = int(num)
                    self.ram[address] = val
                    address += 1

        except FileNotFoundError:
            print("File not found")
            sys.exit(2)

    # ```python
    # x = int("1010101", 2)  # Convert binary string to integer
    # ```

    filename = sys.argv[1]
    load(filename)




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

    # `ram_read()` should accept the address to read and return the value stored there.
    # MAR Address, MDR data
    def ram_read(self, MAR):
        return self.ram[MAR]

    # `raw_write()`should accept a value to write, and the address to write it to.
    def ram_write(self, MDR, MAR):
        self.ram[MAR] = MDR

    # This is the workhorse function of the entire processor.It's the most difficult part to write.
    def run(self):
        # Binary
        # 2** 0 = 1
        # 2** 1 = 2
        # 2** 2 = 4
        # 2** 3 = 8
        # 2** 4 = 16
        # 2** 5 = 32
        # 2** 6 = 64
        # 2** 7 = 128
        # 2** 8 = 256
        # 2** 9 = 512
        # 2** 10 = 1024
        flag_running = True
        HLT = 0b00000001  # 1
        LDI = 0b10000010  # 0b represents binary, 130
        PRN = 0b01000111  # 71

        while flag_running:
            # IR means Instruction Register
            IR = self.ram_read(self.pc)
            op_a = self.ram_read(self.pc + 1)
            op_b = self.ram_read(self.pc + 2)

            # LDI: load "immediate", store a value in a register, or "set this register to this value".
            if IR == LDI:
                self.reg[op_a] = op_b
                self.pc += 3
            # PRN: a pseudo-instruction that prints the numeric value stored in a register.
            elif IR == PRN:
                print(self.reg[self.ram_read(self.pc + 1)])
                self.pc += 2

            # HLT: halt the CPU and exit the emulator.
            elif IR == HLT:
                flag_running = False

            else:
                print("Invalid Command")
