#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include "common.h"
#include "tridiagonal.h"
#include "diffuse_1d.h"

void diffusion_1d_forward_euler(double *v, double alpha, int n, int iters) {
    int i, it;

    /* create buffer array */
    size_t data_size = (n+2)*sizeof(double);
    double *v_buf = malloc(data_size);
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
        memcpy(v_dest, v_new, data_size);
    }

    free(v_buf);
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
    memcpy(v_new, v, data_size);
    double *v_tmp;

    /* save destination array */
    double *v_dest = v;

    for (it = 0; it < iters; it++) {
        /* set up matrix */
        for (i = 1; i <= n; i++) {
            a[i] = -alpha;
            b[i] = 1 + 2*alpha;
            c[i] = -alpha;
        }
        /* ensure no change at the boundaries */
        b[0] = 1;
        c[0] = 0;
        b[n+1] = 1;
        a[n+1] = 0;

        solve_tridiagonal(v_new, v, a, b, c, n);

        /* swap pointers */
        v_tmp = v_new;
        v_new = v;
        v = v_tmp;
    }

    if (v_dest != v) {
        memcpy(v_dest, v, data_size);
    }

    free(a);
    free(b);
    free(c);
    free(v_buf);
}

void diffusion_1d_crank_nicolson(double *v, double alpha, int n, int iters) {
    int i, it;
    size_t data_size = (n+2)*sizeof(double);
    double *a = malloc(data_size);
    double *b = malloc(data_size);
    double *c = malloc(data_size);

    /* create buffer array */
    double *v_buf = malloc(data_size);
    double *v_old = v_buf;
    memcpy(v_old, v, data_size);

    for (it = 0; it < iters; it++) {
        for (i = 0; i <= n+1; i++) {
            a[i] = -alpha;
            b[i] = 2 + 2*alpha;
            c[i] = -alpha;
        }
        /* ensure no change at the boundaries */
        b[0] = 1;
        c[0] = 0;
        b[n+1] = 1;
        a[n+1] = 0;

        for (i = 1; i <= n; i++) {
            v_old[i] = alpha*v[i-1] + (2 - 2*alpha)*v[i] + alpha*v[i+1];
        }

        solve_tridiagonal(v, v_old, a, b, c, n);
    }

    free(a);
    free(b);
    free(c);
    free(v_buf);
}

void solve_1d(double *v, double alpha, int n, int iters, enum solver s) {
    /* set signal handler */
    signal(SIGINT, abort_execution);

    void (*selected_solver)(double *, double, int, int);

    /* choose solver */
    switch (s) {
        case FORWARD_EULER:
            selected_solver = diffusion_1d_forward_euler;
            break;

        case BACKWARD_EULER:
            selected_solver = diffusion_1d_backward_euler;
            break;

        case CRANK_NICOLSON:
            selected_solver = diffusion_1d_crank_nicolson;
            break;

        default:
            printf("ERROR: Unrecognized solver!\n");
            exit(EXIT_FAILURE);
    }

    selected_solver(v, alpha, n, iters);
}
