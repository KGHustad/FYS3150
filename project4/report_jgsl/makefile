all: Report.pdf    #reference to pdf-file
Report.pdf: Report.tex cites.bib    #depedency files
	latexmk -pdf Report    #compiling
show: Report.pdf    #shows pdf-file
	evince Report.pdf &    #evince = pdf-reader
clean:
	latexmk -c    #
	rm *.bbl *.run.xml    #
