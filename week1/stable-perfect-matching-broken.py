import sys
 
output = []
count = 0
input_data = sys.stdin.read().strip().split('\n')

n, m = input_data[0].split(" ")

#n = number of lines
#m = uhhhhh
preferences = dict()  # name of person that likes and a stack of preferences
matchings = dict() # current matchings

matchstack = len(input_data[1].split(" "))-1
for i in range(int(n)):
    check = i<int(int(n)/2)
    current = input_data[i+1].split(" ")
    name = current.pop(0)
    matchstack = len(current)
    

    #print(f'we got {name} {i} {check}')
    tempref = []
    if check:
        matchings[name] = "" #this will be a proposer so we add it to outputs 
    
    current.reverse()  
    for j in range(0, matchstack): 
        #print(matchstack)
        #print(j)
        tempref.append(current[j])

    preferences[name] = tempref 
    #if(check):
       #print(f'we got {name} adding it to actual output')

#print("\n setup done \n")

#for key in preferences: 
   # print(f'{key} {preferences[key].pop()}')

def actualmatch(key, match):
    if len(preferences[match]) == 0: 
        return
    if(preferences[match][0] != key):
        print(f'{match} thinks {key} is better than {preferences[match][0]}')
        removed = preferences[match].pop(0)
        print(f'deleting from stack {removed}')
        actualmatch(key, match)
    else:
        matchings[key] = match
        print(f'{key} is matched with {match}')



def match(key):
    print(f'{key} is not matched')
    match = preferences[key].pop()
    print(f'{key} is trying to match with {match}')
    if(len(preferences[match]) == 1) & (matchings[key] != ""):
        print(f'{match} is matched with {preferences[match][0]} their favorite, rejecting {key}')
        return
    else: 
        print(f'{match} wants to check for better match')
        actualmatch(key, match)
            

notdone = True
while(notdone):
    notdone = False
    counter = 0
    for key in matchings:
        print("checking ", key) 
        print(matchings[key])
        if matchings[key] == "":
            notdone = True
        else: 
            counter += 1
            print("updating counter to ", counter)
            print("counter is ", counter)
        if counter == len(matchings):
            print("everyone has a match")
            notdone = False
        else:
            print("matching...")
            if len(preferences[key]) == 0:
                print(f'{key} has no more matches')
                counter += 1
                continue
            else:
                match(key)
    print("done with round")

print("\ndone with matching\n")
for key in matchings:
    print(f'{key} {matchings[key]}')
