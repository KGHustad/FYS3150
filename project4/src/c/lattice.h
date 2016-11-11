#include <stdint.h>

typedef struct {
    int8_t **spin; /* spin values (may be +1 or -1) */
    int L; /* dimension of lattice */
    double energy;
    long tot_magnetization;
    long accepted_configurations;
} lattice;

lattice alloc_lattice(int8_t *spin_flat, int L);
void free_lattice(lattice lat);
