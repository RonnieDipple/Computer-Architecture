#Ls8 will use binary 1, 0s but this implements base 10
import sys

PRINT_BEEJ = 1
HALT = 2
PRINT_NUM = 3
SAVE = 4 #SAVE a value to a register
PRINT_REGISTER = 5 # Print a value from a register
ADD = 6 # regA += regB This add will work the same as the ls 8

# This represents RAM

memory = [None] * 256

# Hardcoded version of above
# memory = [
#     PRINT_BEEJ,#Op code
#     SAVE,
#     65,
#     2,
#     SAVE,
#     20,
#     3,
#     ADD,
#     2,
#     3,
#     PRINT_REGISTER,
#     2,
#     HALT
# ]

register = [0] * 8 # Registers are ulter fast but limited in size and quantity can only store 1 what is called a WORD

# program_counter represents a register that points to a location in memory
program_counter = 0
flag_running = True


def load_memory(filename):
    address = 0
    try:
     with open(filename) as f:
         for line in f:

             # Ignore comments
             comment_split = line.split("#")

             # Strip out whitespace
             num = comment_split[0].strip()

             # Ignore blank lines
             if num == '':
                 continue

             val = int(num)
             memory[address] = val
             address += 1

    except FileNotFoundError:
        print("File not found")
        sys.exit(2)

if len(sys.argv) != 2:
    print("usage: simple_machine.py filename")
    sys.exit(1)

filename = sys.argv[1]
load_memory(filename)

# While is the processor
while flag_running:
    command = memory[program_counter]

    if command == PRINT_BEEJ:
        print("Beej!")
        program_counter += 1

    elif command == HALT:
        flag_running = False
        program_counter += 1

    elif command == PRINT_NUM:
        num = memory[program_counter + 1]
        print(num)
        program_counter += 2
    elif command == SAVE:
        num = memory[program_counter + 1]
        reg = memory[program_counter + 2]
        register[reg] = num
        program_counter += 3
    elif command == PRINT_REGISTER:
        reg = memory[program_counter + 1]
        print(register[reg])
        program_counter += 2
    elif command == ADD:
        reg_a = memory[program_counter + 1]
        reg_b = memory[program_counter + 2]
        register[reg_a] += register[reg_b]
        program_counter += 3


    else:
        print(f"Unknown instruction: {command}")
        sys.exit(1)


