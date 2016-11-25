#include <stdlib.h>
#include <string.h>

#include "common.h"

double** alloc_2d_array(int rows, int columns) {
    double *data = malloc(sizeof(double)*rows*columns);
    double **a = malloc(sizeof(double*)*rows);
    int i;
    for (i = 0; i < rows; i++) {
        a[i] = data + i*columns;
    }
    return a;
}

void memcpy_2d_array(double **dest, double **src, int rows, int columns) {
    memcpy(dest[0], src[0], sizeof(double)*rows*columns);
}

void free_2d_array(double **a) {
    free(a[0]);
    free(a);
}
