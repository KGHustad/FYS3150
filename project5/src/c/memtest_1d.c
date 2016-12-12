#include <stdlib.h>
#include "diffuse_1d.h"

int main(int argc, char *argv[]) {
    int solvers[] = {FORWARD_EULER, BACKWARD_EULER, CRANK_NICOLSON};
    int num_solvers = 3;

    int n = 4;
    double *v = malloc(sizeof(double)*(n+2));
    double alpha = 0.1;

    int i;
    for (i = 0; i < num_solvers; i++) {
        solve_1d(v, alpha, n, 2, solvers[i]);
        solve_1d(v, alpha, n, 1, solvers[i]);
    }

    free(v);

    return 0;
}
