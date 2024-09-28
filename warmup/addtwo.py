import sys

input_data = sys.stdin.read().strip().split('\n')

# First line of input contains useful_items and scouts
a, b = input_data[0].split(" ")
useful_items = int(a)
scouts = int(b)

scout = {}
pointers = []

for index in range(scouts):
    scout[index] = 0
    pointers.append(index)

item_weights = list(map(int, input_data[1].split()))

hi = 0
counter = 0
bounds = scouts

item_weights.sort(reverse=True)

for elems in item_weights:
    if(counter == scouts):
        pointers.sort(reverse=True)
        #print(pointers)
    curr = counter % bounds  
    #print(pointers[curr])
    #print(elems)
    crr = scout[pointers[curr]]       
    setter = crr + elems    
    scout[pointers[curr]] = setter   
    if setter > hi:          
        hi = setter
    counter += 1            
print(hi)
