#include "boundary.h"

void diffusion_2d_omp(double **v,
                      int height, int width,
                      double kappa, int iters,
                      boundary_condition left, boundary_condition right,
                      boundary_condition top, boundary_condition bottom);
void solve_2d_omp(double *v_flat, int height, int width,
                  double kappa, int iters, int bc_left, int bc_right,
                  int bc_top, int bc_bottom, double *time_spent);
