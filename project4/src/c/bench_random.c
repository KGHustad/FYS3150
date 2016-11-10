#include <stdio.h>
#include <time.h>
#include "random.h"

int main(int argc, char *argv[]) {
    int i;
    clock_t pre, post;
    double time_spent;

    int N = (int) 1E6;
    if (argc > 1) {
        N = (int) atof(argv[1]);
    }

    gsl_rng *r = initialize_rng();

    printf("Generating %d random doubles in [0, 1)...\n", N);
    pre = clock();
    for (i = 0; i < N; i++) {
        gsl_rng_uniform(r);
    }
    post = clock();
    time_spent = (post-pre)*1./CLOCKS_PER_SEC;
    printf("Time spent: %g seconds (%g doubles/sec)\n",
           time_spent, N/time_spent);

    int end_interval = 40;
    printf("Generating %d random ints in [0, %d)...\n", N, end_interval);
    pre = clock();
    for (i = 0; i < N; i++) {
        gsl_rng_uniform_int(r, end_interval);
    }
    post = clock();
    time_spent = (post-pre)*1./CLOCKS_PER_SEC;
    printf("Time spent: %g seconds (%g ints/sec)\n",
           time_spent, N/time_spent);


    destroy_rng(r);
    return 0;
}
