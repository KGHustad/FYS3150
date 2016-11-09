#include <stdlib.h>

#include "lattice.h"

lattice alloc_lattice(int8_t *spin_flat, int L) {
    int i;
    int8_t **spin = malloc(sizeof(int8_t*)*L);
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
