void solve_tridiagonal(double *v, double *s, double *a, double *b, double *c,
                       int n) {
    /* we assume arrays are of length n+2 */
    double row_factor;
    int i;

    /* forward substitution */
    for (i = 1; i <= n+1; i++) {
        row_factor = a[i]/b[i-1];
        b[i] -= c[i-1]*row_factor;
        s[i] -= s[i-1]*row_factor;
    }

    /* backward substitution */
    v[n] = s[n]/b[n];
    for (i = n; i >= 0; i--) {
        v[i] = (s[i] - c[i]*v[i+1]) / b[i];
    }
}
