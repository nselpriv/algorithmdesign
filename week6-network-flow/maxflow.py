import sys

class edge: 
    def __init__(self, cap, usage, to, direction):
        self.cap: int = cap
        self.usage: int = usage
        self.to: int = to
        self.direction: bool = direction
    def __repr__(self):
        return f'Edge(capacity={self.cap}, usage={self.usage}, to={self.to})'
        
class vertex: 
    def __init__(self, id):
        self.id: int = id
        self.edges: list[edge] = []
        self.sink = False
        self.source = False

    def set_sink(self, sink: bool):
        self.sink = sink

    def set_source(self, source: bool):
        self.source = source
    
    def add_edge(self, edge: edge):
        self.edges.append(edge)

    def __repr__(self):
        edges_repr = "\n"
        edges_repr += "\n ".join(str(edge) for edge in self.edges)
        return f'Vertex(id={self.id}, source={self.source}, sink={self.sink}, edges=[{edges_repr}])'

def findpath(graph: list[vertex], u: int, visited: set[int], path: list[edge], t: int) -> bool:
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

def ford_fulkerson(graph: list[vertex], source: int, sink: int) -> int:
    """Implementation of Ford-Fulkerson to find maximum flow."""
    max_flow = 0
    path = []
    
    while findpath(graph, source, set(), path, sink):
        flow = min(e.cap - e.usage for e in path)
        for e in path:
            e.usage += flow
            reverse_edge = next((re for re in graph[e.to].edges if re.to == graph[e.to].id and re.usage < 0), None)
            if reverse_edge is None:
                graph[e.to].add_edge(edge(cap=0, usage=-flow, to=e.to, direction=True)) 
            else:
                reverse_edge.usage -= flow
        max_flow += flow
        path.clear()  

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
graph: list[vertex] = [vertex(i) for i in range(n)]
graph[s].set_source(True)
graph[t].set_sink(True)

for i in range(m):
    u, v, x = map(int, input_data[i + 1].split())
    graph[u].add_edge(edge(x, 0, v, False))
    graph[v].add_edge(edge(0, 0, u, True)) 

max_flow,graph = ford_fulkerson(graph, s, t)
used = 0 

if(max_flow!=0):
    out = ""
    for e in graph:
        for ee in e.edges:
            if(ee.usage != 0 and not ee.direction):
                out += f'{e.id} {ee.to} {ee.usage}\n'
                used +=1
    out = out[:-1]

print(f'{n} {max_flow} {used}')

if(max_flow!=0):
    print(out)
