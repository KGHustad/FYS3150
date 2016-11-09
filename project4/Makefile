.PHONY: clean clean-all clean-c clean-python clean-latex clean-plots libising report_kgh show_kgh clean_kgh

LATEX=pdflatex
LATEX_OPTS=

report_kgh_dir=report_kgh

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
