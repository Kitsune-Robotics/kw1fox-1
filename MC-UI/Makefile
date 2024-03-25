#
# Kitsune Robotics
# 2020-2024
#

ROOT := $(PWD)
STAGEDIR := $(ROOT)/dist/
HASH := $(shell git describe --tags --always)

all: help
help: # List all commands and their descriptions
	@echo
	@cat Makefile | grep ': #' --color=never | sed '/^\t/d' | sed 's/: / /' | column -t -s '#'
	@echo

setup: # Setup your local dev enviroment
	pipenv install -r requirements.txt
