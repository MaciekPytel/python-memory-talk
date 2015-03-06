CMD=pdflatex

.PHONY: all pdf clean
SHELL=/bin/bash

all: slides_pl.pdf slides_en.pdf

pdf: slides_pl.pdf slides_en.pdf clean_intermediate

clean_intermediate :
	rm -f slides_pl.{aux,dvi,log,nav,out,snm,toc,vrb}
	rm -f slides_en.{aux,dvi,log,nav,out,snm,toc,vrb}

clean: clean_intermediate
	rm -f slides_pl.pdf slides_en.pdf

slides_pl.pdf: slides_pl.tex
	$(CMD) slides_pl.tex && $(CMD) slides_pl.tex

slides_en.pdf: slides_en.tex
	$(CMD) slides_en.tex && $(CMD) slides_en.tex
