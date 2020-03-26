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
        # self.ram = [0] * 256 # 256 bytes
        self.ram = {}
        self.pc = -1
        self.reg = [0]* 8 # 8 Registers

    # Increases the Program Counter
    @property
    def counter(self):
        self.pc += 1
        return self.pc


    def load(self, program):
        """Load a program into memory."""

        # memory_address = 0

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
        #     self.ram[memory_address] = instruction
        #     memory_address += 1

        with open(program, 'r') as f:
            for line in f:

                # Ignore comments
                line = line.split("#")[0]


                if line:
                    #Binary conversertion from String to an int with base 2
                    binary = int(line, 2)
                    self.ram_load(binary)

    # ```python
    # x = int("1010101", 2)  # Convert binary string to integer
    # ```

    # `ram_read()` should accept the memory_address to read and return the value stored there.
    # MAR Address, MDR data
    def ram_read(self, MAR):
        return self.ram[MAR]

    # `raw_write()`should accept a value to write, and the memory_address to write it to.
    def ram_write(self, MDR, MAR):
        self.ram[MAR] = MDR

    # loads ram based on value given
    def ram_load(self, value):
        address = len(self.ram.values())
        self.ram[address] = value

    # Register read given register
    def reg_read(self, register):
        return self.reg[register]

    # Register write given register and value
    def reg_write(self, register, value):
        self.reg[register] = value

    def alu(self, op, reg_a, reg_b):
        """ALU operations_code."""

        if op == "MUL":
            self.reg_write(reg_a, self.reg[reg_a] * self.reg[reg_b])
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
        MUL = 0b10100010  # 162
        POP = 0b1000110 # 70
        PUSH = 0b1000101 # 69

        while flag_running:
            IR = self.ram_read(self.counter)
            # # IR means Instruction Register
            # IR = self.ram_read(self.program_counter)
            # op_a = self.ram_read(self.program_counter + 1)
            # op_b = self.ram_read(self.program_counter + 2)

            # LDI: load "immediate", store a value in a register, or "set this register to this value".
            if IR == LDI:
                reg_a = self.ram_read(self.counter)
                value = self.ram_read(self.counter)
                self.reg_write(reg_a, value)
            # PRN: a pseudo-instruction that prints the numeric value stored in a register.
            elif IR == PRN:
                reg_a = self.ram_read(self.counter)
                value = self.reg_read(reg_a)
                print(value)
            #Multiply
            elif IR == MUL:
                reg_a = self.ram_read(self.counter)
                reg_b = self.ram_read(self.counter)
                self.alu("MUL", reg_a, reg_b)

            elif IR == PUSH:
                reg_a = self.ram_write(self.counter)
                value = self.ram

            elif IR == POP:
                reg_a = self.ram_write(self.counter)


            # HLT: halt the CPU and exit the emulator.
            elif IR == HLT:
                flag_running = False

            else:
                print("Invalid Command")





