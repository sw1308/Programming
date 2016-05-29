### MUST BE COMPILED IN UNIX/LINUX ENVIRONMENT ###

OPTS=-O
BINDIR=../../../bin/Tutorials/Tutorial01
TMPFOLDER=$(BINDIR)/tmp
SRC=$(wildcard *.hs)

.DEFAULT_GOAL := default

clean:
	rm -rfv $(BINDIR)/Tutorials

%:
	mkdir -p $(BINDIR)
	mkdir -p $(TMPFOLDER)
	ghc -o $(BINDIR)/tutorial01 -outputdir $(TMPFOLDER) $(OPTS) $@.hs

all: $(basename $(SRC))
	@echo 'Compilation complete for all filenames.'

default: clean all

.PHONY: default clean all
