import sys
import statistics
 
input_data = sys.stdin.read().strip().split('\n')


first_line = input_data[0].strip().split()
N = int(first_line[0])
t = int(first_line[1])

second_line = input_data[1].strip().split()
A = list(map(int, second_line))

def number_to_string(argument):
    match argument:
        case 1:
            return print(7)
        case 2:
            return handle_two()
        case 3:
            return print(statistics.median([A[0], A[1], A[2]]))
        case 4:
            return handle_four(False)
        case 5:
            return handle_four(True)
        case 6:
            return handle_six()
        case 7:
            return handle_seven(0)
        case default:
            return "oh no something i didnt expect happened"
        
def handle_two():
    if A[0] > A[1]:
        return print("Bigger")
    elif A[0] == A[1]:
        return print("Equal")
    else:
        return print("Smaller")
    
def handle_four(iseven):
    res = 0
    if (iseven):
        for i in A:
            if(i % 2 == 0):
                res += i
    else: 
        for i in A:
            res += i
    print(res)

def handle_six():
    mappings = {
        1: "a",
        2: "b",
        3: "c",
        4: "d",
        5: "e",
        6: "f",
        7: "g",
        8: "h",
        9: "i",
        10: "j",
        11: "k",
        12: "l",
        13: "m",
        14: "n",
        15: "o",
        16: "p",
        17: "q",
        18: "r",
        19: "s",
        20: "t",
        21: "u",
        22: "v",
        23: "w",
        24: "x",
        25: "y",
        26: "z"
    }
    res = ""
    for i in A:
        i += 1 # i ruined the mapping >:(
        res += mappings[i % 26]
    print(res)

def handle_seven(i, index = 0):
    counter = i
    #if index out of bounds then return stop
    temp = A[counter]
    if(temp == "OH NO"):
        return print("Cyclic")
    if index == 0: 
        A[0] = "OH NO"
    if temp >= len(A):
        return print("Out")
    if(temp == N-1):
        return print("Done")
    index += 1
    handle_seven(temp, index)

number_to_string(t)

