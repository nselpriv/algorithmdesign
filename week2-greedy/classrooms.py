import sys
 
output = 0
count = 0
input_data = sys.stdin.read().strip().split('\n')

activites, classrooms = input_data[0].split(" ")

activites = int(activites)
classrooms = int(classrooms)

#print(f'{activites} {classrooms}')

count +=1

acti = []

output = []

for i in range(activites):
    start, finish = input_data[i+1].split(" ")
    #print(f'{start} is start and {finish} is end')
    acti.append((int(start), int(finish)))


#print("\n sorting \n")
acti.sort(key=lambda x: x[0]) #sorting on start time

allocations = dict()

#create a dictory of classrooms that contain n lists depending on amount of classrooms
for i in range(classrooms):
    allocations[i] = (0,0,0) #start, end and total activites 



while(len(acti) > 0):
    activity = acti.pop(0)
    #print(f'{activity} is the current activity')
    #print(f'"trying to allocate {activity}')
    possibilites = []
    for room in allocations:
        #print(f'checking room {room}')
        if activity[0] > allocations[room][1]:
            #print(f'activity {activity} is allocated to room {room}')
            selection = (activity[0],activity[1],allocations[room][2], room, allocations[room][1])
            #start, end, counter, index
            possibilites.append(selection)
    if(len(possibilites) == 0):
       # print(f'no room available for {activity}')
        continue
    else:
        possibilites.sort(key=lambda x: x[4]) #sorting on start time
        curr = possibilites[0][2]
        next = curr + 1
        #print(f'activity {activity} is allocated to room {possibilites[0][3]}')
        allocations[possibilites[0][3]] = (0, activity[1],next)
    


amount = 0
for key in allocations:
    amount += allocations[key][2]
    


print(amount)

#print("\n output \n")
#print(len(output))
