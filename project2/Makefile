LATEX=pdflatex
LATEX_OPTS=
report_texdoc=report.tex
report_pdf=report.pdf
bibliography=../papers.bib

#benchmarks=bench_all.dat
#benchmark_programs=src/bench_all.py
#PLOT_OPTS=--dont_show
#plot_programs=src/plot_exact.py src/task_b.py
#plots = fig/plot_exact.pdf fig/plot_b.pdf

#table_programs=src/task_d.py
#tables = table_errors.dat

all: report

report: $(report_pdf)
#$(report_pdf): $(report_texdoc) $(plots) $(tables) $(benchmarks)
$(report_pdf): $(report_texdoc) $(bibliography)
	# need to run several times to fix references
	$(LATEX) $(LATEX_OPTS) $(report_texdoc)
	bibtex report
	$(LATEX) $(LATEX_OPTS) $(report_texdoc)
	$(LATEX) $(LATEX_OPTS) $(report_texdoc)
# benchmarks: $(benchmarks) $(benchmark_programs)
# $(benchmarks):
# 	python src/bench_all.py > bench_all.dat
# plots: $(plots)
# $(plots): $(plot_programs)
# 	for plot_prog in $(plot_programs); do \
# 		python $$plot_prog $(PLOT_OPTS) ; \
# 	done
# tables: $(tables)
# $(tables): $(table_programs)
# 	for table_prog in $(table_programs); do \
# 		python $$table_prog ; \
# 	done
show: report
	evince $(report_pdf) &
