

typedef struct {
    double x, y;
} coor;

void acceleration(coor* pos, double* masses, int target_body, int num_bodies,
                  coor* acc_ptr, double dt);


void forward_euler(coor* pos, coor* vel,
                   coor* pos_new, coor* vel_new, coor* acc_buf,
                   double* masses, double dt, int num_bodies);
void velocity_verlet(coor* pos, coor* vel,
                     coor* pos_new, coor* vel_new, coor* acc_buf,
                     double* masses, double dt, int num_bodies);

void fill_arrays(coor** p, coor** v, double* masses,
                 int num_bodies, int steps, double dt);

void solve(double* pos_flat, double* vel_flat, double* masses,
           int num_bodies, int steps, double dt);
