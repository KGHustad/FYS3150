#ifndef GSL_INCLUDED
#define GSL_INCLUDED
#include <gsl/gsl_rng.h>
#endif

#include <stdint.h>

unsigned long get_unix_seed();
gsl_rng* initialize_rng(unsigned long seed);
void destroy_rng(gsl_rng *r);
