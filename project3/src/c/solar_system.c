#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include "solar_system.h"

/* global variable specifying which acceleration algorithm to use */
acceleration_func_ptr acceleration_func;


/* acceleration algorithms */

void acceleration_classical(vec* pos, vec vel, double* masses,
                            int target_body, int num_bodies,
                            vec* acc_ptr, double dt) {
    double x_acc = 0;
    double y_acc = 0;
    double x_dist;
    double y_dist;
    double distance, distance_cubed;
    int body;
    for (body = 0; body < num_bodies; body++) {
        if (body != target_body) {
            x_dist = pos[target_body].x - pos[body].x;
            y_dist = pos[target_body].y - pos[body].y;
            distance = sqrt(x_dist*x_dist + y_dist*y_dist);
            distance_cubed = distance * distance * distance;

            x_acc -= G*masses[body]*x_dist/distance_cubed;
            y_acc -= G*masses[body]*y_dist/distance_cubed;
        }
    }
    acc_ptr->x = x_acc;
    acc_ptr->y = y_acc;
}

void acceleration_relativistic(vec* pos, vec vel, double* masses,
                               int target_body, int num_bodies,
                               vec* acc_ptr, double dt) {
    double x_acc = 0;
    double y_acc = 0;
    double x_dist;
    double y_dist;
    double distance, distance_squared, distance_cubed;
    double v_squared;
    double rel_fac;
    int body;
    for (body = 0; body < num_bodies; body++) {
        if (body != target_body) {
            x_dist = pos[target_body].x - pos[body].x;
            y_dist = pos[target_body].y - pos[body].y;
            distance = sqrt(x_dist*x_dist + y_dist*y_dist);
            distance_squared = distance * distance;
            distance_cubed = distance_squared * distance;

            v_squared = vel.x*vel.x + vel.y*vel.y;
            rel_fac = 1 + (3*v_squared) / (distance_squared*c_squared);

            x_acc -= G*masses[body]*x_dist/distance_cubed*rel_fac;
            y_acc -= G*masses[body]*y_dist/distance_cubed*rel_fac;
        }
    }
    acc_ptr->x = x_acc;
    acc_ptr->y = y_acc;
}


/* integration algorithms */

void forward_euler(vec* pos, vec* vel,
                   vec* pos_new, vec* vel_new, vec* acc_buf,
                   double* masses, double dt, int num_bodies) {
    vec acc;
    int i;
    for (i = 0; i < num_bodies; i++) {
        (*acceleration_func)(pos, vel[i], masses, i, num_bodies, &acc, dt);
        vel_new[i].x = vel[i].x + acc.x*dt;
        vel_new[i].y = vel[i].y + acc.y*dt;
        pos_new[i].x = pos[i].x + vel_new[i].x*dt;
        pos_new[i].y = pos[i].y + vel_new[i].y*dt;
    }
}

void velocity_verlet(vec* pos, vec* vel,
                     vec* pos_new, vec* vel_new, vec* acc_buf,
                     double* masses, double dt, int num_bodies) {
    vec acc_new;

    int i;
    double dt_sq = dt*dt;
    for (i = 0; i < num_bodies; i++) {
        (*acceleration_func)(pos, vel[i], masses, i, num_bodies, acc_buf+i, dt);
        pos_new[i].x = pos[i].x + vel[i].x*dt + 0.5*dt_sq*acc_buf[i].x;
        pos_new[i].y = pos[i].y + vel[i].y*dt + 0.5*dt_sq*acc_buf[i].y;
    }
    for (i = 0; i < num_bodies; i++) {
        (*acceleration_func)(pos_new, vel_new[i], masses, i, num_bodies, &acc_new, dt);
        vel_new[i].x = vel[i].x + 0.5*(acc_buf[i].x + acc_new.x)*dt;
        vel_new[i].y = vel[i].y + 0.5*(acc_buf[i].y + acc_new.y)*dt;
    }
}


/* utility functions */

void fill_arrays(vec** p, vec** v, double* masses,
                 int num_bodies, int steps, double dt,
                 integration_func_ptr integration_func) {
    int i;
    vec* acc_buf = malloc(sizeof(vec)*num_bodies);
    for (i = 0; i < steps; i++) {
        (*integration_func)(p[i], v[i], p[i+1], v[i+1], acc_buf, masses, dt,
                            num_bodies);
    }
    free(acc_buf);
}

void python_interface(double* pos_flat, double* vel_flat, double* masses,
                      int num_bodies, int steps, double dt,
                      enum integration_alg chosen_integration_alg,
                      enum acceleration_alg chosen_acceleration_alg) {
    /* handle options */
    integration_func_ptr integration_func;
    switch (chosen_integration_alg) {
        case FORWARD_EULER:
            integration_func = &forward_euler;
            break;

        case VELOCITY_VERLET:
            integration_func = &velocity_verlet;
            break;

        default:
            printf("Warning: Unrecognized integration algorithm. "
                   "Defaulting to VELOCITY_VERLET.\n");
            integration_func = &velocity_verlet;
    }

    /* acceleration_func is a global variable */
    switch (chosen_acceleration_alg) {
        case CLASSICAL:
            acceleration_func = &acceleration_classical;
            break;

        case RELATIVISTIC:
            acceleration_func = &acceleration_relativistic;
            break;

        default:
            printf("Warning: Unrecognized acceleration algorithm. "
                   "Defaulting to CLASSICAL.\n");
            acceleration_func = &acceleration_classical;
    }


    /* setup arrays */
    vec* p_flat = (vec*) pos_flat;
    vec* v_flat = (vec*) vel_flat;

    int i;

    vec** p = malloc(sizeof(vec*)*steps+1);
    vec** v = malloc(sizeof(vec*)*steps+1);
    for (i = 0; i < steps+1; i++) {
        p[i] = p_flat + num_bodies*i;
        v[i] = v_flat + num_bodies*i;
    }

    fill_arrays(p, v, masses, num_bodies, steps, dt, integration_func);

    free(p);
    free(v);
}
