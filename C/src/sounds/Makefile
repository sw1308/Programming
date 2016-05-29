### MUST BE COMPILED IN UNIX/LINUX ENVIRONMENT ###

LIBS=-lm
OPTS=-I.
BINDIR=../../bin
CFILES=song1.c

.DEFAULT_GOAL := default

clean:
	rm -rfv $(BINDIR)/sounds
ifeq ($(ls -A $(BINDIR)),)
	rm -rfv $(BINDIR)
endif

all:
	mkdir -p $(BINDIR)/sounds
	cp song1.sh $(BINDIR)/sounds/.
	gcc $(CFILES) -o $(BINDIR)/sounds/song1 $(LIBS) $(OPTS)

default: clean all
