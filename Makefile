### MUST BE COMPILED IN UNIX/LINUX ENVIRONMENT ###

PROJECT_DIRS:=$(dir $(shell find ./*/ -name 'Makefile'))

.DEFAULT_GOAL := default
.PHONY: all $(PROJECT_DIRS)

all: TYPE = 'all'
all: $(PROJECT_DIRS)

clean: TYPE = 'clean'
clean: $(PROJECT_DIRS)

default: TYPE =
default: $(PROJECT_DIRS)

$(PROJECT_DIRS):
	$(MAKE) -C $@ $(TYPE)

