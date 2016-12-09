enum solver {FORWARD_EULER, BACKWARD_EULER, CRANK_NICOLSON};

void diffusion_1d_forward_euler(double *v, double alpha, int n, int iters);
void diffusion_1d_backward_euler(double *v, double alpha, int n, int iters);
void diffusion_1d_crank_nicolson(double *v, double alpha, int n, int iters);
void solve_1d(double *v, double alpha, int n, int iters, enum solver s);
