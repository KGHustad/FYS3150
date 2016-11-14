.PHONY: all report clean	# PHONY targets are not files

all: Report.pdf    #reference to pdf-file
report: Report.pdf # this is just another name for the same thing
Report.pdf: Report.tex cites.bib    #depedency files
	latexmk -pdf Report    #compiling
show: Report.pdf    #shows pdf-file
	evince Report.pdf &    #evince = pdf-reader
clean:
	latexmk -c    #
	$(RM) *.bbl *.run.xml    #
