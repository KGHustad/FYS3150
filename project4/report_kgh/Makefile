.PHONY: clean clean-latex continuous report show

LATEX=pdflatex
LATEX_OPTS=
report_basename=report_kgh
report_texdoc=${report_basename}.tex
report_pdf=${report_basename}.pdf
bibliography=../../papers.bib

clean_latex_ext=*.aux *.bbl *.blg *.log *.out

all: report
continuous:
	latexmk ${LATEX_OPTS} -pdf -pvc ${report_texdoc}
report: $(report_pdf)
$(report_pdf): $(report_texdoc) $(bibliography)
	# need to run several times to fix references
	$(LATEX) $(LATEX_OPTS) $(report_texdoc)
	bibtex $(report_basename)
	$(LATEX) $(LATEX_OPTS) $(report_texdoc)
	$(LATEX) $(LATEX_OPTS) $(report_texdoc)

show: report
	evince $(report_pdf) &

clean: clean-latex
clean-latex:
	$(RM) $(clean_latex_ext)
