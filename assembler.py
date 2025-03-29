import sys
if len(sys.argv) < 2:
    print("Usage: python3 assembler.py <input_file>")
    sys.exit(1)

input_file = sys.argv[1]
def hexConv(rHex, i):
    try:
        return int(rHex, 16)
    except ValueError:
        print(f"Error: Syntax error on line {i+1}, '{temp[1][1:]}' is not a valid hexadecimal number")
        sys.exit(1)

try:
    with open(input_file, 'r') as asm:
        content = []
        for lines in asm:
            if lines.strip():
                tempLine = ""
                for char in lines:
                    
                    if char == ";":
                        break
                    tempLine +=char
                lines = tempLine
                content.append(lines)

except FileNotFoundError:
    print(f"Error: the file {input_file} was not found")
    sys.exit(1)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)



machineCode = []

declarations = {


}
for i in range(len(content)):

    # either label or declaration, which are practically the same thing in assembly
    if content[i][0] != " ":
        temp = content[i].split()
        if len(temp) == 1:
            if temp[0][-1] == ":":
                temp[0] = temp[0][0:-1]
                declarations[temp[0]] = i
                continue
            
            else:
                print(f"Error: Syntax error on line {i+1}, either wrong declaration or label formatted wrong, labels need to end with ':'.")
                sys.exit(1)
        
        elif len(temp) == 3:
            if temp[1] == "=":
                if temp[2][0] == "$":
                    try:
                        declarations[temp[0]] = int(temp[2][1:])
                        continue
                    except ValueError:
                        print(f"Error: Type Error on line {i+1}, '$' is reserved for integers. Context: {temp[2][1:]}.")
                        sys.exit(1)
                elif temp[2][0] == "&":
                    try:
                        declarations[temp[0]] = int(temp[2][1:], 2)
                        continue
                    except ValueError:
                        print(f"Error: Syntax error on line {i+1}, {temp[2][1:]} is not a valid binary number")
                elif temp[2][0] == "#":
                    declarations[temp[0]] = hexConv(temp[2][1:], i)
                    continue
                else: 
                    print(f"Error: Syntax error on line {i+1}, '{temp[2][0]}' is an invalid type declaration.")
                    sys.exit(1)


            else:
                print(f"Error: Syntax error on line {i+1}, likely due to character '{temp[1]}'.")
                sys.exit(1)
        else:
            if temp[-1][-1] == ":":
                print(f"Error: Syntax error on line {i+1}, no spaces allowed in label names.")
                sys.exit(1)

            print(f"Error: Syntax error on line {i+1}, unknown Instruction or instruction at wrong indentation level.")
            sys.exit(1)

    elif content[i][0] == " ":
        inst = 0
        temp = content[i][4:].split()
        if temp[0] == "mov":
            
            if len(temp) == 2 or temp[2] == r"%reg0":
                if temp[1][0] == "$":
                    machineCode.append([hex(int(temp[1][1:]))[2:]])
                    continue

                elif temp[1][0] == "&":
                    try:
                        machineCode.append([hex(int(temp[1][1:], 2))[2:]])
                        continue
                    except ValueError:
                        print(f"Error: Syntax error on line {i+1}, '{temp[1][1:]}' is not a valid binary number")
                        sys.exit(1)

                elif temp[1][0] == "#":
                        
                    machineCode.append([temp[1][1:]])
                    continue

                elif temp[1][0] == "!":
                    try:
                        machineCode.append([hex(int(declarations[temp[1][1:]]))[2:]])
                        continue
                    except KeyError:
                        print(f"Error: Name Error, '{temp[1][1:]}' is undefined")
                        sys.exit(1)
                

            inst += 128

            no_cp = False
            noMv = False
            if temp[1][0] == "%" and temp[2][0] == "%":
                if temp[1][1:] == "in":
                    no_cp = True
                    inst += 48

                if temp[2][1:] == "out":
                    noMv = True
                    inst += 6


                if temp[1][-1] != ",":
                    print(f"Error: syntax error on line {i+1}, Context: {' '.join(temp)}, likely due to missing ','.")
                    sys.exit(1)
                if not no_cp:
                    cpFrom = int(temp[1][-2])

                if not noMv:
                    mvTo = int(temp[2][-1])
                cpFrom *= 8
                inst += cpFrom + mvTo
                machineCode.append([hex(inst)[2:]])
                continue

        if temp[0][0] == "j":
            match temp[0]:
                case "jmp":
                    machineCode.append([hex(196)[2:]])
                    continue
                case "jgz":
                    machineCode.append([hex(199)[2:]])
                    continue
                case "jgez":
                    machineCode.append([hex(198)[2:]])
                    continue
                case "jez":
                    machineCode.append([hex(193)[2:]])
                    continue
                case "jlez":
                    machineCode.append([hex(195)[2:]])
                    continue
                case "jlz":
                    machineCode.append([hex(194)[2:]])
                    continue
                case "jnz":
                    machineCode.append([hex(197)[2:]])
                    continue

        if temp[0] == "and":
            machineCode.append(['43'])
        elif temp[0] == "nand":
            machineCode.append(['41'])
        elif temp[0] == "or":
            machineCode.append(['40'])
        elif temp[0] == "nor":
            machineCode.append(['42'])
        elif temp[0] == "xor":
            machineCode.append(['41'])
        elif temp[0] == "add":
            machineCode.append(['44'])
        elif temp[0] == "sub":
            machineCode.append(['45'])
        elif temp[0] == "mul":
            machineCode.append(['46'])
        else:
            print(f"Error: Unrecognized symbol on line {i+1}")
            sys.exit(1)


if len(sys.argv) == 3:
    out = sys.argv[2]
else:
    out = "out.txt"

print(machineCode)

try:
    with open(out, "w+", encoding="utf-8") as output:
        instPerLine = 0
        for i in range(len(machineCode)):
            
            if int(machineCode[i][0], 16) > 255:
                print(f"Error: instruction on line {i+1} is too large (hint: you are working on an 8 bit computer)")

            if instPerLine == 4:
                output.write("\n")
                instPerLine = 0
            output.write(machineCode[i][0] + " ")
            instPerLine += 1
except Exception as e:
    print(f"Error: {e}")
    raise e