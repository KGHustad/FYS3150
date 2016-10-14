#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include "solar_system.h"

const double G = 4*M_PI*M_PI;

void acceleration(coor* pos, double* masses, int target_body, int num_bodies,
                  coor* acc_ptr, double dt) {
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

void forward_euler(coor* pos, coor* vel,
                   coor* pos_new, coor* vel_new, coor* acc_buf,
                   double* masses, double dt, int num_bodies) {
    coor acc;
    int i;
    for (i = 0; i < num_bodies; i++) {
        acceleration(pos, masses, i, num_bodies, &acc, dt);
        vel_new[i].x = vel[i].x + acc.x;
        vel_new[i].y = vel[i].y + acc.y;
        pos_new[i].x = pos[i].x + vel[i].x*dt;
        pos_new[i].y = pos[i].y + vel[i].y*dt;
    }
}

void velocity_verlet(coor* pos, coor* vel,
                     coor* pos_new, coor* vel_new, coor* acc_buf,
                     double* masses, double dt, int num_bodies) {
    coor acc_new;

    int i;
    double dt_sq = dt*dt;
    for (i = 0; i < num_bodies; i++) {
        acceleration(pos, masses, i, num_bodies, acc_buf+i, dt);
        pos_new[i].x = pos[i].x + vel[i].x*dt + 0.5*dt_sq*acc_buf[i].x;
        pos_new[i].y = pos[i].y + vel[i].y*dt + 0.5*dt_sq*acc_buf[i].y;
    }
    for (i = 0; i < num_bodies; i++) {
        acceleration(pos_new, masses, i, num_bodies, &acc_new, dt);
        vel_new[i].x = vel[i].x + 0.5*(acc_buf[i].x + acc_new.x)*dt;
        vel_new[i].y = vel[i].y + 0.5*(acc_buf[i].y + acc_new.y)*dt;
    }
}


void fill_arrays(coor** p, coor** v, double* masses,
                 int num_bodies, int steps, double dt) {
    int i;
    coor* acc_buf = malloc(sizeof(coor)*num_bodies);
    for (i = 0; i < steps; i++) {
        velocity_verlet(p[i], v[i], p[i+1], v[i+1], acc_buf, masses, dt,
                        num_bodies);
    }
    free(acc_buf);
}

void solve(double* pos_flat, double* vel_flat, double* masses,
           int num_bodies, int steps, double dt) {
    /* setup arrays */
    coor* p_flat = (coor*) pos_flat;
    coor* v_flat = (coor*) vel_flat;

    int i;

    coor** p = malloc(sizeof(coor*)*steps+1);
    coor** v = malloc(sizeof(coor*)*steps+1);
    for (i = 0; i < steps+1; i++) {
        p[i] = p_flat + num_bodies*i;
        v[i] = v_flat + num_bodies*i;
    }

    fill_arrays(p, v, masses, num_bodies, steps, dt);

    free(p);
    free(v);
}
