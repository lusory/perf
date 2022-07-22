package main

import (
	"fmt"
	"math/rand"
	"time"
)

const n = 2048

func main() {
	a := make([][]float32, n)
	for i := range a {
		a[i] = make([]float32, n)
	}
	b := make([][]float32, n)
	for i := range b {
		b[i] = make([]float32, n)
	}
	c := make([][]float32, n)
	for i := range c {
		c[i] = make([]float32, n)
	}

	for i := 0; i < n; i++ {
		rand.Seed(time.Now().UnixNano())

		for j := 0; j < n; j++ {
			a[i][j] = rand.Float32()
			b[i][j] = rand.Float32()
		}
	}

	st := time.Now()

	for i := 0; i < n; i++ {
		for j := 0; j < n; j++ {
			for k := 0; k < n; k++ {
				c[i][j] += a[i][k] * b[j][k]
			}
		}
	}

	fmt.Println(time.Since(st).Seconds())
}
