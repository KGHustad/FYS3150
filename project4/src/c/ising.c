#include <stdlib.h>
#include <stdint.h>
#include <math.h>
#include <signal.h>

#include <gsl/gsl_const_mksa.h>

#include "ising.h"
#include "random.h"

const double boltzmann = GSL_CONST_MKSA_BOLTZMANN;

void abort_execution(int sig) {
    fprintf(stderr, "Aborted execution\n");
    exit(EXIT_SUCCESS);
}

inline int wraparound(int i, int offset, int len) {
    return (len + (i + offset)) % len;
}

void find_energy(lattice *lat_ptr, double J) {
    int L = lat_ptr->L;
    int8_t **A = lat_ptr->spin;

    double E = 0;

    int i, j;
    for (i = 0; i < L; i++) {
        for (j = 0; j < L; j++) {
            E += A[i][j] * A[(i+1) % L][j];     /* horizontal neighbour */
            E += A[i][j] * A[i][(j-1) % L];     /* vertical neighbour */
        }
    }
    lat_ptr->energy = -J*E;
}

void find_mean_magnetization(lattice *lat_ptr) {
    int L = lat_ptr->L;
    int8_t **spin = lat_ptr->spin;
    int i, j;
    long mean_magnetization = 0;
    for (i=0; i < L; i++) {
        for (j=0; j < L; j++) {
            mean_magnetization += spin[i][j];
        }
    }
    lat_ptr->mean_magnetization = mean_magnetization;
}

/* function to compute the change of energy, given that lat.data[i][j] is flipped */
int relative_change_of_energy(lattice* lat_ptr, int i, int j) {
    int L = lat_ptr->L;
    int8_t **A = lat_ptr->spin;

    int E_old_up, E_old_down, E_old_left, E_old_right, E_old;

    E_old_right =   A[i][j] * A[(i+1)%L][j];
    E_old_left =    A[i][j] * A[(L+i-1)%L][j];
    E_old_up =      A[i][j] * A[i][(j+1)%L];
    E_old_down =    A[i][j] * A[i][(L+j-1)%L];
    E_old = E_old_right + E_old_left + E_old_up + E_old_down;

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
    return E_old;
}

void metropolis(lattice *lat_ptr, int mc_cycles, gsl_rng *r,
                double *dE_cache) {
    int L = lat_ptr->L;
    lattice lat = *lat_ptr;
    int8_t **spin = lat_ptr->spin;

    double ran;
    int relative_dE;
    int mc_cycle, accepted_configurations=0;
    int i, j;
    for (mc_cycle=0; mc_cycle < mc_cycles; mc_cycle++) {
        i = gsl_rng_uniform_int(r, L);
        j = gsl_rng_uniform_int(r, L);

        relative_dE = relative_change_of_energy(lat_ptr, i, j);
        double dE = dE_cache[relative_dE];
        ran = gsl_rng_uniform(r);
        /*printf("random: %g\n", ran);*/
        if (dE < ran) {
            /* ACCEPT */
            spin[i][j] *= -1;
            lat.energy += relative_dE;
            lat.mean_magnetization += 2*spin[i][j];
            accepted_configurations++;
        }
    }
    lat.accepted_configurations = accepted_configurations;
    *lat_ptr = lat;
}

void solve(lattice *lat_ptr, int mc_cycles, double T) {
    double beta = 1 / (/*boltzmann**/T);

    /* allocate a buffer where the few possible values of dE can be
    precalculated and stored */
    double *dE_buf = malloc(sizeof(double)*17);
    double *dE_cache = dE_buf + 8; /* allow for negative indexing */
    int i;
    for (i = -8; i <= 8; i++) {
        /* set to NaN so that the error will propagate if there is a bug */
        dE_cache[i] = NAN;
    }
    for (i = -8; i <= 8; i += 4) {
        dE_cache[i] = exp(-beta*i);
    }

    gsl_rng *r = initialize_rng();
    metropolis(lat_ptr, mc_cycles, r, dE_cache);

    /* freeing */
    destroy_rng(r);
    free(dE_buf);
}

void python_interface(int8_t *spin_flat, int L, int mc_cycles, double J,
                      double T, double *energy_ptr,
                      long *mean_magnetization_ptr,
                      long *accepted_configurations_ptr) {
    /* set signal handler */
    signal(SIGINT, abort_execution);

    lattice lat = alloc_lattice(spin_flat, L);
    find_energy(&lat, J);
    find_mean_magnetization(&lat);

    solve(&lat, mc_cycles, T);

    *energy_ptr = lat.energy;
    *mean_magnetization_ptr = lat.mean_magnetization;
    *accepted_configurations_ptr = lat.accepted_configurations;

    free_lattice(lat);
}
