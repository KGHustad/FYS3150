.PHONY: clean jacobi_lib

LATEX=pdflatex
LATEX_OPTS=
report_texdoc=report.tex
report_pdf=report.pdf
bibliography=../papers.bib

clean_latex_ext=*.aux *.bbl *.blg *.log *.out

test_programs=src/common.py src/common_accelerated.py
pytest_opts=--doctest-modules --doctest-report=none -v

jacobi_lib=src/c

#benchmarks=bench_all.dat
#benchmark_programs=src/bench_all.py
#PLOT_OPTS=--dont_show
plot_programs=src/plot_d.py
plots = fig/plot_interacting_omega=0.5,1,5_rho-max=5_n=200.pdf fig/plot_interacting_omega=0.005,0.01,0.05_rho-max=70_n=200.pdf

#table_programs=src/task_d.py
#tables = table_errors.dat

all: jacobi_lib report

jacobi_lib:
	$(MAKE) -C $(jacobi_lib)

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
plots: $(plots)
$(plots): $(plot_programs) $(jacobi_lib)
	@mkdir -p $(@D)
	python src/plot_omegas.py -n 200 --omegas 0.5 1 5 --plot
	python src/plot_omegas.py -n 200 --omegas 0.5E-2 1E-2 5E-2 --plot -p 70

# tables: $(tables)
# $(tables): $(table_programs)
# 	for table_prog in $(table_programs); do \
# 		python $$table_prog ; \
# 	done
show: report
	evince $(report_pdf) &
test: $(test_programs)
	pytest $(pytest_opts) $(test_programs)

clean: clean-c clean-python clean-latex
clean-c:
	$(MAKE) clean -C $(jacobi_lib)
clean-python:
	$(RM) src/*.pyc
clean-latex:
	$(RM) $(clean_latex_ext)
