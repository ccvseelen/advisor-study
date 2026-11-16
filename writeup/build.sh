#!/bin/sh
# Build the PDF from WRITEUP.md (needs pandoc and xelatex)
pandoc WRITEUP.md -o WRITEUP.pdf --pdf-engine=xelatex -V fontsize=10pt -V geometry:margin=1.9cm -V colorlinks=true \
  -V header-includes='\usepackage{float}\floatplacement{figure}{H}\usepackage{etoolbox}\AtBeginEnvironment{longtable}{\small}'
