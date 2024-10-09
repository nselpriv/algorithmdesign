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
        self.edges.append(Edge(to, from_, 0))  # Reverse edge
        self.adj[from_].append(len(self.edges) - 2)  # Forward edge index
        self.adj[to].append(len(self.edges) - 1)      # Reverse edge index

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
        while self.ptr[u] < len(self.adj[u]):
            edge_index = self.adj[u][self.ptr[u]]
            edge = self.edges[edge_index]
            if self.level[edge.to] == self.level[u] + 1 and edge.flow < edge.cap:
                current_flow = min(flow, edge.cap - edge.flow)
                pushed = self.dfs(edge.to, current_flow)
                if pushed > 0:
                    edge.flow += pushed
                    self.edges[edge_index ^ 1].flow -= pushed  # Update reverse edge
                    return pushed
            self.ptr[u] += 1
        return 0

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

    n, m, s, t = map(int, input_data[0].split())
    graph = Graph(n, s, t)

    for i in range(1, m + 1):
        u, v, x = map(int, input_data[i].split())
        graph.add_edge(u, v, x)

    max_flow = graph.max_flow()
    used_edges = sum(1 for edge in graph.edges if edge.flow > 0 and edge.from_ != edge.to)

    out = ""
    for edge in graph.edges:
        if edge.flow > 0 and edge.from_ != edge.to:
            out += f"{edge.from_} {edge.to} {edge.flow}\n"
    out = out[:-1] if out else out  # Remove the trailing newline

    print(f"{n} {max_flow} {used_edges}")
    if max_flow != 0:
        print(out)

if __name__ == "__main__":
    main()
