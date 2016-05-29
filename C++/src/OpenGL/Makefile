COMPILER=g++
BINDIR=../../bin
INCLUDE=../../include
COMMON=../../common
SRC=$(wildcard *.cpp)
BINFOLDERNAME=GLTutorial
LIBS=-lGL -lGLU -lglut -lGLEW -lpthread
OPTS= -I$(INCLUDE) -I$(COMMON)


ifdef DEBUG
OPTS:=-g
endif

.DEFAULT_GOAL := default

clean:
	@rm -r -f $(BINDIR)
	@echo 'Removed build directory $(BINDIR).'


all: $(SRC)
	@mkdir -p $(BINDIR)/GLTutorial
	@echo 'Created build directory at $(BINDIR)/$(BINFOLDERNAME)'
	$(COMPILER) $(OPTS) -o $(BINDIR)/$(BINFOLDERNAME)/$(BINFOLDERNAME) $(SRC) $(LIBS)
	@echo 'Compilation complete for all filenames.'


default: clean build all

.PHONY: clean build all
