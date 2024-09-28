import sys

input_data = sys.stdin.read().strip().split('\n')

# First line of input contains useful_items and scouts
a = input_data[0].split(" ")
lists = int(a)

lst = []

for i in range(lists):
    x = input_data[i+1].split("")
    