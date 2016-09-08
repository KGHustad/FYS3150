LATEX=pdflatex
LATEX_OPTS=
report_texdoc=report.tex
report_pdf=report.pdf
programs=task_b.py

plots = fig/plot_b.pdf

all: report

report: $(report_pdf)
$(report_pdf): $(report_texdoc) $(plots)
	# need to run twice to fix cross-references
	$(LATEX) $(LATEX_OPTS) $(report_texdoc)
	$(LATEX) $(LATEX_OPTS) $(report_texdoc)
plots: $(plots)
$(plots): $(programs)
	python task_b.py
