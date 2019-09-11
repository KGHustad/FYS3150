.PHONY: clean clean-lib clean-objects clean-executables MPI memtest

SONAME = -soname
ifeq ($(shell uname -s),Darwin)
    SONAME = -install_name
    CC = clang
endif

SHELL=/bin/bash
CFLAGS = -Wall -g -O3 -std=gnu89 #-march=native
#LDFLAGS = -lm
LDLIBS = -lm
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

memtest_sources_1d = memtest_1d.c
memtest_executables_1d = memtest_1d
memtest_sources_2d = memtest_2d.c
memtest_executables_2d = memtest_2d_serial memtest_2d_omp
memtest_executables = $(memtest_executables_1d) $(memtest_executables_2d)
valgrind_memtest_flags = -q

ifeq ($(shell uname -s),Linux)
CFLAGS += -fopenmp
diffuse_sources += $(diffuse_sources_omp)
diffuse_headers += $(diffuse_headers_omp)
diffuse_object_files += $(diffuse_object_files_omp)
endif

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

#$(diffuse_lib): CFLAGS += -fpic
$(diffuse_lib): $(diffuse_object_files)
	$(CC) -shared -Wl,$(SONAME),diffuse -o $(diffuse_lib) $(diffuse_object_files) $(LDFLAGS) $(LDLIBS)
$(diffuse_object_files): $(diffuse_headers) $(diffuse_sources)
	$(CC) $(CFLAGS) -fpic $(diffuse_sources) -c

memtest: $(memtest_executables)
	valgrind $(valgrind_memtest_flags) ./memtest_1d
	valgrind $(valgrind_memtest_flags) ./memtest_2d_serial
	valgrind $(valgrind_memtest_flags) ./memtest_2d_omp
#$(memtest_executables): $(diffuse_object_files)
memtest_1d: common.o tridiagonal.o diffuse_1d.o diffuse_1d.h
memtest_2d_serial: common.o boundary.o diffuse_2d.o diffuse_2d.h
memtest_2d_omp: common.o boundary.o diffuse_2d_omp.o diffuse_2d_omp.h

clean: clean-lib clean-objects clean-executables
clean-lib:
	$(RM) $(diffuse_lib)
clean-objects:
	$(RM) $(diffuse_object_files)
clean-executables:
	$(RM) $(memtest_executables)
