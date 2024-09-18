
import sys
#input_data = sys.stdin.read().strip().split('\n')
input_data = [5, 600,300,400,200,500]
n = int(input_data[0])

weights = []

for i in range(n):
    x = input_data[i+1]
    weights.append(int(x))

weights.sort()


capacity = 1000 + weights[0]

print(capacity)
print(f'cap is {capacity}')

memory = [-1] * (n * capacity)

def solve(n, capacity):
    print(n, capacity)
    # base case
    if memory[n] != -1:
        return memory[n]    
    if n == 0:
        return 0
    if n == 1:
        return weights[0]    
    
    if weights[n-1] > capacity:
        0 + solve(n-1, capacity)
    
    take = weights[n-1] + solve(n-1, capacity-weights[n-1])
    skip = 0 + solve(n-1, capacity) 
    memory[n] = max(skip, take)
    return memory[n]

memory.append(solve(n, capacity))

#for elem in memory:
#    print(elem)


correct = min(memory, key=lambda x: abs(x-capacity))

print(correct)