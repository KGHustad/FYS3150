
/* TYPEDEFS */
/* type for representing pair of x, y values*/
typedef struct {
    double x, y;
} coor;

/* type for a functionpointer to one of the integration_algorithms */
typedef void (*integration_func_ptr)(coor*, coor*, coor*, coor*, coor*,
                                     double*, double, int);

typedef void (*acceleration_func_ptr)(coor*, coor, double*, int, int, coor*,
                                      double);

/* ENUMS FOR ALGORITHM OPTIONS */
enum integration_alg {FORWARD_EULER, VELOCITY_VERLET};
enum acceleration_alg {CLASSICAL, RELATIVISTIC};


/* PHYSICAL CONSTANTS */
#define SPEED_OF_LIGHT 63197.8
const double c_squared = SPEED_OF_LIGHT * SPEED_OF_LIGHT;
const double G = 4*M_PI*M_PI;


/* FUNCTIONS */
void acceleration_classical(coor* pos, coor vel, double* masses,
                            int target_body, int num_bodies,
                            coor* acc_ptr, double dt);
/* TODO: Relativistic acceleration */
void acceleration_relativistic(coor* pos, coor vel, double* masses,
                               int target_body, int num_bodies,
                               coor* acc_ptr, double dt);

void forward_euler(coor* pos, coor* vel,
                   coor* pos_new, coor* vel_new, coor* acc_buf,
                   double* masses, double dt, int num_bodies);
void velocity_verlet(coor* pos, coor* vel,
                     coor* pos_new, coor* vel_new, coor* acc_buf,
                     double* masses, double dt, int num_bodies);

void fill_arrays(coor** p, coor** v, double* masses,
                 int num_bodies, int steps, double dt,
                 integration_func_ptr integration_func);

void python_interface(double* pos_flat, double* vel_flat, double* masses,
                      int num_bodies, int steps, double dt,
                      enum integration_alg chosen_integration_alg,
                      enum acceleration_alg chosen_acceleration_alg);
