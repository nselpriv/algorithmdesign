
import sys
from bisect import bisect_right


if len(sys.argv) > 1:
    # running the debugger
    with open(sys.argv[1], 'r') as file:
        input_data = file.read().strip().split('\n')
else:
    input_data = sys.stdin.read().strip().split('\n')

#input_data = ["6","0 3 1","1 5 1","3 7 1","2 10 1", "7 11 1", "8 12 1"]

'''
input structure
3 n -> amount of intervals
1 4 1 intervals s, f, w
2 8 3
5 9 1
s -> starting interval
f -> ending interval 
w -> weight of the interval

notes
No overlap if f1 == s2 
output the added sums of max weight

'''

class Interval: 
    def __init__(self, start,end,weight):
        self.start = start
        self.end = end
        self.weight = weight
    def __repr__(self):
        return f"Interval(start={self.start}, end={self.end}, weight={self.weight}"

intervals = []
n = int(input_data[0])
M = [0 for _ in range(n+1)]

for i in range(n):
    s,f,w = input_data[i+1].split(" ")
    intervals.append(Interval(int(s),int(f),int(w)))

intervals.sort(key=lambda x: x.end)

def p(current_index):
    current_start = intervals[current_index].start
    j = bisect_right([interval.end for interval in intervals], current_start) - 1
    return j 

for j in range(1, n + 1):
    M[j] = max(intervals[j-1].weight + M[p(j-1)+1], M[j - 1])

print(M[n])