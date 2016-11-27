#.PHONY: $(projects) dependencies
.PHONY: project1 project2 project3 project4 project5 dependencies

projects = project1 project2 project3 project4 #project5

all: $(projects)
project1:
	$(MAKE) -C project1
project2:
	$(MAKE) -C project2
project3:
	$(MAKE) -C project3
project4:
	$(MAKE) -C project4
project5:
	$(MAKE) -C project5

dependencies:
	$(MAKE) -C dependencies
