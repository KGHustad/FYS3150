#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <mpi.h>

#include "common.h"

void diffusion_2d_mpi(double **v,
                      int height, int width,
                      double kappa, int iters, MPI_Comm comm) {
    /* Assume data is already distributed  */
    int my_rank, num_procs;
    MPI_Comm_rank (comm, &my_rank);
    MPI_Comm_size (comm, &num_procs);

    /* v and v_bar should be different arrays with identical contents */
    double **v_buf = alloc_2d_array(height, width);
    double **v_bar = v_buf;
    memcpy_2d_array(v_bar, v, height, width);

    /* store destination before any pointer swaps occur */
    double **v_dest = v;
    double** temp;

    /* allocate, if necessary, memory to store rows above and below */
    size_t row_size = sizeof(double)*width;
    double *row_above = NULL, *row_below = NULL;
    if (my_rank != 0) {
        row_above = malloc(row_size);
    }
    if (my_rank != num_procs-1) {
        row_below = malloc(row_size);
    }

    MPI_Status status;

    /* create buffer for sending */
    /* find size of single message */
    int msg_size;
    MPI_Pack_size(width, MPI_DOUBLE, comm, &msg_size);
    /* each region has at most two adjacent regions (above and below) */
    int neighbours = 2;
    /* there can be at most 2 outstanding sends per neighbour, thus the buffer
       needs to be of size 2*neighbours*(size of a message incl. overhead) */
    int buf_size = 2*neighbours*(msg_size+MPI_BSEND_OVERHEAD);
    void* buf = malloc(buf_size);
    MPI_Buffer_attach(buf, buf_size);

    int it, i, j;
    for (it=1; it <= iters; it++) {
        /* buffered send */
        /* to above */
        if (my_rank != 0) {
            MPI_Bsend(v[0], width, MPI_DOUBLE, my_rank-1, it, comm);
        }
        /* to below */
        if (my_rank != num_procs-1) {
            MPI_Bsend(v[height-1], width, MPI_DOUBLE, my_rank+1, it,
                     comm);
        }

        /* compute inner points */
        for (i=1; i < height-1; i++) {
            for (j=1; j < width-1; j++) {
                v_bar[i][j] = v[i][j]
                              + kappa*(v[i-1][j] + v[i][j-1] - 4*v[i][j]
                                       + v[i][j+1] + v[i+1][j]);
            }
        }

        /* receive */
        /* from above */
        if (my_rank != 0) {
            MPI_Recv(row_above, width, MPI_DOUBLE, my_rank-1, it, comm,
                     &status);
            i = 0;
            for (j=1; j < width-1; j++) {
                v_bar[i][j] = v[i][j]
                              + kappa*(row_above[j] + v[i][j-1] - 4*v[i][j]
                                       + v[i][j+1] + v[i+1][j]);
            }
        }
        /* from below */
        if (my_rank != num_procs-1) {
            MPI_Recv(row_below, width, MPI_DOUBLE, my_rank+1, it, comm,
                     &status);
            i = height-1;
            for (j=1; j < width-1; j++) {
                v_bar[i][j] = v[i][j]
                              + kappa*(v[i-1][j] + v[i][j-1] - 4*v[i][j]
                                       + v[i][j+1] + row_below[j]);
            }
        }

        /* TODO: implement boundary conditions */

        /* swap pointers */
        temp = v;
        v = v_bar;
        v_bar = temp;
    }

    /* ensure final data is stored in correct location */
    if (v != v_dest) {
        memcpy_2d_array(v_dest, v, height, width);
    }

    /* free, if necessary, memory allocated to store rows above and below */
    if (my_rank != 0) {
        free(row_above);
    }
    if (my_rank != num_procs-1) {
        free(row_below);
    }

    /* detach and free send buffer */
    MPI_Buffer_detach(buf, &buf_size);
    free(buf);

    /* free v_bar */
    free_2d_array(v_buf);
}


void solve_2d_mpi(double *v_flat, int height, int width,
                  double kappa, int iters, MPI_Comm comm) {
    /* THIS FUNCTION WOULD NEED TO DISTRIBUTE THE DATA IF IT IS NOT DONE IN
     * THE LAYER ABOVE (I.E. IN PYTHON)
     */
    double **v = alloc_2d_array_from_flat(v_flat, height, width);
    diffusion_2d_mpi(v, height, width, kappa, iters, comm);
    free(v);
}
