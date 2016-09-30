#include <stdlib.h>
#include <math.h>

#include "jacobi.h"

double find_max_nondiagonal(double** A, int n, int* k_ptr, int* l_ptr) {
    int max_k = 0;
    int max_l = 1;
    double maximum = fabs(A[max_k][max_l]);
    double current;
    int i, j;
    for (i=0; i < n; i++) {
        for (j=i+1; j < n; j++) {
            current = fabs(A[i][j]);
            if (current > maximum) {
                maximum = current;
                max_k = i;
                max_l = j;
            }
        }
    }
    *k_ptr = max_k;
    *l_ptr = max_l;
    return maximum;
}

void rotate(double** A, double** R, int n, int k, int l) {
    double tau = (A[l][l] - A[k][k])/(2*A[k][l]);
    double t;
    if (tau > 0) {
        t = 1./(tau + sqrt(1 + tau*tau));
    } else {
        t = 1./(tau - sqrt(1 + tau*tau));
    }
    double c = 1 / sqrt(1+t*t);
    double s = c*t;

    // we need to store some values for later use
    double a_kk = A[k][k];
    double a_ll = A[l][l];

    A[k][k] = c*c*a_kk - 2*c*s*A[k][l] + s*s*a_ll;
    A[l][l] = s*s*a_kk + 2*c*s*A[k][l] + c*c*a_ll;
    A[k][l] = 0;
    A[l][k] = 0;

    double a_ik, a_il, r_ik, r_il;
    int i;
    for (i=0; i < n; i++) {
        if (i != k && i != l) {
            a_ik = A[i][k];
            a_il = A[i][l];
            A[i][k] = c*a_ik - s*a_il;
            A[k][i] = A[i][k];
            A[i][l] = c*a_il + s*a_ik;
            A[l][i] = A[i][l];
        }
        r_ik = R[i][k];
        r_il = R[i][l];
        R[i][k] = c*r_ik - s*r_il;
        R[i][l] = c*r_il + s*r_ik;
    }
}

int solve(double** A, double** R, int n, double tol) {
    int iterations = 0;
    int k, l;
    double maximum = find_max_nondiagonal(A, n, &k, &l);
    while (maximum > tol) {
        iterations++;
        rotate(A, R, n, k, l);
        maximum = find_max_nondiagonal(A, n, &k, &l);
    }
    return iterations;
}

/* the function we want to call from Python */
int jacobi(double* A_data, double* R_data, int n, double tol) {
    /* set up abstraction to make our 1D array behave like a 2D array */
    double **A, **R;
    A = (double**) malloc(sizeof(double*)*n);
    R = (double**) malloc(sizeof(double*)*n);

    int i;
    for (i=0; i < n; i++) {
        A[i] = A_data + i*n;
        R[i] = R_data + i*n;
    }

    /* solve */
    int iterations = solve(A, R, n, tol);

    /* free 2D array */
    free(A);
    free(R);
    return iterations;
}
