package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"sort"
	"strconv"
	"strings"
)

type Point struct {
	x, y float64
}

func Distance(p1, p2 Point) float64 {
	return math.Hypot(p1.x-p2.x, p1.y-p2.y)
}

func BruteForce(points []Point) (Point, Point, float64) {
	minDist := math.MaxFloat64
	var p1, p2 Point
	for i := 0; i < len(points); i++ {
		for j := i + 1; j < len(points); j++ {
			dist := Distance(points[i], points[j])
			if dist < minDist {
				minDist = dist
				p1 = points[i]
				p2 = points[j]
			}
		}
	}
	return p1, p2, minDist
}

func ClosestPair(px, py []Point) (Point, Point, float64) {
	if len(px) <= 3 {
		return BruteForce(px)
	}

	mid := len(px) / 2
	Qx := px[:mid]
	Rx := px[mid:]
	midX := Qx[len(Qx)-1].x

	Qy := []Point{}
	Ry := []Point{}
	for _, p := range py {
		if p.x <= midX {
			Qy = append(Qy, p)
		} else {
			Ry = append(Ry, p)
		}
	}

	p1, p2, distQ := ClosestPair(Qx, Qy)
	r1, r2, distR := ClosestPair(Rx, Ry)

	ss := math.Min(distQ, distR)
	bestPair := [2]Point{p1, p2}
	if distR < distQ {
		bestPair = [2]Point{r1, r2}
	}

	strip := []Point{}
	for _, p := range py {
		if math.Abs(p.x-midX) < ss {
			strip = append(strip, p)
		}
	}

	for i := 0; i < len(strip); i++ {
		for j := i + 1; j < len(strip) && strip[j].y-strip[i].y < ss; j++ {
			dist := Distance(strip[i], strip[j])
			if dist < ss {
				ss = dist
				bestPair = [2]Point{strip[i], strip[j]}
			}
		}
	}

	return bestPair[0], bestPair[1], ss
}

func ParseInput(scanner *bufio.Scanner) ([]Point, bool) {
	if !scanner.Scan() {
		return nil, false
	}

	n, _ := strconv.Atoi(scanner.Text())
	if n == 0 {
		return nil, false
	}

	points := make([]Point, n)
	for i := 0; i < n; i++ {
		if scanner.Scan() {
			line := scanner.Text()
			coords := strings.Fields(line)
			x, _ := strconv.ParseFloat(coords[0], 64)
			y, _ := strconv.ParseFloat(coords[1], 64)
			points[i] = Point{x, y}
		}
	}

	return points, true
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)

	for {
		points, more := ParseInput(scanner)
		if !more {
			break
		}

		px := make([]Point, len(points))
		py := make([]Point, len(points))
		copy(px, points)
		copy(py, points)

		sort.Slice(px, func(i, j int) bool { return px[i].x < px[j].x })
		sort.Slice(py, func(i, j int) bool { return py[i].y < py[j].y })

		p1, p2, _ := ClosestPair(px, py)

		fmt.Printf("%.2f %.2f %.2f %.2f\n", p1.x, p1.y, p2.x, p2.y)
	}
}
