.PHONY: clean clean-all clean-c clean-latex clean-plots report show solar_system_lib test reference_test

LATEX=pdflatex
LATEX_OPTS=
report_texdoc=report.tex
report_pdf=report.pdf
bibliography=../papers.bib

clean_latex_ext=*.aux *.bbl *.blg *.log *.out

solar_system_lib_dir=src/c
solar_system_lib_file=src/c/solar_system.so

all: report solar_system_lib

#solar_system_lib: $(solar_system_lib_file)
#$(solar_system_lib_file):
$(solar_system_lib_file): solar_system_lib
solar_system_lib:
	$(MAKE) -C $(solar_system_lib_dir)

report: $(report_pdf)
$(report_pdf): $(report_texdoc) $(bibliography)# $(plots) $(tables)
	# need to run several times to fix references
	$(LATEX) $(LATEX_OPTS) $(report_texdoc)
	bibtex report
	$(LATEX) $(LATEX_OPTS) $(report_texdoc)
	$(LATEX) $(LATEX_OPTS) $(report_texdoc)
reference_test: solar_system_lib
	python src/EinsteinWasRightAllAlong.py -y 20

show: report
	evince $(report_pdf) &

clean-all: clean clean-plots
clean: clean-c clean-python clean-latex
clean-c:
	$(MAKE) clean -C $(solar_system_lib_dir)
clean-python:
	$(RM) src/*.pyc
	$(RM) -r __pycache__
clean-latex:
	$(RM) $(clean_latex_ext)
clean-plots:
	$(RM) fig/plot*
