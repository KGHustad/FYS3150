#include <stdlib.h>
#include <stdint.h>
#include <math.h>
#include <signal.h>

#include <random>

typedef struct {
    int8_t **spin; /* spin values (may be +1 or -1) */
    int L; /* dimension of lattice */
    double energy;
    long tot_magnetization;
    long accepted_configurations;
} lattice;

lattice alloc_lattice(int8_t *spin_flat, int L) {
    int i;
    int8_t **spin = (int8_t**) malloc(sizeof(int8_t*)*L);
    for (i = 0; i < L; i++) {
        spin[i] = spin_flat + L*i;
    }

    lattice lat;
    lat.L = L;
    lat.spin = spin;
    lat.accepted_configurations = 0;
    return lat;
}

void free_lattice(lattice lat) {
    free(lat.spin);
}

unsigned long get_unix_seed(void) {
    FILE *file = fopen("/dev/urandom", "r");
    unsigned long seed;
    int items_read = 0;
    items_read = fread(&seed, sizeof(unsigned long), 1, file);
    if (items_read != 1) {
        fprintf(stderr, "ERROR: Could not retrieve unix seed\n");
        exit(EXIT_FAILURE);
    }
    fclose(file);
    /*printf("seed: %lu\n", seed);*/
    return seed;
}

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
                long *tot_magnetization, double *dE_cache,
                long save_every_nth,
#ifdef USE_GSL
                gsl_rng *r
#else
                std::mt19937_64 &rng,
                std::uniform_int_distribution<long> pos_dist,
                std::uniform_real_distribution<double> flip_dist
#endif
            ) {
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
#ifdef USE_GSL
            pos_1d = gsl_rng_uniform_int(r, L_sq);
#else
            pos_1d = pos_dist(rng);
#endif
            i = pos_1d / L;
            j = pos_1d % L;

            relative_dE = relative_change_of_energy(lat_ptr, i, j);
            double dE = dE_cache[relative_dE];
#ifdef USE_GSL
            ran = gsl_rng_uniform(r);
#else
            ran = flip_dist(rng);
#endif

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
    double *dE_buf = (double*) malloc(sizeof(double)*(4*2 + 1));
    double *dE_cache = dE_buf + 4; /* allow for negative indexing */
    int i;
    for (i = -4; i <= 4; i++) {
        /* set to NaN so that the error will propagate if there is a bug */
        dE_cache[i] = NAN;
    }
    for (i = -4; i <= 4; i += 2) {
        dE_cache[i] = exp(-beta*2*i);
    }

#ifdef USE_GSL
    gsl_rng *r = initialize_rng(seed);
#else
    int L = lat_ptr->L;
    std::mt19937_64 rng;
    rng.seed(get_unix_seed());
    std::uniform_int_distribution<long> pos_dist(0, L*L - 1);
    std::uniform_real_distribution<double> flip_dist(0, 1);
#endif
    metropolis(lat_ptr, sweeps, J, energies, tot_magnetization, dE_cache,
               save_every_nth,
#ifdef USE_GSL
               r
#else
               rng,
               pos_dist,
               flip_dist
#endif
          );

    /* freeing */
#ifdef USE_GSL
    destroy_rng(r);
#else

#endif
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
