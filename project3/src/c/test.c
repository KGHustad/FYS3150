#include <stdlib.h>
#include <stdio.h>
#include <math.h>
/*
#include <string.h>
#include <signal.h>
*/

#include "solar_system.h"


int main() {
    long steps = (int) 2E4;
    double years = 0.100;
    double dt = years/steps;
    int num_bodies = 2;
    size_t tot_size = sizeof(double)*2*num_bodies*(steps+1);

    int minima_capacity = 100;
    double *pos_flat = malloc(tot_size);
    double *vel_flat = malloc(tot_size);
    double *masses = malloc(sizeof(double)*num_bodies);
    double *minima_flat = malloc(sizeof(planet_state)*minima_capacity);

    /*
    memset(pos_flat, 0, tot_size);
    memset(vel_flat, 0, tot_size);
    */

    /* set up planets */
    double mercurymass = 0.1652e-6;
    double mercuryspeed = 12.44;
    double mercury_perihelion_distance = 0.3075;

    // sun
    masses[0] = 1;
    pos_flat[0] = 0 - mercury_perihelion_distance*mercurymass;
    pos_flat[1] = 0;
    vel_flat[0] = 0;
    vel_flat[1] = 0 - mercuryspeed*mercurymass;

    masses[1] = 0.166e-6;
    pos_flat[2] = mercury_perihelion_distance;
    pos_flat[3] = 0;
    vel_flat[2] = 0;
    vel_flat[3] = mercuryspeed;

    python_interface(pos_flat, vel_flat, masses, minima_flat, num_bodies,
                     steps, dt, 0, minima_capacity, 1, 1);

    /*
    int i;
    for (i = 0; i < 3; i++) {
        printf("%15E  %15E    %15E  %15E\n",
                pos_flat[4*i    ], pos_flat[4*i + 1],
                pos_flat[4*i + 2], pos_flat[4*i + 3]
            );
    }
    */

    free(masses);
    free(pos_flat);
    free(vel_flat);
    free(minima_flat);
    return 0;
}
