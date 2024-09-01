import sys
 
output = []
count = 0
input_data = sys.stdin.read().strip().split('\n')

n, m = input_data[0].split(" ")

#n = number of lines
#m = uhhhhh
preferences = dict()  # name of person that likes and a stack of preferences
man = dict() # current matchings
woman = dict() 

matchstack = len(input_data[1].split(" "))-1
for i in range(int(n)):
    check = i<int(int(n)/2)
    current = input_data[i+1].split(" ")
    name = current.pop(0)
    matchstack = len(current)
    

    #print(f'we got {name} {i} {check}')
    tempref = []
    if check:
        man[name] = "" #this will be a proposer so we add it to outputs 
    else:
        woman[name] = ""

    current.reverse()  
    for j in range(0, matchstack): 
        #print(matchstack)
        #print(j)
        value = (current[j], j)
        tempref.append(value)

    preferences[name] = tempref 
    #if(check):
       #print(f'we got {name} adding it to actual output')

#print("\n setup done \n")

#for key in preferences: 
   # print(f'{key} {preferences[key].pop()}')


def matchy(proposer, proposee):
    #print(f'{proposer} wants to ask {proposee}')
    current = woman[proposee]
    #print(f'{proposee} is currently matched with {woman[proposee]}')
    if current == "":
        #print(f'{proposee} is not matched')
        man[proposer] = proposee
        woman[proposee] = proposer
        #print(f'{proposer} is matched with {proposee}')
    else:
        curr = 0
        new = 0
        for elem in preferences[proposee]:
            if elem[0] == proposer:
                new = elem[1]
            if elem[0] == current:
                curr = elem[1]
        if new > curr:
            #print(f'{proposer} is better than {current} for {proposee}')
            man[proposer] = proposee
            woman[proposee] = proposer
            man[current] = ""
        else:
            return



notdone = True
while(notdone):
    notdone = False
    counter = 0
    for proposer in man:
        #print("checking ", proposer) 
        if man[proposer] == "":
            notdone = True
        else: 
            counter += 1
            #print("updating counter to ", counter)
            #print("counter is ", counter)
            continue
        if counter == len(man):
            #print("everyone has a match")
            notdone = False
        else:
            if(len(preferences[proposer]) > 0):
                proposee = preferences[proposer].pop()[0]
                matchy(proposer, proposee)
            
    #print("done with round")




#print("\ndone with matching\n")
for key in man:
    print(f'{key} {man[key]}')

