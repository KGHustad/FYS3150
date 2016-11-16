.PHONY: clean clean-latex continuous report show

PROJ_DIR=..
PY_SRC_DIR=$(PROJ_DIR)/src

LATEX=pdflatex
LATEX_OPTS=
report_basename=report_kgh
report_texdoc=${report_basename}.tex
report_pdf=${report_basename}.pdf
bibliography=../../papers.bib

tables=table_b.tex

clean_latex_ext=*.aux *.bbl *.blg *.log *.out

all: report
continuous:
	latexmk ${LATEX_OPTS} -pdf -pvc ${report_texdoc}
report: $(report_pdf) $(tables)
$(report_pdf): $(report_texdoc) $(bibliography)
	# need to run several times to fix references
	$(LATEX) $(LATEX_OPTS) $(report_texdoc)
	bibtex $(report_basename)
	$(LATEX) $(LATEX_OPTS) $(report_texdoc)
	$(LATEX) $(LATEX_OPTS) $(report_texdoc)

show: report
	evince $(report_pdf) &

table_b.tex: $(PY_SRC_DIR)/task_b_table.py
	python $(PY_SRC_DIR)/task_b_table.py --latex --silent --short > table_b.tex

clean: clean-latex
clean-latex:
	$(RM) $(clean_latex_ext)
