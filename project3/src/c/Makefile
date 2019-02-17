
CFLAGS = -Wall -O3 -ffast-math -std=gnu89 -fpic -march=native
LD_FLAGS = -lm

SONAME = -soname
ifeq ($(shell uname -s),Darwin)
    SONAME = -install_name
endif

solar_system_sources = solar_system.c
solar_system_headers = solar_system.h
solar_system_object_files = solar_system.o
solar_system_lib = libsolarsystem.so

test_executable = test.x

all: $(solar_system_lib)

$(solar_system_lib): $(solar_system_object_files)
	$(CC) -shared -Wl,$(SONAME),solarsystem -o $(solar_system_lib) $(solar_system_object_files) $(LD_FLAGS)
$(solar_system_object_files): $(solar_system_headers) $(solar_system_sources)
	$(CC) $(CFLAGS) $(solar_system_sources) -c
$(test_executable): test.c $(solar_system_object_files)
	$(CC) -Wall -std=gnu89 -o $@ $^ -lm
valgrind: $(test_executable)
	valgrind --track-origins=yes ./$<
clean:
	$(RM) $(solar_system_object_files) $(solar_system_lib) $(test_executable)
