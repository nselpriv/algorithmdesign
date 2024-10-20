from collections import deque
import sys

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
        found = False
        for idx in self.adj[from_]:
            edge = self.edges[idx]
            if edge.to == to:
                edge.cap += cap
                self.edges[idx ^ 1].cap += cap 
                found = True
                break

        if not found:
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
            self.ptr = [0] * self.n  
            while True:
                flow = self.dfs(self.source, float('Inf'))
                if flow == 0:
                    break
                total_flow += flow
        return total_flow

def main():
    input_data = sys.stdin.read().strip().split('\n')
    n, m, k = map(int, input_data[0].split())
    
    graph = Graph(n, 0, 1) 
    
    for i in range(1, m + 1):
        u, v, cap = map(int, input_data[i].split())
        graph.add_edge(u - 1, v - 1, cap)

    current_flow = graph.max_flow()
    print(current_flow)

    for i in range(m + 1, m + 1 + k):
        u, v, cap = map(int, input_data[i].split())
        graph.add_edge(u - 1, v - 1, cap)
        current_flow += graph.max_flow()
        print(current_flow)

main()