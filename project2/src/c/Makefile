
CFLAGS = -Wall -O2 -fpic -march=native
LDLIBS = -lm

SONAME = -soname
ifeq ($(shell uname -s),Darwin)
    SONAME = -install_name
endif

jacobi_sources = jacobi.c
jacobi_headers = jacobi.h
jacobi_object_files = jacobi.o
jacobi_lib = libjacobi.so

all: $(jacobi_lib)

$(jacobi_lib): $(jacobi_object_files)
	$(CC) -shared -Wl,$(SONAME),jacobi -o $@ $^ $(LDFLAGS) $(LDLIBS)
#$(jacobi_object_files): $(jacobi_headers) $(jacobi_sources)
#	$(CC) $(CFLAGS) $(jacobi_sources) -c


clean:
	$(RM) $(jacobi_object_files) $(jacobi_lib)
