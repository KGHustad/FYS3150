#ifndef __ISING_H
#define __ISING_H

#include <stdint.h>

#include "lattice.h"
#include "random.h"


void find_energy(lattice *lat_ptr, double J);
int relative_change_of_energy(lattice *lat_ptr, int i, int j);
void metropolis(lattice *lat_ptr, int sweeps, double J, double *energies,
                long *tot_magnetization, gsl_rng *r, double *dE_cache,
                long save_every_nth);
void solve(lattice *lat_ptr, int sweeps, double J, double T,
           double *energies, long *tot_magnetization, long save_every_nth,
           unsigned long seed);
void python_interface(int8_t *spin_flat, int L, int sweeps, double J,
                      double T, double *energies,
                      long *tot_magnetization,
                      long *accepted_configurations_ptr, long save_every_nth, unsigned long seed);
#endif
