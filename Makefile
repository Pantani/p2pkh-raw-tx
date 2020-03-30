# Project variables.
PROJECT_NAME := $(shell basename "$(PWD)")

## clean: Clean application files.
clean:
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.log' -delete

## install-packages: Install requirement dependencies.
install-packages:
	pip install -r requirements/common.txt

## test: Run unit tests.
test:
	pip install -r requirements/test.txt
	python manage.py test

## run: Run API.
run:
	python manage.py run

## start: Clean, install, test and run API.
start: clean install-packages tests run

.PHONY: help
all: help
help: Makefile
	@echo
	@echo " Choose a command run in "$(PROJECT_NAME)":"
	@echo
	@sed -n 's/^##//p' $< | column -t -s ':' |  sed -e 's/^/ /'
	@echo
