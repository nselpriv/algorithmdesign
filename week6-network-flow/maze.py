from math import gcd
import sys
from collections import deque

class Edge:
    def __init__(self, from_, to, cap):
        self.from_ = from_
        self.to = to
        self.cap = cap
        self.flow = 0

class Graph:
    def __init__(self, n, source, sink):
        self.edges = []
        self.adj = [[] for _ in range(n)]
        self.level = [-1] * n
        self.ptr = [0] * n
        self.n = n
        self.source = source
        self.sink = sink

    def add_edge(self, from_, to, cap):
        self.edges.append(Edge(from_, to, cap))
        self.edges.append(Edge(to, from_, cap))

        self.adj[from_].append(len(self.edges) - 2)  
        self.adj[to].append(len(self.edges) - 1)     

    def bfs(self):
        for i in range(self.n):
            self.level[i] = -1
        self.level[self.source] = 0
        queue = deque([self.source])

        while queue:
            u = queue.popleft()

            for edge_index in self.adj[u]:
                edge = self.edges[edge_index]
                if self.level[edge.to] == -1 and edge.flow < edge.cap:
                    self.level[edge.to] = self.level[u] + 1
                    queue.append(edge.to)
                    if edge.to == self.sink:
                        return True
        return False

    def dfs(self, u, flow):
        if u == self.sink:
            return flow
        total_pushed = 0
        while self.ptr[u] < len(self.adj[u]):
            edge_index = self.adj[u][self.ptr[u]]
            edge = self.edges[edge_index]
            if self.level[edge.to] == self.level[u] + 1 and edge.flow < edge.cap:
                current_flow = min(flow, edge.cap - edge.flow)
                pushed = self.dfs(edge.to, current_flow)
                if pushed > 0:
                    edge.flow += pushed
                    self.edges[edge_index ^ 1].flow -= pushed  
                    total_pushed += pushed
                    flow -= pushed
                    if flow == 0:
                        break
            self.ptr[u] += 1
        return total_pushed

    def max_flow(self):
        total_flow = 0
        while self.bfs():
            for i in range(self.n):
                self.ptr[i] = 0
            while True:
                flow = self.dfs(self.source, float('Inf'))
                if flow == 0:
                    break
                total_flow += flow
        return total_flow

def main():
    input_data = []

    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as file:
            input_data = file.read().strip().split('\n')
    else:
        input_data = sys.stdin.read().strip().split('\n')

    n = int(input_data[0])
    rooms = [int(input_data[i + 1]) for i in range(n)]

    source = min(rooms)
    sink = max(rooms)

    room_to_idx = {room: idx for idx, room in enumerate(rooms)}
    graph = Graph(n, room_to_idx[source], room_to_idx[sink])

    for i in range(n):
        for j in range(i + 1, n):
            u, v = rooms[i], rooms[j]
            g = gcd(u, v)
            if g > 1:
                #print(f"Adding edge between {u} and {v} with capacity {g}")
                graph.add_edge(room_to_idx[u], room_to_idx[v], g)

    max_flow = graph.max_flow()

    #for edge in graph.edges:
    #    if edge.flow > 0:
    #        print(f"Flow from {rooms[edge.from_]} to {rooms[edge.to]}: {edge.flow}")
    #    if edge.cap > edge.flow:
    #        print(f"Residual capacity from {rooms[edge.from_]} to {rooms[edge.to]}: {edge.cap - edge.flow}")

    #print(f"Maximum flow: {max_flow}")
    print(max_flow)


main()
