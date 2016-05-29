### MUST BE COMPILED IN UNIX/LINUX ENVIRONMENT ###

BINDIR=../../bin
OPTS=-d $(BINDIR)

SRCDIR=./
SRCFILES=$(shell find $(SRCDIR) -name "*.java")

.DEFAULT_GOAL := default

clean:
	rm -rfv $(BINDIR)/PhysicsSystem
ifeq ($(ls -A $(BINDIR)),)
	rm -rfv $(BINDIR)
endif

all:
	mkdir -p $(BINDIR)
	mkdir -p $(BINDIR)/PhysicsSystem

	cp settings.sh $(BINDIR)/PhysicsSystem/.

	javac $(OPTS) $(SRCFILES)

default: clean all
