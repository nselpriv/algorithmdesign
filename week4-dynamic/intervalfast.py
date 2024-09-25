import sys
from bisect import bisect_right


if len(sys.argv) > 1:
    # running the debugger
    with open(sys.argv[1], 'r') as file:
        input_data = file.read().strip().split('\n')
else:
    input_data = sys.stdin.read().strip().split('\n')

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
P = [0 for _ in range(n)]

for i in range(n):
    s,f,w = input_data[i+1].split(" ")
    intervals.append(Interval(int(s),int(f),int(w)))

intervals.sort(key=lambda x: x.end)

for j in range(n):
    P[j] = bisect_right(
        [interval.end for interval in intervals],
          intervals[j].start) - 1

for j in range(1, n + 1):
    M[j] = max(intervals[j-1].weight + M[P[j-1]+1], M[j - 1])

print(M[n])