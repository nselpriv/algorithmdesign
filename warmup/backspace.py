import sys
 
output = []

for line in sys.stdin:
    data = str(line.strip())
    for char in data:
        if char == "<" and len(output) > 0:
            output.pop()
        else:
            output.append(char)
    print("".join(output))
    break 