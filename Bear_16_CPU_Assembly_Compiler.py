# This is an assembly compiler for my 16-Bit CPU

# This will work as Command Register 1 (If needed) Data Bus (If needed)
# Example: LD r0 10
# Explaination: LD - Load to register, r0 - Register 1 (Destination), 10 - Immediate
# To do comments you do a ";" then everything after is a comment.

# Data Bus refers to Register 2, Immediate, The Flag Register, The PC Register
# To refer to each of these do: 
#   Register 2: Name of register (Specified in the variable registers) (Example: r1)
#   Immediate: iNumber (Example: i10)
#   Flag: flag
#   PC: pc
# Condition Bus refers to Register 1

registers: List[str] = ["r0", "r1", "r2", "r3", "r4", "r5", "r6", "racc"]
def cleanse(instruction: str) -> list[str] | None:
    if ";" in instruction:
        commentPointer = instruction.index(";")
        instruction = instruction[:commentPointer]
    instruction = instruction.replace("  ", "").strip()

    if instruction == "":
        print(f"Instruction is empty.")
        return None
    instruction_list = instruction.split(" ")
    length = len(instruction_list)
    
    instruction_list[0] = instruction_list[0].upper()
    if length < 2:
        instruction_list.append(None)
    else:
        instruction_list[1] = instruction_list[1].lower()

    if length < 3:
        instruction_list.append(None)
    else:
        instruction_list[2] = instruction_list[2].lower()

    return instruction_list

def opcode(command: str) -> int:
    match command:
        case "NOP": return 0x80 # Does nothing.
        case "LDR": return 0x00 # Loads Data Bus to a register
        case "LDM": return 0x10 # Loads a value at a memory address to a register - uses Data Bus as the address and Condition Bus as the value
        case "STM": return 0x30 # Loads a value in a register to a memory address - uses Data Bus as the address
        case "ADD": return 0x20 # Adds Data Bus to the Acc
        case "SUB": return 0x21 # Subtracts Data Bus to the Acc
        case "NEG": return 0x22 # Negates the Acc
        case "AND": return 0x23 # ANDs Data Bus and the Acc
        case "OR":  return 0x24 # ORs Data Bus and the Acc
        case "NOT": return 0x25 # NOTs the Acc
        case "LTS": return 0x26 # Left Shifts the Acc
        case "RTS": return 0x27 # Right Shifts the Acc
        case "JGT": return 0x09 # Jumps to Data Bus if Condition Bus is greater than 0
        case "JEQ": return 0x0A # Jumps to Data Bus if Condition Bus is equal to 0
        case "JGE": return 0x2B # Jumps to Data Bus if Condition Bus is greater than or equal to 0
        case "JLT": return 0x0C # Jumps to Data Bus if Condition Bus is less than 0
        case "JNE": return 0x0D # Jumps to Data Bus if Condition Bus is not equal to 0
        case "JLE": return 0x0E # Jumps to Data Bus if Condition Bus is less than or equal to 0
        case "JMP": return 0x0F # Jumps to Data Bus
    return 0x80

def operand(operands: list[str] | list[None]) -> (int, str):
    output = 0

    data_bus = operands[-1]
    del operands[-1]
    if len(operands) == 1:
        condition_bus = operands[0]
        output += registers.index(condition_bus)

    data_type_dic = {"r": 0x00, "i": 0x40, "f": 0x80, "p": 0xC0}

    data_type = data_type_dic[data_bus[0]]
    output += data_type

    match data_type:
        case 0x00: return output + registers.index(data_bus) * 8, "r"
        case 0x40: return output, data_bus
        case 0x80: return output, "f"
        case 0xC0: return output, "p"

def fixData(data: int) -> int:
    hexCode = hex(data).replace('0x', '')
    if len(hexCode) > 4:
        hexCode = hexCode[:3]
        print(f"Immediate is too large. Adjusting to: {hexCode}")
    return int(hexCode, 16)

def decode(instructions: list[str]) -> list[int]:
    codes = []
    for instruction in instructions:
        code = 0

        instruction_list = cleanse(instruction)
        if instruction_list == None:
            continue
        
        commandOpcode = opcode(instruction_list[0])
        
        code += commandOpcode * 256

        operandList = []
        if instruction_list[1] != None:
            operandList.append(instruction_list[1])
        if instruction_list[2] != None:
            operandList.append(instruction_list[2])

        dataType = "None"
        if len(operandList) > 0:
            commandOperand, dataType = operand(operandList)
            
            code += commandOperand

        codes.append(code)
        if dataType[0] == "i":
            data = dataType[1:]
            fixedData = fixData(int(data))
            codes.append(fixedData)

    return codes

def loadFile(fileName: str) -> list[str]: # Without extension
    instructions = []
    with open(f"{fileName}.asm", "r") as file:
        for line in file:
            instructions.append(line.replace("\n", ""))

    return instructions

def writeFile(fileName: str, codes: list[int]) -> None:
    with open(f"{fileName}.bin", "w") as file:
        pointer = 1
        for code in codes:
            if pointer >= len(codes):
                file.write(f"{code}")
            else:
                file.write(f"{code}\n")
            pointer += 1

def main():
    print("The Bear-16 Assembler")

    while True:
        fileName = input("Enter the name of the file you would like to load: ")
        try:
            print("Loading file...")
            instructions = loadFile(fileName)
            break
        except FileNotFoundError:
            print("This file does not exist.")

    print("Decoding instructions...")
    codes = decode(instructions)

    print("Writing file...")
    writeFile(fileName, codes)

    print("Complete!")

main()