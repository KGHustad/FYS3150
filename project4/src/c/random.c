#include <stdlib.h>
#include <stdio.h>
#include "random.h"

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

gsl_rng* initialize_rng(unsigned long seed) {
    const gsl_rng_type * T; /* specifies the type of random number generator */
    gsl_rng * r; /* pointer to random number generator */

    if (seed == 0) {
        seed = get_unix_seed();
    }

    /*gsl_rng_env_setup();*/

    T = gsl_rng_default;
    r = gsl_rng_alloc(T);
    gsl_rng_set(r, seed);
    return r;
}

void destroy_rng(gsl_rng *r) {
    gsl_rng_free(r);
}

inline int8_t rand_plus_minus(gsl_rng *r) {
    /*
    bitwise AND with 2 can yield 2 or 0, subtracting 1,
    the returned number is either -1 or 1
    */
    return ((int8_t) (gsl_rng_get(r) & 2)) - 1;
}

void fill_random(int8_t *spin, int L, unsigned long seed) {
    int i;
    gsl_rng *r = initialize_rng(seed);
    for (i = 0; i < L*L; i++) {
        spin[i] = rand_plus_minus(r);
    }
    destroy_rng(r);
}
