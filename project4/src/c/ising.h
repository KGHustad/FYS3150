typedef struct {
    signed char **spin; /* spin values (may be +1 or -1) */
    int L; /* dimension of lattice */
    double energy;
    long mean_magnetization;
} lattice;


double find_energy(lattice* lat, double J);
int relative_change_of_energy(lattice* lat, int i, int j);
