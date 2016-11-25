all: report.pdf
report.pdf: report.tex cites.bib
	latexmk -pdf report
show: report.pdf
	evince report.pdf &    #evince = pdf-reader
clean:
	latexmk -c
	rm *.bbl *.run.xml
