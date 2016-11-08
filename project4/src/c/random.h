#ifndef GSL_INCLUDED
#define GSL_INCLUDED
#include <gsl/gsl_rng.h>
#endif

gsl_rng* initialize_rng();
inline signed char rand_plus_minus(gsl_rng *r);
void destroy_rng(gsl_rng *r);
