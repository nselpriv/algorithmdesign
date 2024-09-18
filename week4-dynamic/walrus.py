import sys

input_data = sys.stdin.read().strip().split('\n')
n = int(input_data[0])

weights = []
for i in range(n):
    x = input_data[i+1]
    weights.append(int(x))

weights.sort()
capacity = 1000 + weights[0]

memory = []
for i in range(n+1):
    memory.append([0] * capacity)
    
for i in range(len(weights)):
    for j in range(capacity):
        if weights[i] > j:
            memory[i+1][j] = memory[i][j]
        else:
            memory[i+1][j] = max(memory[i][j], weights[i] + memory[i][j-weights[i]])

print(min([x for xs in memory for x in xs], key=lambda x: (abs(x - 1000), -x)))