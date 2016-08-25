#include <iostream>
#include <math.h>

double f(double x) {
    return atan(x);
}

double forward_euler_diff(double x, double h) {
    return (f(x + h) - f(x))/h;
}

double central_diff(double x, double h) {
    return (f(x + h) - f(x - h))/(2*h);
}

int main() {
    double exact = 1. / 3;
    double sqrt_2 = sqrt(2);
    for (double h = 1E-2; h > 1E-17; h /= 10) {
        printf("\nh = %g\n", h);
        double fe_approx = forward_euler_diff(sqrt_2, h);
        double fe_err_abs = fe_approx - exact;
        double fe_err_rel = (fe_approx - exact)/exact;
        double ce_approx = central_diff(sqrt_2, h);
        double ce_err_abs = ce_approx - exact;
        double ce_err_rel = (ce_approx - exact)/exact;
        printf("FE:  %8g  %10.2E  %10.2E\n", fe_approx, fe_err_abs, fe_err_rel);
        printf("Ce:  %8g  %10.2E  %10.2E\n", ce_approx, ce_err_abs, ce_err_rel);
    }

}
