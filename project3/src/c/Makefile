
CC_FLAGS = -Wall -O3 -std=gnu89 -fpic -lm -march=native

SONAME = -soname
ifeq ($(shell uname -s),Darwin)
    SONAME = -install_name
endif

solar_system_sources = solar_system.c
solar_system_headers = solar_system.h
solar_system_object_files = solar_system.o
solar_system_lib = libsolarsystem.so

all: $(solar_system_lib)

$(solar_system_lib): $(solar_system_object_files)
	$(CC) -shared -Wl,$(SONAME),solarsystem -o $(solar_system_lib) $(solar_system_object_files)
$(solar_system_object_files): $(solar_system_headers) $(solar_system_sources)
	$(CC) $(CC_FLAGS) $(solar_system_sources) -c
test.o: test.c $(solar_system_object_files)
	$(CC) -Wall -std=gnu89 -o test.o test.c solar_system.o -lm
valgrind: test.o
	valgrind --track-origins=yes ./test.o
clean:
	$(RM) $(solar_system_object_files) $(solar_system_lib) test.o
