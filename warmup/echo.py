import sys
 
for line in sys.stdin:
    data = str(line.strip())
    print(f"{data} {data} {data}")
    break 