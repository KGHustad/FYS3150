#include "random.h"

gsl_rng* initialize_rng() {
    const gsl_rng_type * T; /* specifies the type of random number generator */
    gsl_rng * r; /* pointer to random number generator */

    gsl_rng_env_setup();

    T = gsl_rng_default;
    r = gsl_rng_alloc(T);
    return r;
}

inline int8_t rand_plus_minus(gsl_rng *r) {
    /*
    bitwise AND with 2 can yield 2 or 0, subtracting 1,
    the returned number is either -1 or 1
    */
    return ((int8_t) (gsl_rng_get(r) & 2)) - 1;
}

void destroy_rng(gsl_rng *r) {
    gsl_rng_free(r);
}
