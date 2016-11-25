.PHONY: clean

MPICC=mpicc
CC_FLAGS = -Wall -O3 -std=gnu89 -fpic -march=native
LDFLAGS= -lm
diffuse_sources = common.c diffuse_2d.c
diffuse_headers = common.h
diffuse_object_files = common.o diffuse_2d.o
diffuse_lib = libdiffuse.so

bench_random = bench_random.o

all: $(diffuse_lib)

$(diffuse_lib): $(diffuse_object_files)
	$(MPICC) -shared -Wl,-soname,diffuse -o $(diffuse_lib) $(diffuse_object_files) $(LDFLAGS)
$(diffuse_object_files): $(diffuse_headers) $(diffuse_sources)
	$(MPICC) $(CC_FLAGS) $(diffuse_sources) -c $(LDFLAGS)

clean:
	$(RM) $(diffuse_object_files) $(diffuse_lib) test.o
