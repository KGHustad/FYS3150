#include <stdlib.h>
#include <string.h>

#include "common.h"
#include "boundary.h"

void diffusion_2d(double **v, double **f,
                  int height, int width,
                  double kappa, int iters,
                  boundary_condition left, boundary_condition right,
                  boundary_condition top, boundary_condition bottom) {
    /* v and v_bar should be different arrays with identical contents */
    double **v_bar = alloc_2d_array(height, width);
    memcpy_2d_array(v_bar, v, height, width);

    /* store destination before any pointer swaps occur */
    double **v_dest = v;
    double** temp;

    int it, i, j;
    for (it = 1; it <= iters; it++) {
        /* update inner points */
        for (i = 1; i < height - 1; i++) {
            for (j = 1; j < width - 1; j++) {
                v_bar[i][j] = v[i][j]
                              + kappa*(v[i-1][j] + v[i][j-1] - 4*v[i][j]
                                     + v[i][j+1] + v[i+1][j]);
            }
        }

        /* boundaries */
        update_boundary(v_bar, top, height, width);
        update_boundary(v_bar, bottom, height, width);
        update_boundary(v_bar, left, height, width);
        update_boundary(v_bar, right, height, width);

        /* swap pointers */
        temp = v;
        v = v_bar;
        v_bar = temp;
    }

    /* ensure final data is stored in correct location */
    if (v != v_dest) {
        memcpy(v[0], v_dest[0], sizeof(double)*width*height);
    }

    /* free v_bar */
    free_2d_array(v_bar);
}


void solve_2d(double *v_flat, double *f_flat, int width, int height,
              double kappa, int iters, int bc_left, int bc_right,
              int bc_top, int bc_bottom) {
    boundary_condition left, right, top, bottom;
    left.pos = LEFT;
    left.type = bc_left;
    right.pos = RIGHT;
    right.type = bc_right;
    top.pos = TOP;
    top.type = bc_top;
    bottom.pos = BOTTOM;
    bottom.type = bc_bottom;

    double **v = alloc_2d_array_from_flat(v_flat, height, width);
    double **f = alloc_2d_array_from_flat(f_flat, height, width);
    diffusion_2d(v, f, height, width, kappa, iters, left, right, top, bottom);
    free(v);
    free(f);
}
