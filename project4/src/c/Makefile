
CC_FLAGS = -Wall -O3 -std=gnu89 -fpic -lm -march=native

ising_sources = ising.c
ising_headers = ising.h
ising_object_files = ising.o
ising_lib = libising.so

all: $(ising_lib)

$(ising_lib): $(ising_object_files)
	$(CC) -shared -Wl,-soname,solarsystem -o $(ising_lib) $(ising_object_files)
$(ising_object_files): $(ising_headers) $(ising_sources)
	$(CC) $(CC_FLAGS) $(ising_sources) -c
#test.o: test.c $(ising_object_files)
#	$(CC) -Wall -std=gnu89 -o test.o test.c ising.o -lm
#valgrind: test.o
#	valgrind --track-origins=yes ./test.o
clean:
	$(RM) $(ising_object_files) $(ising_lib) test.o
