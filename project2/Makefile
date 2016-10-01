.PHONY: clean jacobi_lib

LATEX=pdflatex
LATEX_OPTS=
report_texdoc=report.tex
report_pdf=report.pdf
bibliography=../papers.bib

clean_latex_ext=*.aux *.bbl *.blg *.log *.out

test_programs=src/common.py
pytest_opts=--doctest-modules --doctest-report=none -v

jacobi_lib_dir=src/c
jacobi_lib_file=src/c/jacobi.so

#benchmarks=bench_all.dat
#benchmark_programs=src/bench_all.py
util_programs=src/common.py
plot_programs=src/plot_b.py src/plot_d.py
plots = fig/plot_3-lowest_interacting_omega=1_rho-max=5_n=200.pdf fig/plot_3-lowest_non-interacting_omega=1_rho-max=5_n=200.pdf fig/plot_varying-omega_interacting_omega=0.005,0.01,0.05_rho-max=70_n=100.pdf fig/plot_varying-omega_interacting_omega=0.5,1,5_rho-max=5_n=100.pdf fig/plot_varying-omega_non-interacting_omega=0.005,0.01,0.05_rho-max=70_n=100.pdf fig/plot_varying-omega_non-interacting_omega=0.5,1,5_rho-max=5_n=100.pdf

fig/plot_interacting_omega=0.5,1,5_rho-max=5_n=200.pdf fig/plot_interacting_omega=0.005,0.01,0.05_rho-max=70_n=200.pdf

#table_programs=src/task_d.py
#tables = table_errors.dat

all: jacobi_lib report

jacobi_lib: $(jacobi_lib_file)
$(jacobi_lib_file):
	$(MAKE) -C $(jacobi_lib_dir)

report: $(report_pdf)
#$(report_pdf): $(report_texdoc) $(plots) $(tables) $(benchmarks)
$(report_pdf): $(report_texdoc) $(bibliography) $(plots)
	# need to run several times to fix references
	$(LATEX) $(LATEX_OPTS) $(report_texdoc)
	bibtex report
	$(LATEX) $(LATEX_OPTS) $(report_texdoc)
	$(LATEX) $(LATEX_OPTS) $(report_texdoc)
# benchmarks: $(benchmarks) $(benchmark_programs)
# $(benchmarks):
# 	python src/bench_all.py > bench_all.dat
plots: $(plots)
$(plots): $(plot_programs) $(jacobi_lib_file) $(util_programs)
	@mkdir -p $(@D)
	for plot_prog in $(plot_programs); do \
		python $$plot_prog ; \
	done

# tables: $(tables)
# $(tables): $(table_programs)
# 	for table_prog in $(table_programs); do \
# 		python $$table_prog ; \
# 	done
show: report
	evince $(report_pdf) &
test: $(test_programs) $(jacobi_lib_file)
	pytest $(pytest_opts) $(test_programs)

clean-all: clean clean-plots
clean: clean-c clean-python clean-latex
clean-c:
	$(MAKE) clean -C $(jacobi_lib_dir)
clean-python:
	$(RM) src/*.pyc
clean-latex:
	$(RM) $(clean_latex_ext)
clean-plots:
	$(RM) fig/plot*
