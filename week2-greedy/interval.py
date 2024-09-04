import sys
 
output = 0
count = 0
input_data = sys.stdin.read().strip().split('\n')

n = int(input_data[0])

count +=1

intervals = []

output = []

for i in range(n):
    start, finish = input_data[i+1].split(" ")
    #print(f'{start} is start and {finish} is end')
    intervals.append((int(start), int(finish)))


#print("\n sorting \n")
intervals.sort(key=lambda x: x[1]) #sorting on smallest finish time

prev = (0,0)

for elem in intervals: 
    if len(output) == 0:
        output.append(elem)
        prev = elem
    else:
        if elem[0] >= prev[1]:
            output.append(elem)
            prev = elem
    
    

#print("\n output \n")
print(len(output))