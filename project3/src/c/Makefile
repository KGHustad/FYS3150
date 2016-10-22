
CC_FLAGS = -Wall -O3 -std=gnu89 -fpic -lm -march=native

solar_system_sources = solar_system.c
solar_system_headers = solar_system.h
solar_system_object_files = solar_system.o
solar_system_lib = solar_system_lib.so

all: $(solar_system_lib)

$(solar_system_lib): $(solar_system_object_files)
	$(CC) -shared -o $(solar_system_lib) $(solar_system_object_files)
$(solar_system_object_files): $(solar_system_headers) $(solar_system_sources)
	$(CC) $(CC_FLAGS) $(solar_system_sources) -c


clean:
	$(RM) $(solar_system_object_files) $(solar_system_lib)
