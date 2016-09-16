LATEX=pdflatex
options=
#options="-interaction=batchmode"
texdoc=report.tex

$LATEX $options $texdoc
$LATEX $options $texdoc
# need to run twice to fix cross-references
