
CC_FLAGS = -Wall -O2 -fpic -lm -march=native

SONAME = -soname
ifeq ($(shell uname -s),Darwin)
    SONAME = -install_name
endif

jacobi_sources = jacobi.c
jacobi_headers = jacobi.h
jacobi_object_files = jacobi.o
jacobi_lib = jacobi.so

all: $(jacobi_lib)

$(jacobi_lib): $(jacobi_object_files)
	$(CC) -shared -Wl,$(SONAME),jacobi -o $(jacobi_lib) $(jacobi_object_files)
$(jacobi_object_files): $(jacobi_headers) $(jacobi_sources)
	$(CC) $(CC_FLAGS) $(jacobi_sources) -c


clean:
	$(RM) $(jacobi_object_files) $(jacobi_lib)
