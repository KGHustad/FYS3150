.PHONY: clean clean-all clean-c clean-python clean-latex clean-plots libising report_kgh show_kgh clean_kgh

PY_SRC_DIR=.

LATEX=pdflatex
LATEX_OPTS=

report_kgh_dir=report_kgh
report_jgsl_dir=report_jgsl

bibliography=../papers.bib

clean_latex_ext=*.aux *.bbl *.blg *.log *.out

# test_programs=src/common.py
# pytest_opts=--doctest-modules --doctest-report=none -v
#
libising_dir=src/c


all: libising


libising:
	$(MAKE) -C $(libising_dir)

# kgh's report in separate directory
report_kgh:
	$(MAKE) -C $(report_kgh_dir)
show_kgh: report_kgh
	$(MAKE) -C $(report_kgh_dir) show
clean_kgh:
	$(MAKE) -C $(report_kgh_dir) clean

# jgsl's report in separate directory
report_jgsl:
	$(MAKE) -C $(report_jgsl_dir)
show_jgsl: report_kgh
	$(MAKE) -C $(report_jgsl_dir) show
clean_jgsl:
	$(MAKE) -C $(report_jgsl_dir) clean

reference_test: libising
	python $(PY_SRC_DIR)/task_b_table.py

#test: $(test_programs) #$(libising_file)
#	pytest $(pytest_opts) $(test_programs)

clean-all: clean clean-plots
clean: clean-c clean-python clean-latex
clean-c:
	$(MAKE) clean -C $(libising_dir)
clean-python:
	$(RM) src/*.pyc
	$(RM) -r __pycache__
clean-latex:
	$(RM) $(clean_latex_ext)
clean-plots:
	$(RM) fig/plot*
