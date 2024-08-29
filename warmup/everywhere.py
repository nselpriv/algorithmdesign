import sys
 
output = []
count = 0
input_data = sys.stdin.read().strip().split('\n')

trips = int(input_data[count])

for i in range(trips):
    count += 1
    cities = int(input_data[count])
    cur_cities = set()
    for x in range(cities):
        count += 1
        city = input_data[count]
        cur_cities.add(city)
    output.append(len(cur_cities))
      

for i in output:
    print(i)