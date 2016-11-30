.PHONY: clean MPI

CC=cc
CC_FLAGS = -Wall -O3 -std=gnu89 -fpic -march=native
LDFLAGS= -lm
diffuse_sources = boundary.c common.c diffuse_2d.c
diffuse_sources_mpi = diffuse_2d_mpi.c
diffuse_headers = boundary.h common.h
diffuse_headers_mpi =
diffuse_object_files = boundary.o common.o diffuse_2d.o
diffuse_object_files_mpi = diffuse_2d_mpi.o
diffuse_lib = libdiffuse.so

bench_random = bench_random.o

all: $(diffuse_lib)

MPI: CC=mpicc
MPI: diffuse_sources += $(diffuse_sources_mpi)
MPI: diffuse_headers += $(diffuse_headers_mpi)
MPI: diffuse_object_files += $(diffuse_object_files_mpi)
MPI: $(diffuse_lib)

$(diffuse_lib): $(diffuse_object_files)
	$(CC) -shared -Wl,-soname,diffuse -o $(diffuse_lib) $(diffuse_object_files) $(LDFLAGS)
$(diffuse_object_files): $(diffuse_headers) $(diffuse_sources)
	$(CC) $(CC_FLAGS) $(diffuse_sources) -c $(LDFLAGS)

clean:
	$(RM) $(diffuse_object_files) $(diffuse_lib) test.o
