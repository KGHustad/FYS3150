#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include "common.h"

void abort_execution(int sig) {
    fprintf(stderr, "Aborted execution\n");
    exit(EXIT_SUCCESS);
}

double** alloc_2d_array_from_flat(double *a_flat, int rows, int columns) {
    double **a = malloc(sizeof(double*)*rows);
    int i;
    for (i = 0; i < rows; i++) {
        a[i] = a_flat + i*columns;
    }
    return a;
}

double** alloc_2d_array(int rows, int columns) {
    double *data = malloc(sizeof(double)*rows*columns);
    double **a = alloc_2d_array_from_flat(data, rows, columns);
    return a;
}

void memcpy_2d_array(double **dest, double **src, int rows, int columns) {
    memcpy(dest[0], src[0], sizeof(double)*rows*columns);
}

void copy_selection_2d_array(double **dest, double **src,
                             int dest_row_offset, int dest_col_offset,
                             int src_row_offset, int src_col_offset,
                             int rows, int cols) {
    int row;
    for (row=0; row < rows; row++) {
        memcpy(dest[row + dest_row_offset]+dest_col_offset,
               src[row + src_row_offset]+src_col_offset,
               sizeof(double)*cols);
    }
}

void free_2d_array(double **a) {
    free(a[0]);
    free(a);
}
