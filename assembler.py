import sys
if len(sys.argv) < 2:
    print("Usage: python3 assembler.py <input_file>")
    sys.exit(1)

input_file = sys.argv[1]

try:
    with open(input_file, 'r') as asm:
        content = []
        for lines in asm:
            if lines.strip():
                content.append(lines)
except FileNotFoundError:
    print(f"Error: the file {input_file} was not found")
    sys.exit(1)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)


declarations = {


}
for i in range(len(content)):

    # either label or declaration, which are practically the same thing in assembly
    if content[i][0] != " ":
        temp = content[i].split()
        if len(temp) == 1:
            if temp[0][-1] == ":":
                print(temp[0])
                temp[0] = temp[0][0:-1]
                declarations[temp[0]] = i
        
        if len(temp) == 3:
            if temp[1] == "=" and temp[2][0] == "$":
                declarations[temp[0]] = int(temp[2][1:])
        print(temp)
