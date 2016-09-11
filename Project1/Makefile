LATEX=pdflatex
LATEX_OPTS=
report_texdoc=report.tex
report_pdf=report.pdf
PLOT_OPTS=--dont_show
plot_programs=plot_exact.py task_b.py

plots = fig/plot_exact.pdf fig/plot_b.pdf

all: report

report: $(report_pdf)
$(report_pdf): $(report_texdoc) $(plots)
	# need to run several times to fix references
	$(LATEX) $(LATEX_OPTS) $(report_texdoc)
	bibtex report
	$(LATEX) $(LATEX_OPTS) $(report_texdoc)
	$(LATEX) $(LATEX_OPTS) $(report_texdoc)
plots: $(plots)
$(plots): $(plot_programs)
	for plot_prog in $(plot_programs); do \
		python $$plot_prog $(PLOT_OPTS) ; \
	done
show: report
	evince $(report_pdf) &
