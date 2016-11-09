
CC_FLAGS = -Wall -O3 -std=gnu89 -fpic -march=native
LDFLAGS= -lm -lgsl
ising_sources = ising.c lattice.c random.c
ising_headers = ising.h lattice.h random.h
ising_object_files = ising.o
ising_lib = libising.so

all: $(ising_lib)

$(ising_lib): $(ising_object_files)
	$(CC) -shared -Wl,-soname,ising -o $(ising_lib) $(ising_object_files)
$(ising_object_files): $(ising_headers) $(ising_sources)
	$(CC) $(CC_FLAGS) $(ising_sources) -c $(LDFLAGS)
#test.o: test.c $(ising_object_files)
#	$(CC) -Wall -std=gnu89 -o test.o test.c ising.o -lm
#valgrind: test.o
#	valgrind --track-origins=yes ./test.o
clean:
	$(RM) $(ising_object_files) $(ising_lib) test.o
