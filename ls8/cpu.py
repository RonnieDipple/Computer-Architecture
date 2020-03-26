import sys

# REMEMBER THIS IR MEANS INSTRUCTION REGISTER, BASICALLY THE USER INPUT
# IN PYCHARM PARTS OF THIS LOOK LIKE THEY WILL NOT WORK BUT THEY DO
# PYCHARM IS REGISTERING FALSE POSITIVES?
class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.regs = [0] * 8 # 8 registers emulated
        self.ram = [0] * 256     # Standard 256 Bytes
        self.program_counter = 0  # Program Counter or pc
        self.memory_address = 0
        self.stack = [] # Simple stack

        # for beautification
        self.operations_code = {
            "01000101": {"code": 1, "operation_code": "PUSH"}, # Op code for Push
            "01000110": {"code": 1, "operation_code": "POP"},  # Op code for Pop
            "10000010": {"code": 2, "operation_code": "LDI"}, # Op code for Save
            "10100010": {"code": 2, "operation_code": "MUL"}, # Op code for Multiply
            "01000111": {"code": 1, "operation_code": "PRN"}, # Op code for Print
            "00000001": {"code": 0, "operation_code": "HLT"}  # Op code for Halt
        }

    # Loads the file and adds each line
    def load(self, file: str):
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

        # with - ensures that a resource is "cleaned up" when the code that uses it finishes running
        with open(file, 'r') as file:
            program = file.readlines()
        for instruction in program:
            if "#" in instruction:
                instruction = instruction[: instruction.index("#")].strip()

            self.ram[self.memory_address] = instruction
            self.memory_address += 1

    # Loads ram given a value
    def ram_load(self, value):
        address = len(self.ram.values())
        self.ram[address] = value

    # `ram_read()` should accept the memory_address to read and return the value stored there.
    # MAR Address, MDR data
    def ram_read(self, MAR):
        return self.ram[MAR]

    # `raw_write()`should accept a value to write, and the memory_address to write it to.
    def ram_write(self, MDR, MAR):
        self.ram[MAR] = MDR

    # Register read given register
    def reg_read(self, register):
        return self.regs[register]

    # Register write given register and value
    def reg_write(self, register, value):
        self.regs[register] = value


    # Simulation of an Arithmetic logic unit
    # this performs arithmetic and bitwise operations
    # effectively this is the brain
    def alu(self, operation, reg_1, reg_2):
        """ALU operations_code."""
        #if operation equals operation code given by IR then it performs that operation here
        # effectively this is the brain core
        if operation == "LDI":
            self.regs[reg_1] = reg_2
        elif operation == "PRN":
            print(self.regs[reg_1])
        elif operation == "MUL":
            self.regs[reg_1] = self.regs[reg_1] * self.regs[reg_2]
        elif operation == "PUSH":
            self.stack.append(self.regs[reg_1])
        elif operation == "POP":
            self.regs[reg_1] = self.stack.pop()
        else:
            raise Exception("Invalid operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.program_counter,
            self.ram_read(self.program_counter),
            self.ram_read(self.program_counter + 1),
            self.ram_read(self.program_counter + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.regs[i], end='')

    def run(self):
        """Run the CPU."""

        # flag_running = True
        # MOVED TO SELF.OPERATIONS_CODE IN __INIT__ AND LOGIC IS IN THE BRAIN AKA ALU
        # HLT = 0b00000001  # 1
        # LDI = 0b10000010  # 0b represents binary, 130
        # PRN = 0b01000111  # 71
        # MUL = 0b10100010  # 162
        # POP = 0b1000110  # 70
        # PUSH = 0b1000101  # 69

        while self.program_counter <= self.memory_address:

            IR = self.ram_read(self.program_counter)


            object_map = self.operations_code[IR]
            operation = object_map["operation_code"]

            # OBVIOUSLY HALTS EVERYTHING
            if operation == "HLT":
                return

            # operand aka object that can be manipulated, in this case made into binary
            operand_1 = int(self.ram_read(self.program_counter + 1), 2)
            operand_2 = int(self.ram_read(self.program_counter + 2), 2)

            # Aka a call to the brain passing in the operation code like push, pop etc
            # then values in memory address of operand_1 and operand_2
            self.alu(operation, operand_1, operand_2)
            self.program_counter += 1 + object_map["code"]
