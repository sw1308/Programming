### MUST BE COMPILED IN UNIX/LINUX ENVIRONMENT ###

OPTS=-O
BINDIR=../../bin
SRC=$(wildcard *.hs)

.DEFAULT_GOAL := default

clean:
	rm -rfv $(BINDIR)/Tutorials

%:
	mkdir -p $(BINDIR)/Tutorials
	ghc -o $(BINDIR)/Tutorials $(OPTS) $@.hs

all: $(basename $(SRC))
	@echo 'Compilation complete for all filenames.'

default: clean all

.PHONY: default clean all
