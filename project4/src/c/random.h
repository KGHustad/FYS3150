#ifndef GSL_INCLUDED
#define GSL_INCLUDED
#include <gsl/gsl_rng.h>
#endif

#include <stdint.h>

unsigned long get_unix_seed(void);
gsl_rng* initialize_rng();
inline int8_t rand_plus_minus(gsl_rng *r);
void destroy_rng(gsl_rng *r);