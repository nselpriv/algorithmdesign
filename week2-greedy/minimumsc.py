import sys

input_data = sys.stdin.read().strip().split('\n')
cases = 0

for i in range(1, len(input_data), 3):
    
    sizeOfVector = int(input_data[i])

    one = list(map(int,input_data[i+1].split()))
    two = list(map(int,input_data[i+2].split()))
    #cursed typecasting by oscar OSKA 

    one.sort()
    two.sort(reverse=True) 
    cases += 1 
    dotproduct = 0
    for i in range(sizeOfVector):
     dotproduct += one[i] * two[i]
    print(f'Case #{cases}: {dotproduct}')
