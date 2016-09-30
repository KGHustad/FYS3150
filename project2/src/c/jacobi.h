

double find_max_nondiagonal(double** A, int n, int* k_ptr, int* l_ptr);
void rotate(double** A, double** R, int n, int k, int l);
int solve(double** A, double** R, int n, double tol);
int jacobi(double* A_data, double* R_data, int n, double tol);
