#include "boundary.h"

void update_boundary(double **v, boundary_condition bc, int height, int width) {
    int i, j;

    /* Dirichlet conditions (which are constant in time) need not be updated */
    if (bc.type == DIRICHLET) {
        return;
    } else if (bc.type == NEUMANN) {
        if (bc.pos == TOP || bc.pos == BOTTOM) {
            int i_dest, i_src;
            if (bc.pos == TOP) {
                i_dest = 0;
                i_src = 1;
            } else {
                i_dest = height-1;
                i_src = height-2;
            }
            for (j = 1; j < width - 1; j++) {
                v[i_dest][j] = v[i_src][j];
            }
        }
        if (bc.pos == LEFT || bc.pos == RIGHT) {
            int j_dest, j_src;
            if (bc.pos == LEFT) {
                j_dest = 0;
                j_src = 1;
            } else {
                j_dest = width-1;
                j_src = width-2;
            }
            for (i = 0; i < height; i++) {
                v[i][j_dest] = v[i][j_src];
            }
        }
    }
}
