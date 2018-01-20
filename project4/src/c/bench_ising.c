#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "ising.h"

int main(int argc, char *argv[]) {
    printf("bench_ising\n");

    double J = 1;
    double T = 2.27;

    int L = 100;
    int sweeps = 10000;

    int8_t *spin_flat = malloc(L*L*sizeof(int8_t));
    memset(spin_flat, 1, L*L);
    double *energies = malloc(sizeof(double)*(sweeps+1));
    long *tot_magnetization = malloc(sizeof(long)*(sweeps+1));
    long accepted_configurations;
    long save_every_nth = 1;
    unsigned long seed = 0;

    python_interface(spin_flat, L, sweeps, J, T, energies, tot_magnetization,
                     &accepted_configurations, save_every_nth, seed);

    free(spin_flat);
    free(energies);
    free(tot_magnetization);

    return 0;
}
