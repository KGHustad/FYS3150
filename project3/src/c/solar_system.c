#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <string.h>
#include <signal.h>

#include "solar_system.h"

/* PHYSICAL CONSTANTS */
#define SPEED_OF_LIGHT 63197.8
const double c_squared = SPEED_OF_LIGHT * SPEED_OF_LIGHT;
const double G = 4*M_PI*M_PI;

/* global variable specifying which acceleration algorithm to use */
acceleration_func_ptr acceleration_func;


static inline double norm(vec *v) {
    return sqrt(v->x * v->x + v->y * v->y);
}

/*** ACCELERATION ALGORITHMS ***/

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
    double l;
    double rel_fac;
    int body;
    for (body = 0; body < num_bodies; body++) {
        if (body != target_body) {
            x_dist = pos[target_body].x - pos[body].x;
            y_dist = pos[target_body].y - pos[body].y;
            distance = sqrt(x_dist*x_dist + y_dist*y_dist);
            distance_squared = distance * distance;
            distance_cubed = distance_squared * distance;

            l = pos[target_body].x*vel.y - pos[target_body].y*vel.x;
            rel_fac = 1 + (3*l*l) / (distance_squared*c_squared);

            x_acc -= G*masses[body]*x_dist/distance_cubed*rel_fac;
            y_acc -= G*masses[body]*y_dist/distance_cubed*rel_fac;
        }
    }
    acc_ptr->x = x_acc;
    acc_ptr->y = y_acc;
}


/*** INTEGRATION ALGORITHMS ***/

void forward_euler(vec* pos, vec* vel,
                   vec* pos_new, vec* vel_new, vec* acc_buf,
                   double* masses, double dt, int num_bodies) {
    vec acc;
    int i;
    for (i = 0; i < num_bodies; i++) {
        (*acceleration_func)(pos, vel[i], masses, i, num_bodies, &acc, dt);
        pos_new[i].x = pos[i].x + vel[i].x*dt;
        pos_new[i].y = pos[i].y + vel[i].y*dt;
        vel_new[i].x = vel[i].x + acc.x*dt;
        vel_new[i].y = vel[i].y + acc.y*dt;
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
        (*acceleration_func)(pos_new, vel[i], masses, i, num_bodies, &acc_new, dt);
        vel_new[i].x = vel[i].x + 0.5*(acc_buf[i].x + acc_new.x)*dt;
        vel_new[i].y = vel[i].y + 0.5*(acc_buf[i].y + acc_new.y)*dt;
    }
}

void euler_cromer(vec* pos, vec* vel,
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


/*** UTILITY FUNCTIONS ***/

void fill_arrays(vec** p, vec** v, double* masses,
                 int num_bodies, long steps, double dt,
                 integration_func_ptr integration_func) {
    long i;
    vec* acc_buf = malloc(sizeof(vec)*num_bodies);
    for (i = 0; i < steps; i++) {
        (*integration_func)(p[i], v[i], p[i+1], v[i+1], acc_buf, masses, dt,
                            num_bodies);
    }
    free(acc_buf);
}

void fill_arrays_every_nth_step(vec** p, vec** v, double* masses,
                                int num_bodies, long steps, double dt,
                                integration_func_ptr integration_func, int n,
                                int *recorded_minima, planet_state* minima) {
    const int perihelion = *recorded_minima;
    if (perihelion && num_bodies < 2) {
        printf("Two bodies are required for there to be a perihelion");
        exit(1);
    }

    planet_state prev_prev, prev, curr;
    const int PERIHELION_BODY = 1;
    int minima_counter = 0;

    /* initialize planet states */
    curr.pos = p[0][PERIHELION_BODY];
    curr.vel = v[0][PERIHELION_BODY];
    curr.time = 0;
    curr.dist = norm(&(curr.pos));
    prev_prev = prev = curr;

    int i, j;
    size_t tot_vec_size = sizeof(vec)*num_bodies;
    vec* acc_buf = malloc(tot_vec_size);

    /* allocate buffers for current and previous step */
    vec *p_a, *p_b;
    vec *v_a, *v_b;
    p_a = malloc(tot_vec_size);
    p_b = malloc(tot_vec_size);
    v_a = malloc(tot_vec_size);
    v_b = malloc(tot_vec_size);

    /* we will need a second set of pointers to do pointer swaps */
    vec *p_old = p_a, *p_new = p_b, *p_tmp;
    vec *v_old = v_a, *v_new = v_b, *v_tmp;

    /* copy in first step */
    memcpy(p_old, p[0], tot_vec_size);
    memcpy(v_old, v[0], tot_vec_size);

    long counter=0;
    for (i = 0; i < steps; i++) {
        for (j = 0; j < n; j++) {
            counter++;
            (*integration_func)(p_old, v_old, p_new, v_new, acc_buf, masses, dt,
                                num_bodies);

            if (perihelion) {
                prev_prev = prev;
                prev = curr;
                curr.pos = p_new[PERIHELION_BODY];
                curr.vel = v_new[PERIHELION_BODY];
                curr.time = counter*dt;
                curr.dist = norm(&(curr.pos));

                if (prev_prev.dist > prev.dist && prev.dist < curr.dist) {
                    if (minima_counter < perihelion) {
                        minima[minima_counter++] = prev;
                    } else if (minima_counter++ == perihelion) {
                        printf("WARNING: Minima buffer is full! "
                               "Remaining minima will not be recorded.\n");
                    }
                }
            }


            /* pointer swapping */
            p_tmp = p_old;
            p_old = p_new;
            p_new = p_tmp;
            v_tmp = v_old;
            v_old = v_new;
            v_new = v_tmp;
        }

        /* save result in array */
        memcpy(p[i+1], p_old, tot_vec_size);
        memcpy(v[i+1], v_old, tot_vec_size);
    }

    printf("%ld iterations (saving every %d-th number)\n", counter, n);
    if (perihelion) {
        printf("Found %d minima\n", minima_counter);
        if (minima_counter < perihelion) {
            *recorded_minima = minima_counter;
        }
    }

    free(acc_buf);
    free(p_a);
    free(p_b);
    free(v_a);
    free(v_b);
}

int python_interface(double* pos_flat, double* vel_flat, double* masses,
                     double* minima_flat, int num_bodies, long steps,
                     double dt, int skip_saving, int minima_capacity,
                     enum integration_alg chosen_integration_alg,
                     enum acceleration_alg chosen_acceleration_alg) {
    /* handle signals */
    signal(SIGINT, exit);

    /* handle options */
    integration_func_ptr integration_func;
    switch (chosen_integration_alg) {
        case FORWARD_EULER:
            integration_func = &forward_euler;
            break;

        case VELOCITY_VERLET:
            integration_func = &velocity_verlet;
            break;

        case EULER_CROMER:
            integration_func = &euler_cromer;
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

    long i;

    vec** p = malloc(sizeof(vec*)*(steps+1));
    vec** v = malloc(sizeof(vec*)*(steps+1));
    for (i = 0; i < steps+1; i++) {
        p[i] = p_flat + num_bodies*i;
        v[i] = v_flat + num_bodies*i;
    }

    int perihelion = minima_capacity;
    planet_state *minima = NULL;
    if (perihelion) {
        minima = (planet_state*) minima_flat;
    }

    /* call the right function */
    if (skip_saving) {
        fill_arrays_every_nth_step(p, v, masses, num_bodies, steps, dt,
                                   integration_func, skip_saving,
                                   &perihelion, minima);
    } else {
        fill_arrays(p, v, masses, num_bodies, steps, dt, integration_func);
    }

    free(p);
    free(v);
    return perihelion;
}
