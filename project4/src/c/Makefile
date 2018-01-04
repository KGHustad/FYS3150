.PHONY: clean bench_ising bench_random

CC_FLAGS = -Wall -O3 -std=gnu89 -fpic -march=native
#LDFLAGS= -lm -lgsl -lcblas -latlas
LDFLAGS= -lm -lgsl -lgslcblas
SONAME = -soname
ifeq ($(shell uname -s),Darwin)
    SONAME = -install_name
endif

ising_sources = ising.c lattice.c random.c
ising_headers = ising.h lattice.h random.h
ising_object_files = ising.o lattice.o random.o
ising_lib = libising.so

benchmarks = $(bench_random) $(bench_ising)
bench_random = bench_random.x
bench_ising = bench_ising.x

all: $(ising_lib)

$(ising_lib): $(ising_object_files)
	$(CC) -shared -Wl,$(SONAME),ising -o $(ising_lib) $(ising_object_files) $(LDFLAGS)
$(ising_object_files): $(ising_headers) $(ising_sources)
	$(CC) $(CC_FLAGS) $(ising_sources) -c $(LDFLAGS)
bench_random: $(bench_random)
$(bench_random): random.o bench_random.c
	$(CC) $(CC_FLAGS) bench_random.c random.o -o $(bench_random) $(LDFLAGS)
bench_ising: $(bench_ising)
$(bench_ising): $(ising_object_files) bench_ising.c
	$(CC) $(CC_FLAGS) bench_ising.c $(ising_object_files) -o $(bench_ising) $(LDFLAGS)

clean:
	$(RM) $(ising_object_files) $(ising_lib) $(bench_random) $(bench_ising) test.o
