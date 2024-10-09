import sys
from collections import deque

class Edge:
    def __init__(self, cap, usage, to):
        self.cap: int = cap
        self.usage: int = usage
        self.to: int = to

class Vertex:
    def __init__(self, id):
        self.id: int = id
        self.edges: list[Edge] = []
    
    def add_edge(self, edge: Edge):
        self.edges.append(edge)

def bfs(graph: list[Vertex], source: int, sink: int, parent: list[int]) -> bool:
    """Breadth-first search to find an augmenting path from the source to the sink."""
    visited = set()
    queue = deque([source])
    visited.add(source)

    while queue:
        print("test")
        u = queue.popleft()

        for i, e in enumerate(graph[u].edges):
            residual_capacity = e.cap - e.usage
            if residual_capacity > 0 and e.to not in visited:
                visited.add(e.to)
                parent[e.to] = (u, i)  # Store the parent vertex and the edge index
                if e.to == sink:
                    return True
                queue.append(e.to)
    return False

def ford_fulkerson(graph: list[Vertex], source: int, sink: int) -> int:
    """Implementation of Ford-Fulkerson to find maximum flow."""
    max_flow = 0

    while True:
        print("yes")
        parent = [None] * len(graph)  # Reset parent for the next BFS
        
        if not bfs(graph, source, sink, parent):
            break  # No more augmenting paths

        # Find the maximum flow through the path found.
        flow = float('Inf')
        s = sink
        
        while s != source:
            print
            u, idx = parent[s]
            flow = min(flow, graph[u].edges[idx].cap - graph[u].edges[idx].usage)
            s = graph[u].edges[idx].to
        
        # Update residual capacities of the edges and reverse edges along the path
        v = sink
        while v != source:
            u, idx = parent[v]
            graph[u].edges[idx].usage += flow  # Forward edge
            
            # Update reverse edge
            reverse_edge_idx = next(
                (i for i, rev_edge in enumerate(graph[v].edges) if rev_edge.to == u), None
            )
            if reverse_edge_idx is not None:
                graph[v].edges[reverse_edge_idx].usage -= flow
            else:
                # If reverse edge doesn't exist, create it
                graph[v].add_edge(Edge(0, 0, u))  # Create reverse edge with 0 capacity initially
            
            v = u
        
        max_flow += flow

    return max_flow

# Reading input
if len(sys.argv) > 1:
    with open(sys.argv[1], 'r') as file:
        input_data = file.read().strip().split('\n')
else:
    input_data = sys.stdin.read().strip().split('\n')

n, m, s, t = map(int, input_data[0].split())
graph: list[Vertex] = [Vertex(i) for i in range(n)]

for i in range(m):
    u, v, x = map(int, input_data[i + 1].split())
    graph[u].add_edge(Edge(x, 0, v))  # Forward edge
    graph[v].add_edge(Edge(0, 0, u))  # Reverse edge with 0 capacity

max_flow = ford_fulkerson(graph, s, t)
used_edges = 0 
out = []

for e in graph:
    for ee in e.edges:
        if ee.usage > 0:  # Only output edges with flow
            out.append(f'{e.id} {ee.to} {ee.usage}')

# Output results
print(f'{n} {max_flow} {len(out)}')
if len(out) > 0:
    print('\n'.join(out))
