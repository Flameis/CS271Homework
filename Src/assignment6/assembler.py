import re
from os import path

# Table of symbols used in assembly code, initialized to include predefined symbols
table = {
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "SCREEN": 16384,
    "KBD": 24576,
    }

for i in range(0,16):
    label = "R" + str(i)
    table[label] = i

variableCursor = 16

# Binary code translations for comp, dest, jump
COMP = {
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "!D": "0001101",
    "!A": "0110001",
    "-D": "0001111",
    "-A": "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "D|A": "0010101",
    "M": "1110000",
    "!M": "1110001",
    "-M": "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101"
    }


DEST = {
    "null": "000",
    "M": "001",
    "D": "010",
    "A": "100",
    "MD": "011",
    "AM": "101",
    "AD": "110",
    "AMD": "111"
    }


JUMP = {
    "null": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
    }

def cleanLine(line):
    # Remove comments and whitespace
    line = re.sub(r"//.*", "", line).strip()
    return line

def normalize(line):
    # Normalize C-instruction
    if not "=" in line:
        line = "null=" + line
    if not ";" in line:
        line = line + ";null"
    return line

def addVariable(label):
    # Add variable to symbol table
    global variableCursor
    table[label] = variableCursor
    variableCursor += 1
    return table[label]

def parseA(line):
    # Parse A-instruction and return the binary code
    line = line[1:]
    if line.isdigit():
        return format(int(line), "016b")
    if line in table:
        return format(table[line], "016b")
    return format(addVariable(line), "016b")

def parceC(line):
    # Parse C-instruction and return the binary code
    line = normalize(line)
    temp = line.split("=")
    dest = DEST.get(temp[0], "000")
    temp = temp[1].split(";")
    comp = COMP.get(temp[0], "000000")
    jump = JUMP.get(temp[1], "000")
    return comp, dest, jump

def translate(lines):
    binary_code = []
    # Translate A-instruction or C-instruction
    for line in lines:
        if line[0] == "@":
            binary_code.append(parseA(line))
        else:
            codes = parceC(line)
            binary_code.append("111" + codes[0] + codes[1] + codes[2])

    return binary_code
    
def firstPass(lines):
    # Remove labels and create symbol table
    global table
    cleaned_lines = []
    line_number = 0

    # Iterate through lines and remove labels
    for line in lines:
        line = cleanLine(line)
        if not line:
            continue

        # Check if line is a label
        if line[0] == "(":
            label = line[1:-1]
            table[label] = line_number
        else:
            cleaned_lines.append(line)
            line_number += 1
        
    return cleaned_lines

def assemble(input_file, output_file):
    # Get path of input file
    input_file = path.join(path.dirname(__file__), input_file)

    # Read input file
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # First pass to remove labels and replace symbols with addresses on the same line
    cleaned_lines = firstPass(lines)

    # Translate instructions
    binary_code = translate(cleaned_lines)
    
    # Create path to output file
    output_file = path.join(path.dirname(__file__), output_file)

    # Write output file
    with open(output_file, 'w') as file:
        for code in binary_code:
            file.write(code + "\n")

if __name__ == "__main__":
    input_file = input("Enter the name of the assembly file: ")
    output_file = input("Enter the name of the output file: ")

    # Add file extensions if not provided
    if not input_file.endswith(".asm"):
        input_file += ".asm"
    if not output_file.endswith(".hack"):
        output_file += ".hack"

    assemble(input_file, output_file)
    print(f"Assembly complete. Output written to {output_file}")