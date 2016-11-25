.PHONY: clean

LATEX=pdflatex
LATEX_OPTS=
report_texdoc=report.tex
report_pdf=report.pdf
bibliography=../papers.bib

clean_latex_ext=*.aux *.bbl *.blg *.log *.out

diffusion_lib_dir=src/c
diffusion_lib_file=src/c/libdiffuse.so

all: report diffusion_lib

$(diffusion_lib_file): diffusion_lib
diffusion_lib:
	$(MAKE) -C $(diffusion_lib_dir)

# report stuff
continuous:
	latexmk ${LATEX_OPTS} -pdf -pvc ${report_texdoc}

report: $(report_pdf)
#$(report_pdf): $(report_texdoc) $(plots) $(tables) $(benchmarks)
$(report_pdf): $(report_texdoc) $(bibliography)# $(plots) $(tables)
	# need to run several times to fix references
	$(LATEX) $(LATEX_OPTS) $(report_texdoc)
	bibtex report
	$(LATEX) $(LATEX_OPTS) $(report_texdoc)
	$(LATEX) $(LATEX_OPTS) $(report_texdoc)
#reference_test: diffusion_lib
#	python src/something

show: report
	evince $(report_pdf) &
#test: $(test_programs) #$(diffusion_lib_file)
#	pytest $(pytest_opts) $(test_programs)

clean-all: clean clean-plots
clean: clean-c clean-python clean-latex
clean-c:
	$(MAKE) clean -C $(diffusion_lib_dir)
clean-python:
	$(RM) src/*.pyc
	$(RM) -r __pycache__
clean-latex:
	$(RM) $(clean_latex_ext)
clean-plots:
	$(RM) fig/plot*