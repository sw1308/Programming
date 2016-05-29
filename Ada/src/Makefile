COMPILER=gnat make
BINDIR=../bin
SRC=$(wildcard *.adb)

.DEFAULT_GOAL := default

clean:
	@rm -rfv $(BINDIR)
	@echo 'Removed build directory $(BINDIR).'

%:
	mkdir -p $(BINDIR)/$@
	echo 'Created build directory at $(BINDIR)/$@.'
	$(COMPILER) -v -D $(BINDIR)/$< -o $(BINDIR)/$@/$@ $@.adb
	echo 'Compiled $@'

all: $(basename $(SRC))
	@echo 'Compilation complete for all filenames.'

default: clean build all

.PHONY: clean build all
