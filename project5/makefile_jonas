all: report.pdf
report.pdf: report.tex
	latexmk -pdf report
show: report.pdf
	evince report.pdf &
clean:
	latexmk -c
	rm *.bbl *.run.xml
