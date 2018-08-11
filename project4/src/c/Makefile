.PHONY: clean bench_ising bench_random run-benchmark

CC_FLAGS = -Wall -O3 -std=gnu89 -fpic -march=native
CXX_FLAGS = -Wall -O3 -std=gnu++11 -march=native
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
bench_ising_cpp = bench_ising_cpp.x

all: $(ising_lib)

$(ising_lib): $(ising_object_files)
	$(CC) -shared -Wl,$(SONAME),ising -o $(ising_lib) $(ising_object_files) $(LDFLAGS)
%.o: %.c %.h
	$(CC) $(CC_FLAGS) $< -c
%.o: %.cpp
	$(CXX) $(CXX_FLAGS) $< -c
bench_random: $(bench_random)
$(bench_random): random.o bench_random.c
	$(CC) $(CC_FLAGS) -o $@ bench_random.c random.o $(LDFLAGS)
bench_ising: $(bench_ising)
$(bench_ising): $(ising_object_files) bench_ising.c
	$(CC) $(CC_FLAGS) -o $@ bench_ising.c $(ising_object_files) $(LDFLAGS)
$(bench_ising_cpp): bench_ising.cpp ising_cpp.o
	$(CXX) $(CXX_FLAGS) -o $@ $^ -lm
run-benchmark: $(bench_ising)
	time -p ./$(bench_ising)
run-benchmark-cpp: $(bench_ising_cpp)
	time -p ./$(bench_ising_cpp)

clean:
	$(RM) $(wildcard *.o) $(ising_lib) $(bench_random) $(bench_ising) $(bench_ising_cpp) test.o
