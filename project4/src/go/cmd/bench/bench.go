package main

import (
	"flag"
	"fmt"
	"github.com/KGHustad/FYS3150/project4/src/go/ising"
	"log"
	"os"
	"runtime/pprof"
	"time"
)

var cpuprofile = flag.String("cpuprofile", "", "write cpu profile to file")

func main() {
	fmt.Println("Benchmarking go implementation")

	flag.Parse()
	if *cpuprofile != "" {
		f, err := os.Create(*cpuprofile)
		if err != nil {
			log.Fatal(err)
		}
		pprof.StartCPUProfile(f)
		defer pprof.StopCPUProfile()
	}

	start := time.Now()
	var J float64 = 1
	var T float64 = 2.27

	var L int = 100
	var sweeps int64 = 10000

	var spin [][]int8 = make([][]int8, L)
	for i := 0; i < L; i++ {
		spin[i] = make([]int8, L)
		for j := 0; j < L; j++ {
			spin[i][j] = 1
		}
	}
	energies := make([]float64, sweeps+1)
	tot_magnetization := make([]int64, sweeps+1)
	var save_every_nth int64 = 1
	var seed int64 = 0

	var lat ising.Lattice
	lat.Spin = spin
	lat.L = L

	ising.Solve(&lat, sweeps, J, T, energies, tot_magnetization, save_every_nth, seed)
	elapsed := time.Since(start)
	fmt.Println("Finished in ", elapsed)
	//fmt.Println(lat)
}
