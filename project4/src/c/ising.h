typedef struct {
    signed char **data; /* values (may be +1 or -1) */
    int L; /* dimension of lattice */
} lattice;



double find_energy(lattice* lat, double J);
double relative_change_of_energy(lattice* lat, int i, int j);
