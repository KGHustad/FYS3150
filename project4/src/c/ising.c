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
            E += A[i][j] * A[i][(j+1) % L];     /* vertical neighbour */
        }
    }
    lat_ptr->energy = -J*E;
}

void find_tot_magnetization(lattice *lat_ptr) {
    int L = lat_ptr->L;
    int8_t **spin = lat_ptr->spin;
    int i, j;
    long tot_magnetization = 0;
    for (i=0; i < L; i++) {
        for (j=0; j < L; j++) {
            tot_magnetization += spin[i][j];
        }
    }
    lat_ptr->tot_magnetization = tot_magnetization;
}

/* function to compute the change of energy, given that lat.data[i][j] is flipped */
int relative_change_of_energy(lattice* lat_ptr, int i, int j) {
    int L = lat_ptr->L;
    int8_t **A = lat_ptr->spin;

    int E_old_up, E_old_down, E_old_left, E_old_right, E_old;

    E_old_down =    A[i][j] * A[(i+1)%L][j];
    E_old_up =      A[i][j] * A[(L+i-1)%L][j];
    E_old_right =   A[i][j] * A[i][(j+1)%L];
    E_old_left =    A[i][j] * A[i][(L+j-1)%L];
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

void metropolis(lattice *lat_ptr, int sweeps, double J, double *energies,
                long *tot_magnetization, gsl_rng *r, double *dE_cache,
                long save_every_nth) {
    int L = lat_ptr->L;
    lattice lat = *lat_ptr;
    int8_t **spin = lat_ptr->spin;

    double ran;
    int relative_dE;
    long sweep, count, accepted_configurations=0;
    int i, j;
    long pos_1d;
    long L_sq = L*L;
    for (sweep=1; sweep <= sweeps; sweep++) {
        for (count=0; count < L*L; count++) {
            pos_1d = gsl_rng_uniform_int(r, L_sq);
            i = pos_1d / L;
            j = pos_1d % L;

            relative_dE = relative_change_of_energy(lat_ptr, i, j);
            double dE = dE_cache[relative_dE];
            ran = gsl_rng_uniform(r);

            if (dE > ran) {
                /* ACCEPT */
                spin[i][j] *= -1;
                lat.energy += 2*J*relative_dE;
                lat.tot_magnetization += 2*spin[i][j];
                accepted_configurations++;
            }
        }
        if ((sweep % save_every_nth) == 0) {
            energies[sweep/save_every_nth] = lat.energy;
            tot_magnetization[sweep/save_every_nth] = lat.tot_magnetization;
        }

    }
    lat.accepted_configurations = accepted_configurations;
    *lat_ptr = lat;
}

void solve(lattice *lat_ptr, int sweeps, double J, double T,
           double *energies, long *tot_magnetization, long save_every_nth,
           unsigned long seed) {
    double beta = 1 / (/*boltzmann**/T);

    /* allocate a buffer where the few possible values of dE can be
    precalculated and stored */
    double *dE_buf = malloc(sizeof(double)*(4*2 + 1));
    double *dE_cache = dE_buf + 4; /* allow for negative indexing */
    int i;
    for (i = -4; i <= 4; i++) {
        /* set to NaN so that the error will propagate if there is a bug */
        dE_cache[i] = NAN;
    }
    for (i = -4; i <= 4; i += 2) {
        dE_cache[i] = exp(-beta*2*i);
    }

    gsl_rng *r = initialize_rng(seed);
    metropolis(lat_ptr, sweeps, J, energies, tot_magnetization, r, dE_cache,
               save_every_nth);

    /* freeing */
    destroy_rng(r);
    free(dE_buf);
}

void python_interface(int8_t *spin_flat, int L, int sweeps, double J,
                      double T, double *energies,
                      long *tot_magnetization,
                      long *accepted_configurations_ptr, long save_every_nth, unsigned long seed) {
    /* set signal handler */
    signal(SIGINT, abort_execution);

    lattice lat = alloc_lattice(spin_flat, L);
    find_energy(&lat, J);
    find_tot_magnetization(&lat);

    solve(&lat, sweeps, J, T, energies, tot_magnetization, save_every_nth,
          seed);


    *energies = lat.energy;
    *tot_magnetization = lat.tot_magnetization;

    *accepted_configurations_ptr = lat.accepted_configurations;

    free_lattice(lat);
}
