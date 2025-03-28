import sys
# if len(sys.argv) < 2:
#     print("Usage: python3 assembler.py <input_file>")
#     sys.exit(1)

input_file = "test.txt"

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

print(content)

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
            
            else:
                print(f"Error: Syntax error on line {i+1}, either wrong declaration or label formatted wrong, labels need to end with ':'.")
                sys.exit(1)
        
        elif len(temp) == 3:
            if temp[1] == "=":
                if temp[2][0] == "$":
                    try:
                        declarations[temp[0]] = int(temp[2][1:])
                    except ValueError:
                        print(f"Error: Type Error on line {i+1}, '$' is reserved for integers. Context: {temp[2][1:]}")
                        sys.exit(1)
                elif temp[2][0] == "&":
                    #TODO: binary number declaration
                    pass
                elif temp[2][0] == "#":
                    #TODO: hex number declaration
                    pass

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
            
            if len(temp) == 2:
                inst+=int(temp[1][1:])
                print(inst)
                continue

            if temp[2] == r"%reg1":
                if temp[1][0] == "$":
                    inst += int(temp[1][1:-1])
                    print(inst)
                    continue
            

            inst += 128
            print(temp)
            if temp[1][0] == "%" and temp[2][0] == "%":
                #TODO: copy instruction
                pass

