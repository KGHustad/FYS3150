
/* TYPEDEFS */
/* type for representing pair of x, y values*/
typedef struct {
    double x, y;
} vec;

/* type for a function pointer to one of the integration_algorithms */
typedef void (*integration_func_ptr)(vec*, vec*, vec*, vec*, vec*,
                                     double*, double, int);

typedef void (*acceleration_func_ptr)(vec*, vec, double*, int, int, vec*,
                                      double);

/* ENUMS FOR ALGORITHM OPTIONS */
enum integration_alg {FORWARD_EULER, VELOCITY_VERLET};
enum acceleration_alg {CLASSICAL, RELATIVISTIC};


/* PHYSICAL CONSTANTS */
#define SPEED_OF_LIGHT 63197.8
const double c_squared = SPEED_OF_LIGHT * SPEED_OF_LIGHT;
const double G = 4*M_PI*M_PI;


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

/* utility functions */
void fill_arrays(vec** p, vec** v, double* masses,
                 int num_bodies, int steps, double dt,
                 integration_func_ptr integration_func);
void fill_arrays_every_nth_step(vec** p, vec** v, double* masses,
                                int num_bodies, int steps, double dt,
                                integration_func_ptr integration_func, int n);

void python_interface(double* pos_flat, double* vel_flat, double* masses,
                      int num_bodies, int steps, double dt, int skip_saving,
                      enum integration_alg chosen_integration_alg,
                      enum acceleration_alg chosen_acceleration_alg);
