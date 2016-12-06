#include <stdlib.h>
#include <string.h>

#include "tridiagonal.h"
#include "diffuse_1d.h"

void diffusion_1d_forward_euler(double *v, double alpha, int n, int iters) {
    int i, it;

    /* create buffer array */
    double *v_buf = malloc((n+2)*sizeof(double));
    double *v_new = v_buf;
    double *v_tmp;

    /* save destination array */
    double *v_dest = v;

    /* copy boundaries */
    v_buf[0] = v[0];
    v_buf[n+1] = v[n+1];

    for (it = 0; it < iters; it++) {
        for (i = 1; i <= n; i++) {
            v_new[i] = alpha*v[i+1] + (1 - 2*alpha)*v[i] + alpha*v[i-1];
        }

        /* swap pointers */
        v_tmp = v_new;
        v_new = v;
        v = v_tmp;
    }

    if (v_dest != v_new) {
        memcpy(v_dest, v_new, (n+2)*sizeof(double));
    }
}

void diffusion_1d_backward_euler(double *v, double alpha, int n, int iters) {
    int i, it;
    size_t data_size = (n+2)*sizeof(double);
    double *a = malloc(data_size);
    double *b = malloc(data_size);
    double *c = malloc(data_size);

    /* create buffer array */
    double *v_buf = malloc(data_size);
    double *v_new = v_buf;
    double *v_tmp;

    /* save destination array */
    double *v_dest = v;


    for (it = 0; it < iters; it++) {
        for (i = 0; i <= n+1; i++) {
            a[i] = -alpha;
            b[i] = 1 + 2*alpha;
            c[i] = -alpha;
        }
        solve_tridiagonal(v_new, v, a, b, c, n);

        /* swap pointers */
        v_tmp = v_new;
        v_new = v;
        v = v_tmp;
    }

    if (v_dest != v_new) {
        memcpy(v_dest, v_new, (n+2)*sizeof(double));
    }
}

void diffusion_1d_crank_nicolson(double *v, double alpha, int n, int iters) {
    /* NEEDS TO BE IMPLEMENTED */
}

void solve_1d(double *v, double alpha, int n, int iters, enum solver s) {
    /* NEEDS TO BE IMPLEMENTED */
}
