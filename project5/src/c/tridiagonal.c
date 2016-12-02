/*
def solve_general(f_func, n, a, b, c):
    x = np.linspace(0, 1, n+2)
    h = x[1] - x[0]
    s = f_func(x)*h**2
    v = np.zeros(n+2)

    # Forward Substitution
    for i in range(2, n+1):
        row_factor = a[i]/b[i-1]      # 1 FLOP
        b[i] -= c[i-1]*row_factor     # 2 FLOPS
        s[i] -= s[i-1]*row_factor     # 2 FLOPS

    #Backward Substitution
    v[n] = s[n]/b[n]

    for i in range(n-1,0,-1):
        v[i] = (s[i] - c[i]*v[i+1]) / b[i]  # 3 FLOPS

    return x, v
*/

void solve_tridiagonal(double *v, double *s, double *a, double *b, double *c,
                       int n) {
    /* we assume arrays are of length n+2 */
    double row_factor;
    int i;

    /* forward substitution */
    for (i = 2; i <= n; i++) {
        row_factor = a[i]/b[i-1];
        b[i] -= c[i-1]*row_factor;
        s[i] -= s[i-1]*row_factor;
    }

    /* backward substitution */
    v[n] = s[n]/b[n];
    for (i = n-1; i > 0; i--) {
        v[i] = (s[i] - c[i]*v[i+1]) / b[i];
    }
}
