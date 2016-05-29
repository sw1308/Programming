### MUST BE COMPILED IN UNIX/LINUX ENVIRONMENT ###

OPTS=-O -v
BINDIR=../bin
SRC=$(wildcard *.hs)

.DEFAULT_GOAL := default

clean:
	rm -rfv $(BINDIR)

all:
	mkdir -p $(BINDIR)
	ghc -o $(BINDIR)/PrimeGenerator $(OPTS) $(HFILES)

default: clean all

.PHONY: all clean default
