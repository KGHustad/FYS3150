
/* TYPEDEFS */
/* type for representing pair of x, y values*/
typedef struct {
    double x, y;
} __attribute__((__packed__)) vec;

typedef struct {
    vec pos, vel;
    double dist, time;
} __attribute__((__packed__)) planet_state;

/* type for a function pointer to one of the integration_algorithms */
typedef void (*integration_func_ptr)(vec*, vec*, vec*, vec*, vec*,
                                     double*, double, int);

typedef void (*acceleration_func_ptr)(vec*, vec, double*, int, int, vec*,
                                      double);

/* ENUMS FOR ALGORITHM OPTIONS */
enum integration_alg {FORWARD_EULER, VELOCITY_VERLET, EULER_CROMER};
enum acceleration_alg {CLASSICAL, RELATIVISTIC};





/* FUNCTIONS */
/* acceleration algorithms */
void acceleration_classical(vec* pos, vec vel, double* masses,
                            int target_body, int num_bodies,
                            vec* acc_ptr, double dt);
void acceleration_relativistic(vec* pos, vec vel, double* masses,
                               int target_body, int num_bodies,
                               vec* acc_ptr, double dt);

/* integration algorithms */
void forward_euler(vec* pos, vec* vel,
                   vec* pos_new, vec* vel_new, vec* acc_buf,
                   double* masses, double dt, int num_bodies);
void velocity_verlet(vec* pos, vec* vel,
                     vec* pos_new, vec* vel_new, vec* acc_buf,
                     double* masses, double dt, int num_bodies);
void euler_cromer(vec* pos, vec* vel,
                  vec* pos_new, vec* vel_new, vec* acc_buf,
                  double* masses, double dt, int num_bodies);

/* utility functions */
void fill_arrays(vec** p, vec** v, double* masses,
                 int num_bodies, long steps, double dt,
                 integration_func_ptr integration_func);
void fill_arrays_every_nth_step(vec** p, vec** v, double* masses,
                                int num_bodies, long steps, double dt,
                                integration_func_ptr integration_func, int n,
                                int *perihelion, planet_state* minima);

int python_interface(double* pos_flat, double* vel_flat, double* masses,
                     double* minima_flat, int num_bodies, long steps,
                     double dt, int skip_saving, int perihelion_capacity,
                     enum integration_alg chosen_integration_alg,
                     enum acceleration_alg chosen_acceleration_alg);
