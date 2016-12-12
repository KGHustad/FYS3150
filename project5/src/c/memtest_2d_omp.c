#include <stdlib.h>
#include "diffuse_2d_omp.h"

int main(int argc, char *argv[]) {
    int height = 4;
    int width = 4;
    double *v = malloc(sizeof(double)*height*width);
    double alpha = 0.1;
    int bc = 0;
    double time_spent;

    solve_2d_omp(v, height, width, alpha, 1, bc, bc, bc, bc, &time_spent);
    solve_2d_omp(v, height, width, alpha, 2, bc, bc, bc, bc, &time_spent);

    free(v);

    return 0;
}
