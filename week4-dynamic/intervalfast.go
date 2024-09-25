package main

import (
    "bufio"
    "fmt"
    "os"
    "sort"
)

type Interval struct {
    Start  int
    End    int
    Weight int
}

func readInput() ([]Interval, int) {
    var n int
    var intervals []Interval

    scanner := bufio.NewScanner(os.Stdin)
    if scanner.Scan() {
        fmt.Sscan(scanner.Text(), &n)
    }

    for i := 0; i < n; i++ {
        var s, f, w int
        if scanner.Scan() {
            fmt.Sscan(scanner.Text(), &s, &f, &w)
            intervals = append(intervals, Interval{Start: s, End: f, Weight: w})
        }
    }

    return intervals, n
}

func Pcal(intervals []Interval, currentStart int) int {
    low, high := 0, len(intervals)-1
    for low <= high {
        mid := (low + high) / 2
        if intervals[mid].End <= currentStart { 
            low = mid + 1
        } else {
            high = mid - 1
        }
    }
    return high 
}

func main() {
    intervals, n := readInput()

    sort.Slice(intervals, func(i, j int) bool {
        return intervals[i].End < intervals[j].End
    })

    M := make([]int, n+1)
    P := make([]int, n)

    for j := 0; j < n; j++ {
        P[j] = Pcal(intervals, intervals[j].Start)
    }

    for j := 1; j <= n; j++ {
        w := intervals[j-1].Weight
        previousIndex := 0
        if P[j-1] >= 0 {
            previousIndex = P[j-1] + 1
        }
        M[j] = max(w+M[previousIndex], M[j-1])
    }
    fmt.Println(M[n])
}

func max(a, b int) int {
    if a > b {
        return a
    }
    return b
}
