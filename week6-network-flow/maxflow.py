import sys

class Edge: 
    def __init__(self, cap, usage, to, from_, direction):
        self.cap: int = cap
        self.usage: int = usage
        self.to: int = to
        self.from_: int = from_  # Added from_ to keep track of the originating vertex
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

    def __repr__(self):
        edges_repr = "\n "
        edges_repr += "\n ".join(str(edge) for edge in self.edges)
        return f'Vertex(id={self.id}, source={self.source}, sink={self.sink}, edges=[{edges_repr}])'

def findpath(graph: list[Vertex], u: int, visited: set[int], path: list[Edge], t: int) -> bool:
    """DFS to find an augmenting path from the source to the sink."""
    if u == t:
        return True
    visited.add(u)
    for e in graph[u].edges:
        residual_capacity = e.cap - e.usage
        if residual_capacity > 0 and e.to not in visited:
            path.append(e)
            if findpath(graph, e.to, visited, path, t):
                return True
            path.pop() 
    return False

def ford_fulkerson(graph: list[Vertex], source: int, sink: int) -> int:
    """Implementation of Ford-Fulkerson to find maximum flow."""
    max_flow = 0
    
    while True:
        path = []
        visited = set()
        if not findpath(graph, source, visited, path, sink):
            break
        
        flow = min(e.cap - e.usage for e in path)
        for e in path:
            e.usage += flow
            
            # Check for reverse edge
            reverse_edge = next((re for re in graph[e.to].edges if re.to == e.from_), None)
            if reverse_edge is None:
                # Create reverse edge if it doesn't exist
                graph[e.to].add_edge(Edge(cap=0, usage=-flow, to=e.from_, from_=e.to, direction=True)) 
            else:
                reverse_edge.usage -= flow
        
        max_flow += flow

    return max_flow, graph

if len(sys.argv) > 1:
    with open(sys.argv[1], 'r') as file:
        input_data = file.read().strip().split('\n')
else:
    input_data = sys.stdin.read().strip().split('\n')

n, m, s, t = map(int, input_data[0].split())
'''
n = vertices
m = edges
s = source
t = sink
'''
graph: list[Vertex] = [Vertex(i) for i in range(n)]
graph[s].set_source(True)
graph[t].set_sink(True)

for i in range(m):
    u, v, x = map(int, input_data[i + 1].split())
    graph[u].add_edge(Edge(x, 0, v, u, False))
    graph[v].add_edge(Edge(0, 0, u, v, True)) 

max_flow, graph = ford_fulkerson(graph, s, t)
used = 0 

if max_flow != 0:
    out = ""
    for e in graph:
        for ee in e.edges:
            if ee.usage != 0 and not ee.direction:
                out += f'{e.id} {ee.to} {ee.usage}\n'
                used += 1
    out = out[:-1]  # Remove the trailing newline

print(f'{n} {max_flow} {used}')

if max_flow != 0:
    print(out)
