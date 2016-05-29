### MUST BE COMPILED IN UNIX/LINUX ENVIRONMENT ###

LIBS=-lpthread
OPTS=-I.
BINDIR=../../bin
CFILES=threadedPrimes.c controllerThread.c generationThread.c sortThread.c

.DEFAULT_GOAL := default

clean:
	rm -rfv $(BINDIR)/threadedPrimes
ifeq ($(ls -A $(BINDIR)),)
	rm -rfv $(BINDIR)
endif

all:
	mkdir -p $(BINDIR)/threadedPrimes
	gcc $(CFILES) -o $(BINDIR)/threadedPrimes/threadedPrimes $(LIBS) $(OPTS)

default: clean all
