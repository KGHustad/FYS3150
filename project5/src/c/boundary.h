enum position {TOP, BOTTOM, LEFT, RIGHT};
enum condition_type {DIRICHLET, NEUMANN};

typedef struct {
    enum position pos;
    enum condition_type type;
} boundary_condition;

void update_boundary(double **v, boundary_condition bc, int height,
                       int width);
/*
void update_boundary(double **v, boundary_condition_v bc, int height,
                       int width);
*/
