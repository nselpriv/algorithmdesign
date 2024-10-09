package main

import (
	"bufio"
	"fmt"
	"os"
)

type Edge struct {
	from, to, cap, flow int
}

type Graph struct {
	edges   []Edge
	adj     [][]int
	level   []int
	ptr     []int
	n, source, sink int
}

func NewGraph(n, source, sink int) *Graph {
	return &Graph{
		edges:   make([]Edge, 0),
		adj:     make([][]int, n),
		level:   make([]int, n),
		ptr:     make([]int, n),
		n:       n,
		source:  source,
		sink:    sink,
	}
}

func (g *Graph) AddEdge(from, to, cap int) {
	g.edges = append(g.edges, Edge{from, to, cap, 0})
	g.edges = append(g.edges, Edge{to, from, 0, 0}) // Reverse edge
	g.adj[from] = append(g.adj[from], len(g.edges)-2) // Forward edge index
	g.adj[to] = append(g.adj[to], len(g.edges)-1)     // Reverse edge index
}

func (g *Graph) BFS() bool {
	for i := range g.level {
		g.level[i] = -1
	}
	g.level[g.source] = 0
	queue := []int{g.source}

	for len(queue) > 0 {
		u := queue[0]
		queue = queue[1:]

		for _, edgeIndex := range g.adj[u] {
			edge := &g.edges[edgeIndex]
			if g.level[edge.to] == -1 && edge.flow < edge.cap {
				g.level[edge.to] = g.level[u] + 1
				queue = append(queue, edge.to)
				if edge.to == g.sink {
					return true
				}
			}
		}
	}
	return false
}

func (g *Graph) DFS(u, flow int) int {
	if u == g.sink {
		return flow
	}
	for g.ptr[u] < len(g.adj[u]) {
		edgeIndex := g.adj[u][g.ptr[u]]
		edge := &g.edges[edgeIndex]
		if g.level[edge.to] == g.level[u]+1 && edge.flow < edge.cap {
			currentFlow := min(flow, edge.cap-edge.flow)
			if pushed := g.DFS(edge.to, currentFlow); pushed > 0 {
				edge.flow += pushed
				g.edges[edgeIndex^1].flow -= pushed // Update reverse edge
				return pushed
			}
		}
		g.ptr[u]++
	}
	return 0
}

func (g *Graph) MaxFlow() (int, int) {
	totalFlow := 0

	for g.BFS() {
		for i := range g.ptr {
			g.ptr[i] = 0
		}
		for {
			flow := g.DFS(g.source, 1<<30) // Some large number
			if flow == 0 {
				break
			}
			totalFlow += flow
		}
	}
	return totalFlow, g.getUsedEdges()
}

func (g *Graph) getUsedEdges() int {
	used := 0
	for _, edge := range g.edges {
		if edge.flow > 0 && edge.from != edge.to {
			used++
		}
	}
	return used
}

func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}

func main() {
	var n, m, s, t int
	var inputData []string

	if len(os.Args) > 1 {
		file, err := os.Open(os.Args[1])
		if err != nil {
			fmt.Println(err)
			return
		}
		defer file.Close()
		scanner := bufio.NewScanner(file)
		for scanner.Scan() {
			inputData = append(inputData, scanner.Text())
		}
	} else {
		scanner := bufio.NewScanner(os.Stdin)
		for scanner.Scan() {
			inputData = append(inputData, scanner.Text())
		}
	}

	fmt.Sscanf(inputData[0], "%d %d %d %d", &n, &m, &s, &t)

	graph := NewGraph(n, s, t)

	for i := 1; i <= m; i++ {
		var u, v, x int
		fmt.Sscanf(inputData[i], "%d %d %d", &u, &v, &x)
		graph.AddEdge(u, v, x)
	}

	maxFlow, usedEdges := graph.MaxFlow()
	out := ""

	if maxFlow != 0 {
		for _, edge := range graph.edges {
			if edge.flow > 0 && edge.from != edge.to {
				out += fmt.Sprintf("%d %d %d\n", edge.from, edge.to, edge.flow)
			}
		}
		out = out[:len(out)-1] // Remove the trailing newline

		fmt.Printf("%d %d %d\n", n, maxFlow, usedEdges)
		fmt.Print(out)
	} else {
		fmt.Printf("%d %d %d\n", n, maxFlow, usedEdges)
	}
}
