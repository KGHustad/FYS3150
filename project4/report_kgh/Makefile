.PHONY: clean clean-latex continuous report show libising tables plots

PROJ_DIR=..
DATA_DIR=$(PROJ_DIR)/data
FIG_DIR=$(PROJ_DIR)/fig
PY_SRC_DIR=$(PROJ_DIR)/src
LIB_FOLDER=$(PROJ_DIR)/src/c
LIB_FILE=$(LIB_FOLDER)/libising.so

LATEX=pdflatex
LATEX_OPTS=
report_basename=report_kgh
report_texdoc=${report_basename}.tex
report_pdf=${report_basename}.pdf
bibliography=../../papers.bib

tables=table_b.tex
plots_c=$(FIG_DIR)/plot_c_energy_homogeneous_T=2.4_sweeps=1E+06.pdf $(FIG_DIR)/plot_c_energy_random_T=2.4_sweeps=1E+06.pdf

plots_e=$(FIG_DIR)/plot_e_dT=0.001_sweeps=2E+06_specific_heat.pdf

datafiles_e=$(DATA_DIR)/task_e_dT=0.001_sweeps=2E+06_2016-11-15--18-13-00.dat

clean_latex_ext=*.aux *.bbl *.blg *.log *.out

all: report
continuous:
	latexmk ${LATEX_OPTS} -pdf -pvc ${report_texdoc}
report: $(report_pdf) $(tables) plots
$(report_pdf): $(report_texdoc) $(bibliography)
	# need to run several times to fix references
	$(LATEX) $(LATEX_OPTS) $(report_texdoc)
	bibtex $(report_basename)
	$(LATEX) $(LATEX_OPTS) $(report_texdoc)
	$(LATEX) $(LATEX_OPTS) $(report_texdoc)

show: report
	evince $(report_pdf) &

plots: $(plots_c) $(plots_e)
tables: $(tables)


libising: $(LIB_FILE)
$(LIB_FILE):
	make -C $(PROJ_DIR) libising

table_b.tex: $(LIB_FILE) $(PY_SRC_DIR)/task_b_table.py
	python $(PY_SRC_DIR)/task_b_table.py --latex --silent --short > table_b.tex

$(plots_c): $(LIB_FILE) $(PY_SRC_DIR)/task_c.py
	python $(PY_SRC_DIR)/task_c.py --no_show

$(plots_e): $(LIB_FILE) $(PY_SRC_DIR)/plot_e_data.py $(datafiles_e)
	python $(PY_SRC_DIR)/plot_e_data.py $(datafiles_e)
clean: clean-latex
clean-latex:
	$(RM) $(clean_latex_ext)
