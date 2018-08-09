#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <time.h>

#include "ising.h"

int main(int argc, char *argv[]) {
    struct timespec start, end;
    printf("bench_ising\n");

    double J = 1;
    double T = 2.27;

    int L = 100;
    int sweeps = 10000;

    clock_gettime(CLOCK_MONOTONIC_RAW, &start);
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

    clock_gettime(CLOCK_MONOTONIC_RAW, &end);
    double time_spent = end.tv_sec - start.tv_sec + 1E-9 * (end.tv_nsec - start.tv_nsec);
    printf("Finished in %g seconds\n", time_spent);

    return 0;
}
