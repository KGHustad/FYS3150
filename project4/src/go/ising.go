package ising

import (
	"fmt"
	"math"
	"math/rand"
)

type Lattice struct {
	Spin [][]int8		// spin values (may be +1 or -1)
	L int 					// dimension of lattice
	Energy float64
	Tot_magnetization int64
	Accepted_configurations int64
}

func wraparound(i, offset, len int) int {
  return (len + (i + offset)) % len
}

func find_energy(lat_ptr *Lattice, J float64) {
	L := lat_ptr.L
	A := lat_ptr.Spin

	//var E float64 = 0
	var E int64 = 0


	for i := 0; i < L; i++ {
		for j := 0; j < L; j++ {
			E += int64(A[i][j] * A[(i+1) % L][j])    // horizontal neighbour
			E += int64(A[i][j] * A[i][(j+1) % L])    // vertical neighbour
		}
	}
	lat_ptr.Energy = -J*float64(E)
}

func find_tot_magnetization(lat_ptr *Lattice) {
	L := lat_ptr.L
	A := lat_ptr.Spin


	var tot_magnetization int64
	for i := 0; i < L; i++ {
			for j := 0; j < L; j++ {
					tot_magnetization += int64(A[i][j])
			}
	}
	lat_ptr.Tot_magnetization = tot_magnetization}

/* function to compute the change of energy, given that lat.data[i][j] is flipped */
func relative_change_of_energy(lat_ptr *Lattice, i int, j int) int {
	L := lat_ptr.L
	A := lat_ptr.Spin

	var E_old_up, E_old_down, E_old_left, E_old_right, E_old int8

	E_old_down =    A[i][j] * A[(i+1)%L][j]
	E_old_up =      A[i][j] * A[(L+i-1)%L][j]
	E_old_right =   A[i][j] * A[i][(j+1)%L]
	E_old_left =    A[i][j] * A[i][(L+j-1)%L]
	E_old = E_old_right + E_old_left + E_old_up + E_old_down

	/*
	the difference in energy is equal to
			dE = -J * (E_new - E_old)

	Since the change consists of flipping the sign of A[i][j],
			E_new = -E_old

	Implying
			dE = -J * (- 2 * E_old) = 2*J*E_old

	Since, only the relative value (scaled by a positive factor) is of
	importance, it is sufficient to return E_old
	*/
	return int(E_old)
}

func metropolis(lat_ptr *Lattice, sweeps int64, J float64, energies []float64,
	tot_magnetization []int64, r *rand.Rand, dE_cache []float64,
	save_every_nth int64) {
	L := lat_ptr.L
	lat := *lat_ptr
	spin := lat_ptr.Spin

	var ran float64
	var relative_dE int
	var accepted_configurations int64
	var pos_1d int64
	var sweep int64
	var L_sq int64 = int64(L*L)
	for sweep = 1; sweep <= sweeps; sweep++ {
		for count := 0; count < L*L; count++ {
			pos_1d = r.Int63n(L_sq)
			i := int(pos_1d / int64(L))
			j := int(pos_1d % int64(L))

			relative_dE = relative_change_of_energy(lat_ptr, i, j)
			dE := dE_cache[4+relative_dE]
			ran = r.Float64()

			if dE > ran {
				/* ACCEPT */
				spin[i][j] *= -1
				lat.Energy += 2*J*float64(relative_dE)
				lat.Tot_magnetization += int64(2*spin[i][j])
				accepted_configurations++
			}
		}
		if (sweep % save_every_nth) == 0 {
			energies[sweep/save_every_nth] = lat.Energy
			tot_magnetization[sweep/save_every_nth] = lat.Tot_magnetization
		}
	}
	lat.Accepted_configurations = accepted_configurations
	*lat_ptr = lat
}

func Solve(lat_ptr *Lattice, sweeps int64, J float64, T float64,
	energies []float64, tot_magnetization []int64, save_every_nth int64,
 	seed int64) {
	var beta float64 = 1 / T

	find_energy(lat_ptr, J)
	find_tot_magnetization(lat_ptr)

	dE_cache := make([]float64, 9)
	for i := 0; i <= 8; i += 2 {
		dE_cache[i] = math.Exp(-beta*float64(2*(i-4)))
	}

	// create new Rand
	var r = rand.New(rand.NewSource(seed))

	metropolis(lat_ptr, sweeps, J, energies, tot_magnetization, r, dE_cache,
				save_every_nth)
}

func Init_lattice(lat_ptr *Lattice, L int) {
}

func main() {
  fmt.Println("Test")
}
