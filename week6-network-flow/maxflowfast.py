import sys
from collections import deque

class Edge: 
    def __init__(self, cap, usage, to, from_, direction):
        self.cap: int = cap
        self.usage: int = usage
        self.to: int = to
        self.from_: int = from_  
        self.direction: bool = direction

    def __repr__(self):
        return f'Edge(capacity={self.cap}, usage={self.usage}, to={self.to})'

class Vertex: 
    def __init__(self, id):
        self.id: int = id
        self.edges: list[Edge] = []
        self.sink = False
        self.source = False

    def set_sink(self, sink: bool):
        self.sink = sink

    def set_source(self, source: bool):
        self.source = source
    
    def add_edge(self, edge: Edge):
        self.edges.append(edge)

def bfs(graph: list[Vertex], source: int, sink: int, parent: dict[int, Edge]) -> bool:
    visited = set()
    queue = deque([source])
    visited.add(source)

    while queue:
        u = queue.popleft()
        for e in graph[u].edges:
            residual_capacity = e.cap - e.usage
            if residual_capacity > 0 and e.to not in visited:
                visited.add(e.to)
                parent[e.to] = e  # Keep track of the path
                if e.to == sink:
                    return True
                queue.append(e.to)

    return False

def edmonds_karp(graph: list[Vertex], source: int, sink: int) -> int:
    max_flow = 0
    parent = {}

    while bfs(graph, source, sink, parent):
        flow = float('Inf')
        s = sink

        # Find the maximum flow through the path found by BFS
        while s != source:
            e = parent[s]
            flow = min(flow, e.cap - e.usage)
            s = e.from_

        # update residual capacities of the edges and reverse edges along the path
        v = sink
        while v != source:
            e = parent[v]
            e.usage += flow
            # Check for reverse edge
            reverse_edge = next((re for re in graph[e.to].edges if re.to == e.from_), None)
            if reverse_edge is None:
                # Create reverse edge if it doesn't exist
                graph[e.to].add_edge(Edge(cap=0, usage=-flow, to=e.from_, from_=e.to, direction=True))
            else:
                reverse_edge.usage -= flow
            v = e.from_

        max_flow += flow

    return max_flow, graph

if len(sys.argv) > 1:
    with open(sys.argv[1], 'r') as file:
        input_data = file.read().strip().split('\n')
else:
    input_data = sys.stdin.read().strip().split('\n')

n, m, s, t = map(int, input_data[0].split())
graph: list[Vertex] = [Vertex(i) for i in range(n)]
graph[s].set_source(True)
graph[t].set_sink(True)

for i in range(m):
    u, v, x = map(int, input_data[i + 1].split())
    graph[u].add_edge(Edge(x, 0, v, u, False))  # Original edge
    graph[v].add_edge(Edge(0, 0, u, v, True))   # Reverse edge

max_flow, graph = edmonds_karp(graph, s, t)
used = 0 

if max_flow != 0:
    out = ""
    for e in graph:
        for ee in e.edges:
            if ee.usage > 0 and not ee.direction:  # Only output forward edges with flow
                out += f'{e.id} {ee.to} {ee.usage}\n'
                used += 1
    out = out[:-1]  # Remove the trailing newline

print(f'{n} {max_flow} {used}')

if max_flow != 0:
    print(out)
