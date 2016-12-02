.PHONY: clean MPI

CC=cc
CC_FLAGS = -Wall -O3 -std=gnu89 -fpic -march=native
LDFLAGS= -lm
LDFLAGS += -fopenmp
diffuse_sources = boundary.c common.c diffuse_1d.c diffuse_2d.c tridiagonal.c
diffuse_sources_omp = diffuse_2d_omp.c
diffuse_sources_mpi = diffuse_2d_mpi.c
diffuse_headers = boundary.h common.h tridiagonal.h
diffuse_headers_omp =
diffuse_headers_mpi =
diffuse_object_files = boundary.o common.o diffuse_1d.o diffuse_2d.o tridiagonal.o
diffuse_object_files_omp = diffuse_2d_omp.o
diffuse_object_files_mpi = diffuse_2d_mpi.o
diffuse_lib = libdiffuse.so

LDFLAGS += -fopenmp
diffuse_sources += $(diffuse_sources_omp)
diffuse_headers += $(diffuse_headers_omp)
diffuse_object_files += $(diffuse_object_files_omp)

all: $(diffuse_lib)

#OMP: LDFLAGS += -fopenmp
#OMP: diffuse_sources += $(diffuse_sources_omp)
#OMP: diffuse_headers += $(diffuse_headers_omp)
#OMP: diffuse_object_files += $(diffuse_object_files_omp)
#OMP: all

MPI: CC=mpicc
MPI: diffuse_sources += $(diffuse_sources_mpi)
MPI: diffuse_headers += $(diffuse_headers_mpi)
MPI: diffuse_object_files += $(diffuse_object_files_mpi)
MPI: all

$(diffuse_lib): $(diffuse_object_files)
	$(CC) -shared -Wl,-soname,diffuse -o $(diffuse_lib) $(diffuse_object_files) $(LDFLAGS)
$(diffuse_object_files): $(diffuse_headers) $(diffuse_sources)
	$(CC) $(CC_FLAGS) $(diffuse_sources) -c $(LDFLAGS)

clean:
	$(RM) $(diffuse_object_files) $(diffuse_lib) test.o
