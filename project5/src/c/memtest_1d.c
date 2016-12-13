#include <stdlib.h>
#include <stdio.h>
#include "diffuse_1d.h"

int main(int argc, char *argv[]) {
    int solvers[] = {FORWARD_EULER, BACKWARD_EULER, CRANK_NICOLSON};
    int num_solvers = 3;

    int n = 4;
    double alpha = 0.1;
    double *v = malloc(sizeof(double)*(n+2));
    int i;
    for (i = 0; i < n+2; i++) {
        v[i] = i/(double)(n+1);
    }

    for (i = 0; i < num_solvers; i++) {
        solve_1d(v, alpha, n, 2, solvers[i]);
        solve_1d(v, alpha, n, 1, solvers[i]);
    }

    double sum = 0;
    for (i = 0; i < n+2; i++) {
        sum += v[i];
    }

    /* trigger 'conditional jump depends on uninitialized values' by using a
     * variable's value
     */
    if (sum == 0) {
        printf("%g\n", sum);
    }

    free(v);

    return 0;
}
