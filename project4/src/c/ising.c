#include <stdlib.h>
#include <stdint.h>

#include "ising.h"

double find_energy(lattice* lat, double J) {
    int L = lat->L;
    signed char **A = lat->data;

    double E = 0;

    int i, j;
    for (i = 0; i < L; i++) {
        for (j = 0; j < L; j++) {
            E += A[i][j] * A[(i+1) % L][j];     /* horizontal neighbour */
            E += A[i][j] * A[i][(j-1) % L];     /* vertical neighbour */
        }
    }
    return -J*E;
}

/* function to compute the change of energy, given that lat.data[i][j] is flipped */
double relative_change_of_energy(lattice* lat, int i, int j) {
    int L = lat->L;
    signed char **A = lat->data;

    signed char E_old_up, E_old_down, E_old_left, E_old_right, E_old;

    E_old_right =   A[i][j] * A[(i+1)%L][j];
    E_old_left =    A[i][j] * A[(i-1)%L][j];
    E_old_up =      A[i][j] * A[i][(j+1)%L];
    E_old_down =    A[i][j] * A[i][(j-1)%L];
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
