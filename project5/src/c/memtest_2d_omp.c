#include <stdlib.h>
#include <stdio.h>
#include "diffuse_2d_omp.h"

int main(int argc, char *argv[]) {
    int height = 4;
    int width = 4;
    double *v = malloc(sizeof(double)*height*width);
    double alpha = 0.1;
    int bc = 0;
    double time_spent;

    int i;
    for (i = 0; i < height*width; i++) {
        v[i] = i/(double)(height*width);
    }

    solve_2d_omp(v, height, width, alpha, 1, bc, bc, bc, bc, &time_spent);
    solve_2d_omp(v, height, width, alpha, 2, bc, bc, bc, bc, &time_spent);

    double sum = 0;
    for (i = 0; i < height*width; i++) {
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
