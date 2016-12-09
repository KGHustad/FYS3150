#include <signal.h>

void abort_execution(int sig);

double** alloc_2d_array_from_flat(double *a_flat, int rows, int columns);
double** alloc_2d_array(int rows, int columns);
void memcpy_2d_array(double **dest, double **src, int rows, int columns);
void copy_selection_2d_array(double **dest, double **src,
                             int dest_row_offset, int dest_col_offset,
                             int src_row_offset, int src_col_offset,
                             int rows, int cols);
void free_2d_array(double **a);
