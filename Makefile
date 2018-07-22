PYTHON=python
LATEX=pdflatex
OUTDIR=output

all: html md pdf pdf-short

html:
	$(PYTHON) build_cv.py --md_template cv_template.html --md_out_file $(OUTDIR)/cv.html

md:
	$(PYTHON) build_cv.py --md_template cv_template.md --md_out_file $(OUTDIR)/cv.md

tex:
	$(PYTHON) build_cv.py --tex_template cv_template.tex --tex_out_file $(OUTDIR)/cv.tex

tex-short:
	$(PYTHON) build_cv.py --tex_template cv_template.proposal.tex --tex_out_file $(OUTDIR)/cv.short.tex

pdf: tex
	cd $(OUTDIR)
	$(LATEX) $(OUTDIR)/cv.tex
	cd ..

pdf-short: tex-short
	cd $(OUTDIR)
	$(LATEX) $(OUTDIR)/cv.short.tex
	cd ..

clean:
	rm $(OUTDIR)/*