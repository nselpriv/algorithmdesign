
import sys, math

input_data = sys.stdin.read().strip().split('\n')
n = int(input_data[0])

px = []
py = []

for i in range(n):
    x, y = input_data[i+1].split(" ")
    px.append((float(x),float(y)))
    py.append((float(x),float(y)))

px.sort(key=lambda x: x[0])    
py = sorted(px, key=lambda x: x[1])


def brute_force(px):
    minimum = float('inf')
    result = None
    for i in range(len(px)):
        for j in range(i+1, len(px)):
            dist = (px[i][0] - px[j][0]) ** 2 + (px[i][1] - px[j][1]) ** 2
            if dist < minimum:
                minimum = dist
                result = (px[i], px[j])
    return result, math.sqrt(minimum)

def split_list(a_list):
    half = len(a_list)//2
    return a_list[:half], a_list[half:]

def closest_pair(px, py):
    if len(px) <= 3:
        return brute_force(px)
    else:
        Qx, Rx = split_list(px)

        xmax = Qx[-1][0]

        Qy = [p for p in py if p[0] <= xmax]
        Ry = [p for p in py if p[0] > xmax]

        (q0, q1), dist_q = closest_pair(Qx, Qy)
        (r0, r1), dist_r = closest_pair(Rx, Ry)

        ss = min(dist_q, dist_r)
        Sy = [p for p in py if abs(p[0] - xmax) < ss]
        
        best_pair = (q0, q1) if dist_q < dist_r else (r0, r1)
        
        for i in range(len(Sy)):
            for j in range(i+1, min(i+7, len(Sy))):
                dist_sq = (Sy[i][0] - Sy[j][0]) ** 2 + (Sy[i][1] - Sy[j][1]) ** 2
                if dist_sq < ss ** 2:
                    ss = math.sqrt(dist_sq)
                    best_pair = (Sy[i], Sy[j])

        return best_pair, ss

res, _ = closest_pair(px, py)

print(f'{res[0][0]} {res[0][1]}\n{res[1][0]} {res[1][1]}')
